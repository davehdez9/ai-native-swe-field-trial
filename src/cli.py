"""CLI for the offline personal task tracker."""
import argparse
import json
import sys
from .tracker import TaskStore

def main(argv=None):
    parser=argparse.ArgumentParser(description='Local task tracker')
    parser.add_argument('--store',required=True,help='path to local JSON tasks file')
    subs=parser.add_subparsers(dest='command',required=True)
    add=subs.add_parser('add');add.add_argument('--id',required=True);add.add_argument('--title',required=True);add.add_argument('--due')
    complete=subs.add_parser('complete');complete.add_argument('--id',required=True)
    subs.add_parser('list')
    late=subs.add_parser('overdue');late.add_argument('--as-of',required=True)
    find=subs.add_parser('search');find.add_argument('--query',required=True,help='case-insensitive title substring (use --query=VALUE if VALUE starts with -)')
    args=parser.parse_args(argv)
    tasks=TaskStore(args.store)
    try:
        if args.command=='add': result=tasks.add(args.id,args.title,args.due)
        elif args.command=='complete':tasks.complete(args.id);result={'id':args.id,'done':True}
        elif args.command=='list':result=tasks.load()
        elif args.command=='overdue':result=tasks.overdue(args.as_of)
        elif args.command=='search':result=tasks.search(args.query)
        else:raise ValueError(f'unknown command {args.command}')
    except (ValueError,TypeError,KeyError,OSError) as exc:
        print(f'error: {exc}',file=sys.stderr)
        return 2
    print(json.dumps(result,sort_keys=True))
    return 0

if __name__=='__main__':sys.exit(main())
