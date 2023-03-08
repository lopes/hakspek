from argparse import ArgumentParser
from os import walk
from os.path import abspath, join, isdir, isfile
from time import sleep

from hakspek.conversation import text_processor


parser = ArgumentParser(
    description='SEO Advisor for blog posts in Markdown format'
    )
parser.add_argument(
    'path',
    nargs='+',
    help='List of files or directories to be processed'
    )
parser.add_argument(
    '--tags', '-t',
    required=False,
    default=3,
    help='Number of tags to generate'
    )
parser.add_argument(
    '--summary', '-s',
    required=False,
    default=15,
    help='Maximum number of words in summary'
    )
parser.add_argument(
    '--exclude', '-e',
    required=False,
    default=['_index.md'],
    nargs='+',
    help='List of markdown file names to be skipped'
    )
parser.add_argument(
    '--apikey', '-a',
    required=True,
    help='OpenAI\'s API key'
    )
parser.add_argument(
    '--delay', '-d',  # sleeps to avoid breaking the rate-limit: 20 reqs./min.
    required=False,
    default=20,  # seconds
    help='Wait (secs) between requests to avoid breaking rate limits in OpenAI'
)
args = parser.parse_args()


def show_suggestions(suggestions):
    print(f'''\
Suggestions:
\tTitle..: {suggestions["title"]}
\tSummary: {suggestions["summary"]}
\tTags...: {suggestions["tags"]}
''')

def run():
    for path in args.path:
        if isdir(path):
            for root,dirs,files in walk(abspath(path)):
                for f in files:
                    if f.endswith('.md') and f not in args.exclude:
                        print(f'Processing file: {f}')
                        try:
                            show_suggestions(text_processor(
                                join(root,f), 
                                args.summary, 
                                args.tags, 
                                args.apikey
                            ))
                        except TypeError:
                            print('Error processing file, try again.')
                        sleep(args.delay)
        elif isfile(path) and path.endswith('.md'):
            print(f'Processing file: {path}')
            try:
                show_suggestions(text_processor(
                    path, 
                    args.summary, 
                    args.tags, 
                    args.apikey
                ))
            except TypeError:
                print('Error processing file, try again.')
        else:
            print(f'Not found or not supported: {abspath(path)}')
