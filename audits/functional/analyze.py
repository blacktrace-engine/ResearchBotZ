"""Group newly introduced URL formulations; never treats them as executed requests.
Usage: python analyze.py CORPUS_DIR OUTPUT_DIR
Standard library, offline. Unknown query parameters and expressions are preserved.
"""
import collections as C
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit, parse_qsl, unquote

TOKEN=re.compile(r'https?://[^\s\[\]<>"\x27]+')
NONCE={'uniq','unique','nonce','cb','cachebust','cache_bust','cachebuster','rnd','rand','random','_','timestamp','ts'}
DELIVERY={'max_tokens','mode','format','output','pretty','indent','download','callback','cache'}
QUERY_WRAPPERS={'jqp.vercel.app':('url',),'allorigins.hexlet.app':('url',),'api.allorigins.win':('url',),'api.codetabs.com':('quest',),'corsproxy.io':('url',),'md.succ.ai':('url',),'markdown.new':('url',),'r.jina.ai':('url',),'webcrawlerapi.com':('url',),'docs.google.com':('url',),'md.dhr.wtf':('url',)}
PATH_WRAPPERS={'md.succ.ai','markdown.new','r.jina.ai','pure.md','cors.isomorphic-git.org','cors.bwa.workers.dev','test.cors.workers.dev','proxy.corsfix.com'}
RENDERERS={'md.succ.ai','markdown.new','r.jina.ai','pure.md','md.dhr.wtf','docs.google.com','webcrawlerapi.com'}
SHORTENERS={'is.gd','v.gd','tinyurl.com','bit.ly','da.gd'}

def dumps(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def hid(x):return hashlib.sha256(dumps(x).encode()).hexdigest()[:20]
def decode_target(v):
    # Only peel whole-string encoding until a scheme becomes parseable.
    for _ in range(3):
        if v.startswith(('https://','http://')):return v
        w=unquote(v)
        if w==v:break
        v=w
    return v if v.startswith(('https://','http://')) else None

def classify(raw):
    current=raw;hops=[];transforms=[];render=False;flags=[]
    for depth in range(6):
        try:
            z=urlsplit(current);host=(z.hostname or '').lower()
            if not host or not z.scheme:raise ValueError()
            pairs=parse_qsl(z.query,keep_blank_values=True)
            _=z.port
        except ValueError:return {'error':'unparseable','raw':raw}
        target=None;target_key=None
        for key in QUERY_WRAPPERS.get(host,()):
            vals=[v for k,v in pairs if k==key]
            if len(vals)==1:
                target=decode_target(vals[0]);target_key=key
                if target:break
        if target is None and host in PATH_WRAPPERS:
            target=decode_target(z.path.lstrip('/'))
            # Bare-host embedded paths remain unresolved; do not invent a scheme.
        if target is None:break
        other=[(k,v) for k,v in pairs if k!=target_key]
        for k,v in other:
            if k=='jq':transforms.append({'operator':'jq','expression':v})
        unknown=[(k,v) for k,v in other if k not in NONCE|DELIVERY|{'jq'}]
        if unknown:transforms.append({'wrapper_unknown_parameters':unknown})
        if host in RENDERERS:render=True
        hops.append({'host':host,'scheme':z.scheme,'authority':z.netloc,'path':z.path,'parameters':other,'fragment':z.fragment})
        if target_key is None and pairs:
            flags.append('path_wrapper_query_scope_ambiguous')
        current=target
    else:flags.append('wrapper_depth_limit')
    # current and z refer to the final leaf unless depth-limit was reached.
    try:
        z=urlsplit(current);host=(z.hostname or '').lower();pairs=parse_qsl(z.query,keep_blank_values=True)
    except ValueError:return {'error':'unparseable_leaf','raw':raw}
    resource=host+z.path
    result=[(k,v) for k,v in pairs if k not in NONCE|DELIVERY]
    nonce=[(k,v) for k,v in pairs if k in NONCE]
    delivery=[(k,v) for k,v in pairs if k in DELIVERY]
    operation='retrieve-reference'
    if transforms:operation='retrieve-and-transform'
    if render:operation+='-rendered'
    action=dict(pairs).get('action')
    if 'wiki.cgi' in z.path or 'wiki2.cgi' in z.path:
        operation='wiki-reference:'+str(action or 'unspecified')
    if host=='api.counterapi.dev' and z.path.rstrip('/').endswith(('/up','/down','/set')):
        operation='counter-mutation-reference'
    if host in SHORTENERS:flags.append('shortener_destination_unknown')
    if host in PATH_WRAPPERS|set(QUERY_WRAPPERS) and not hops:
        flags.append('wrapper_unresolved_or_not_embedded')
    if z.fragment:flags.append('fragment_retained_as_delivery_variant')
    # Port, scheme, raw URL spelling, encoding, fragment, limits and routing stay visible.
    functional={'resource':resource,'requested_result':{'query':result,'transforms':transforms},'operation':operation}
    transport={'leaf_scheme':z.scheme,'leaf_authority':z.netloc,'hops':hops,'delivery':delivery,'fragment':z.fragment,'nonce':nonce}
    return {'group_id':hid(functional),'functional':functional,'transport_id':hid(transport),'transport':transport,'flags':flags,'raw':raw}

def main(inp,out):
    out.mkdir(parents=True,exist_ok=True)
    rs=[json.loads(l) for l in (inp/'revisions.jsonl').open()]
    es=[json.loads(l) for l in (inp/'events.jsonl').open()]
    pages=C.defaultdict(list)
    for x in rs:pages[x['page_id']].append(x)
    events_by_rev=C.defaultdict(list)
    for x in es:
        if x.get('revision_ref'):events_by_rev[x['revision_ref']].append(x)
    cache={};records=[];counts=C.Counter();claims=[]
    claim_re=re.compile(r'\b(success|failed|blocked|denied|error|answered|confirmed|correct|result|response|timeout|525|403|404|429)\b',re.I)
    for page,rows in sorted(pages.items()):
        prev=set();priorlines=set()
        for index,x in enumerate(sorted(rows,key=lambda x:x['seq'])):
            allurls=set(TOKEN.findall(x['body']));added=allurls-prev
            counts['url_revision_pairs_including_carryforward']+=len(allurls)
            counts['url_tokens_carried_from_previous_held_revision']+=len(allurls&prev)
            for raw in sorted(added):
                if raw not in cache:cache[raw]=classify(raw)
                a=cache[raw]
                if 'error' in a:counts['unparseable_introductions']+=1;continue
                records.append({'rev_id':x['rev_id'],'page_id':page,'time':x['time'],'seq':x['seq'],'label':x['label'],'ip16':x['ip16'],'first_held_revision':index==0,**a,'linked_event_types':[e['event_type'] for e in events_by_rev[x['rev_id']]],'external_result_status':'unlinked_unknown'})
            newlines=[l for l in x['body'].splitlines() if l not in priorlines]
            for l in newlines:
                if claim_re.search(TOKEN.sub('',l)):
                    claims.append({'rev_id':x['rev_id'],'page_id':page,'time':x['time'],'label':x['label'],'text':l,'status':'unverified_text_claim_not_linked_response'})
            prev=allurls;priorlines=set(x['body'].splitlines())
    records.sort(key=lambda x:(x['time'],x['page_id'],x['seq'],x['raw']))
    groups={}
    for row in records:
        k=row['group_id']
        if k not in groups:groups[k]={'group_id':k,**row['functional'],'n':0,'revisions':set(),'pages':set(),'labels':set(),'transports':set(),'raws':set(),'first':row['time'],'last':row['time'],'refs':[],'flagged':0,'repeats_same_raw_global':0,'repeats_same_transport_global':0}
        g=groups[k];g['n']+=1;g['pages'].add(row['page_id']);g['labels'].add(row['label']);g['last']=row['time']
        g['revisions'].add(row['rev_id'])
        row['raw_seen_previously_in_group']=row['raw'] in g['raws'];row['transport_seen_previously_in_group']=row['transport_id'] in g['transports']
        g['repeats_same_raw_global']+=row['raw_seen_previously_in_group'];g['repeats_same_transport_global']+=row['transport_seen_previously_in_group']
        g['raws'].add(row['raw']);g['transports'].add(row['transport_id']);g['flagged']+=bool(row['flags'])
        if len(g['refs'])<8:g['refs'].append(row['rev_id'])
    serial=[]
    for g in groups.values():
        serial.append({**g,'revisions':len(g['revisions']),'pages':len(g['pages']),'labels':len(g['labels']),'transports':len(g['transports']),'raws':len(g['raws'])})
    serial.sort(key=lambda x:(-x['n'],x['group_id']))
    for filename,data in [('introductions.jsonl',records),('claim_candidates.jsonl',claims)]:
        with (out/filename).open('w') as f:
            for x in data:f.write(dumps(x)+'\n')
    with (out/'groups.json').open('w') as f:json.dump(serial,f,indent=2)
    with (out/'groups.csv').open('w') as f:
        w=csv.writer(f);w.writerow(['group_id','resource','operation','requested_result_json','introductions','revisions','pages','labels','raw_urls','transport_descriptors','first','last'])
        for g in serial:w.writerow([g['group_id'],g['resource'],g['operation'],dumps(g['requested_result']),g['n'],g['revisions'],g['pages'],g['labels'],g['raws'],g['transports'],g['first'],g['last']])
    external_keys={'status_code','http_status','response_body','response_hash','request_url','response_url','tool_result'}
    summary={'scope':'All revisions scanned; lexical URL formulations only. Not executed requests, not run-level trajectories. User describes corpus as synthetic.',
      'records':len(rs),'counts':dict(counts),'introduced_url_formulations':len(records),'unique_raw_urls':len(cache),'functional_groups':len(groups),'repeated_functional_groups':sum(g['n']>1 for g in serial),'introductions_beyond_first_per_group':sum(g['n']-1 for g in serial),
      'repeated_raw_introductions':sum(g['repeats_same_raw_global'] for g in serial),
      'flag_counts':dict(C.Counter(f for x in records for f in x['flags'])),
      'claim_candidates':len(claims),'event_fields_intersecting_response_keys':sorted(set().union(*(x.keys() for x in es))&external_keys),
      'external_outcome_assessment':'No structured external response fields found. URL execution and external outcome remain unknown; free-text claim candidates are not validated responses.',
      'event_types':dict(C.Counter(x['event_type'] for x in es)),
      'nonce_parameter_names':sorted(NONCE),'delivery_parameter_names':sorted(DELIVERY),
      'input_sha256':{n:hashlib.sha256((inp/n).read_bytes()).hexdigest() for n in ['pages.jsonl','revisions.jsonl','events.jsonl','labels.jsonl','manifest.json']},
      'top_groups':serial[:20]}
    with (out/'summary.json').open('w') as f:json.dump(summary,f,indent=2)
    print(dumps({k:v for k,v in summary.items() if k not in {'top_groups','input_sha256'}}))

if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]))
