"""Offline write-state audit. Python standard library only.
Usage: python analyze_states.py CORPUS_DIR INTRODUCTIONS_JSONL OUTPUT_DIR
INTRODUCTIONS_JSONL is from the accompanying functional-retry-audit.
No URLs or embedded code are executed.
"""
import collections
import csv
import hashlib
import json
from pathlib import Path
import re
import sys

GROUPS={'32e56f9e50c1bfc275de','e4441274ebcea72e7b1a','d9818687056ba13062a7'}
LINK=re.compile(r'\[(?:https?://|//)\S+(?:[ \t][^\]\n]*)?\]')
URL=re.compile(r'(?:https?://|//)[^\s<>"\x27]+')
COUNTY=re.compile(r'\bus-ma-\d{3}\b|["\x27]usd["\x27]\s*:\s*\d|\b(?:Barnstable|Berkshire|Bristol|Dukes|Essex|Franklin|Hampden|Hampshire|Middlesex|Nantucket|Norfolk|Plymouth|Suffolk|Worcester)\b',re.I)
ROW=re.compile(r'^\s*[A-Za-z][A-Za-z .\x27-]*\s*:\s*-?\d+(?:\.\d+)?(?:\s*,\s*-?\d+(?:\.\d+)?){2,}\s*$')
DECIMAL=re.compile(r'(?<![\w.])\d{1,7}(?:,\d{3})*\.\d{1,3}(?![\d.])')
DECODER=json.JSONDecoder()

def clean(body):
    # Do not decode requests into apparent returned data.
    return URL.sub('[URL]',LINK.sub('[LINK]',body))

def candidates(text):
    found=[];end=0
    for m in re.finditer(r'[\[{]',text):
        if m.start()<end:continue
        try:o,n=DECODER.raw_decode(text[m.start():])
        except ValueError:continue
        end=m.start()+n
        if isinstance(o,(dict,list)) and o:
            found.append(('json_literal',json.dumps(o,sort_keys=True,ensure_ascii=False)))
    for line in text.splitlines():
        line=line.strip()
        if not line:continue
        if COUNTY.search(line):found.append(('county_marker_candidate',line))
        if ROW.match(line):found.append(('numeric_row',line))
        if line.count('|')>=2 and re.search(r'\d',line):found.append(('table_candidate',line))
        if DECIMAL.search(line):found.append(('decimal_candidate',line))
    return sorted(set(found))

def dump(x):return json.dumps(x,ensure_ascii=False,sort_keys=True)
def fingerprint(s):return hashlib.sha256(s.encode()).hexdigest()

def main(inp,intros_path,out):
    out.mkdir(parents=True,exist_ok=True)
    rs=[json.loads(l) for l in (inp/'revisions.jsonl').open()]
    refs={r['rev_id']:r for r in rs};anchors={};intro_counts=collections.Counter()
    for l in intros_path.open():
        x=json.loads(l);intro_counts[x['rev_id']]+=1
        if x['group_id'] in GROUPS:
            old=anchors.get(x['page_id'])
            if old is None or x['seq']<old['seq']:
                anchors[x['page_id']]={k:x[k] for k in ['rev_id','seq','time','group_id']}
    cache={};states=[];all_candidates=[];first_global={}
    # Global first appearance is an export-order fact, not a causal attribution.
    for r in sorted(rs,key=lambda r:(r['time'],r['rev_id'])):
        b=r['body']
        if b not in cache:
            t=clean(b);cache[b]=(t,candidates(t))
        t,cs=cache[b]
        for kind,text in cs:
            k=(kind,text);earlier=first_global.get(k)
            if earlier is None:first_global[k]=r['rev_id']
            if r['page_id'] in anchors or earlier is None:
                all_candidates.append({'rev_id':r['rev_id'],'time':r['time'],'page_id':r['page_id'],'kind':kind,'text':text,'first_global_ref':first_global[k],'seen_in_earlier_export_order_record':earlier is not None})
    by_page=collections.defaultdict(list)
    for r in rs:by_page[r['page_id']].append(r)
    for p,rows in sorted(by_page.items()):
        previous=set()
        for r in sorted(rows,key=lambda r:r['seq']):
            t,cs=cache[r['body']];current=set(cs)
            if p in anchors:
                states.append({'rev_id':r['rev_id'],'page_id':p,'seq':r['seq'],'time':r['time'],'label':r['label'],'anchor':anchors[p]['rev_id'],'at_or_after_anchor':r['seq']>=anchors[p]['seq'],'new_url_references':intro_counts[r['rev_id']],'external_url_tokens_present':len(set(URL.findall(r['body']))),'candidate_counts':dict(collections.Counter(k for k,v in cs)),'new_on_page_candidates':[{'kind':k,'text':v,'first_global_ref':first_global[(k,v)]} for k,v in sorted(current-previous)],'nonlink_text':t})
            previous=current
    post=[s for s in states if s['at_or_after_anchor']]
    sensitivity=[];seen_sensitivity=set()
    for s in sorted(post,key=lambda s:(s['time'],s['rev_id'])):
        for kind,text in candidates(URL.sub('[URL]',refs[s['rev_id']]['body'])):
            if (kind,text) not in seen_sensitivity:
                seen_sensitivity.add((kind,text))
                sensitivity.append({'rev_id':s['rev_id'],'kind':kind,'text':text})
    gateway=[s for s in states if s['page_id']=='dse/AgentCountyGateway991']
    summary={'provenance':'Collusion Wiki published archive: https://collusion.wiki/explorer/download.html',
        'all_revisions_scanned':len(rs),'focus_pages':len(anchors),'focus_revisions_including_pre_anchor':len(states),'focus_revisions_at_or_after_first_reference':len(post),'focus_revisions_strictly_after_first_reference':sum(s['seq']>anchors[s['page_id']]['seq'] for s in post),
        'post_anchor_states_by_candidate_kind':dict(collections.Counter(k for s in post for k in s['candidate_counts'])),
        'new_post_anchor_candidates_by_kind':dict(collections.Counter(x['kind'] for s in post for x in s['new_on_page_candidates'])),
        'gateway':{'held_revisions':len(gateway),'first':gateway[0]['time'],'last':gateway[-1]['time'],'revisions_with_url_tokens':sum(s['external_url_tokens_present']>0 for s in gateway),'new_url_references':sum(s['new_url_references'] for s in gateway),'candidate_counts':dict(collections.Counter(k for s in gateway for k in s['candidate_counts']))},
        'globally_distinct_candidate_counts':dict(collections.Counter(k for k,v in first_global)),
        'post_anchor_link_label_retaining_sensitivity_candidates':len(sensitivity),
        'input_sha256':{'revisions.jsonl':fingerprint((inp/'revisions.jsonl').read_text()),'introductions.jsonl':fingerprint(intros_path.read_text())},
        'interpretation':'Candidate detectors are a review aid. Written numeric content is a proxy for progress, not authenticated retrieval. No runtime success classification.'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2))
    (out/'anchors.json').write_text(json.dumps(anchors,indent=2))
    control=refs['dse~Sector61AllStateValues2027@1']
    control_rows=[line for line in clean(control['body']).splitlines() if ROW.match(line)]
    (out/'numeric_data_comparison.json').write_text(json.dumps({'revision':control['rev_id'],'time':control['time'],'body':control['body'],'numeric_rows':len(control_rows),'numeric_cells':sum(len(line.split(':',1)[1].split(',')) for line in control_rows),'status':'Written numeric data in a separate task; provenance and correctness are not independently validated.'},indent=2))
    for name,data in [('focus_states.jsonl',states),('candidate_evidence.jsonl',all_candidates),('link_label_sensitivity.jsonl',sensitivity)]:
        with (out/name).open('w') as f:
            for x in data:f.write(dump(x)+'\n')
    with (out/'states.csv').open('w') as f:
        w=csv.writer(f);w.writerow(['revision','time','page','at_or_after_anchor','new_url_references','url_tokens_present','candidate_counts'])
        for s in states:w.writerow([s['rev_id'],s['time'],s['page_id'],s['at_or_after_anchor'],s['new_url_references'],s['external_url_tokens_present'],dump(s['candidate_counts'])])
    with (out/'gateway_nonlink_text.txt').open('w') as f:
        for s in gateway:f.write(s['rev_id']+' '+s['time']+'\n'+s['nonlink_text']+'\n\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]))
