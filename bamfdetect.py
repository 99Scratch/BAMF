#!/usr/bin/env python
import bamfdetect
import json


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(
        prog=__file__,
        description="Identifies and extracts information from bots",
        version="%(prog)s v" + bamfdetect.get_version() + " by Brian Wallace (@botnet_hunter)",
        epilog="%(prog)s v" + bamfdetect.get_version() + " by Brian Wallace (@botnet_hunter)"
    )
    parser.add_argument('path', metavar='path', type=str, nargs='*', default=None,
                        help="Paths to files or directories to scan")
    parser.add_argument('-d', '--detect', default=False, required=False, action='store_true', help="Only detect files")
    parser.add_argument('-r', '--recursive', default=False, required=False, action='store_true',
                        help="Scan paths recursively")
    parser.add_argument('-l', '--list', default=False, required=False, action='store_true',
                        help='List available modules')
    parser.add_argument('-m', '--module', default=None, type=str, action='append', help='Modules to use, if not defined'
                                                                                        'all modules are used')

    args = parser.parse_args()

    if args.list:
        for mod in bamfdetect.get_loaded_modules():
            print mod
    else:
        if args.path is None or len(args.path) == 0:
            parser.print_help()
            exit()
        results = bamfdetect.scan_paths(args.path, args.detect, args.recursive, args.module)
        print json.dumps(results, sort_keys=True, indent=4, separators=(',', ': '))