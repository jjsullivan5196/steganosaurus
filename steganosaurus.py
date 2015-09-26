import os, sys, subprocess, argparse

parser = argparse.ArgumentParser(description='Take an image and hide/extract a file in/from it.')
subparsers = parser.add_subparsers(title = 'commands', dest='command')

inject = subparsers.add_parser('inject')
retrieve = subparsers.add_parser('retrieve')
check = subparsers.add_parser('check')

inject.add_argument('image', help='Image to hide file in.', type=str)
inject.add_argument('infile', help='File to hide in image.', type=str)
inject.add_argument('outfile', help='Name of final image.', type=str)

retrieve.add_argument('image', help='Image to retrieve file from.', type=str)
retrieve.add_argument('--override', '-o', help='Optional override for file name, original will be used if not specified.', type=str)

check.add_argument('image', help='Image to check.', type=str)

args = parser.parse_args()

def inject(args):
	subprocess.call([sys.executable, "injector.py", args.image, args.infile, args.outfile])
def retrieve(args):
	arglist = [sys.executable, "retriever.py", args.image]
	if isinstance(args.override, str):
		arglist.append(args.override)
	subprocess.call(arglist)
def check(args):
	subprocess.call([sys.executable, "checker.py", args.image])
commands = {'inject':inject, 'retrieve':retrieve, 'check':check}
commands[args.command](args)