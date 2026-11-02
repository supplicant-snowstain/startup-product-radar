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
    args=parser.parse_args()
    if args.command=='evaluate':
        report=evaluate_file(args.file)
        print(json.dumps(report,ensure_ascii=False,indent=2))
        if args.output: Path(args.output).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
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
