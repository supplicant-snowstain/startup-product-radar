import argparse
import json
from pathlib import Path
from .evaluator import evaluate_file

def main():
    parser=argparse.ArgumentParser(description='Startup Radar evidence audit')
    sub=parser.add_subparsers(dest='command',required=True)
    ev=sub.add_parser('evaluate')
    ev.add_argument('file')
    ev.add_argument('--output')
    bench=sub.add_parser('benchmark')
    bench.add_argument('--cases',default='tools/startup_lab/benchmarks/cases.json')
    promote_parser=sub.add_parser('promote',help='Promote a manually reviewed candidate to the evidence store')
    promote_parser.add_argument('file')
    promote_parser.add_argument('--output-dir',default='data/evidence')
    for command in ('search','sides'):
        p=sub.add_parser(command)
        p.add_argument('query')
        p.add_argument('--root',default='.')
        p.add_argument('--limit',type=int,default=10)
    candidate_parser=sub.add_parser('candidates')
    candidate_parser.add_argument('report')
    snapshot=sub.add_parser('verify-snapshot',help='Check a quoted excerpt in local HTML, without making network requests')
    snapshot.add_argument('html_file')
    snapshot.add_argument('excerpt')
    discovery=sub.add_parser('discover',help='Browse evidence-linked user needs')
    discovery.add_argument('query',nargs='?',default='')
    discovery.add_argument('--root',default='.')
    discovery.add_argument('--limit',type=int,default=20)
    exploration=sub.add_parser('explore',help='Inspect need, products and evidence')
    exploration.add_argument('need_id')
    exploration.add_argument('--root',default='.')
    pd=sub.add_parser('discover-public',help='Browse provisional attributed public signals')
    pd.add_argument('query',nargs='?',default='')
    pd.add_argument('--root',default='.')
    pd.add_argument('--limit',type=int,default=20)
    pe=sub.add_parser('explore-public',help='Explore a provisional source signal')
    pe.add_argument('signal_id')
    pe.add_argument('--root',default='.')
    args=parser.parse_args()
    if args.command=='evaluate':
        report=evaluate_file(args.file)
        print(json.dumps(report,ensure_ascii=False,indent=2))
        if args.output: Path(args.output).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    elif args.command=='promote':
        from .extraction import promote
        result=promote(args.file,args.output_dir)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        if not result['accepted']: raise SystemExit(1)
    elif args.command in ('search','sides'):
        from .retrieval import retrieve,evidence_sides
        fn=retrieve if args.command=='search' else evidence_sides
        print(json.dumps(fn(args.root,args.query,args.limit),ensure_ascii=False,indent=2))
    elif args.command=='verify-snapshot':
        from .source_verify import match_snapshot
        content=Path(args.html_file).read_text(encoding='utf-8')
        result=match_snapshot(content,args.excerpt)
        result['source_file']=args.html_file
        result['verification_scope']='text presence in supplied local snapshot only'
        print(json.dumps(result,ensure_ascii=False,indent=2))
    elif args.command=='discover-public':
        from .public_opportunities import discover_public
        print(json.dumps(discover_public(args.root,args.query,args.limit),ensure_ascii=False,indent=2))
    elif args.command=='explore-public':
        from .public_opportunities import explore_public
        print(json.dumps(explore_public(args.root,args.signal_id),ensure_ascii=False,indent=2))
    elif args.command=='discover':
        from .opportunity import discover
        print(json.dumps(discover(args.root,args.query,args.limit),ensure_ascii=False,indent=2))
    elif args.command=='explore':
        from .opportunity import explore
        print(json.dumps(explore(args.root,args.need_id),ensure_ascii=False,indent=2))
    elif args.command=='candidates':
        from .report_candidates import report_candidates
        print(json.dumps(report_candidates(args.report),ensure_ascii=False,indent=2))
    else:
        p=Path(args.cases); cases=json.loads(p.read_text(encoding='utf-8')); passed=0
        for case in cases:
            result=evaluate_file(p.parent/case['file'])
            ok=result['status']==case['expected_status'] and set(result['risk_flags'])==set(case['expected_risk_flags'])
            print(f"{'PASS' if ok else 'FAIL'} {case['id']}: {result['status']}")
            passed+=ok
        print(f'{passed}/{len(cases)} passed')
        if passed!=len(cases): raise SystemExit(1)

if __name__=='__main__': main()
