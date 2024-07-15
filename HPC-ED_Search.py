import argparse
import copy
import globus_sdk
import os
import pandas as pd
import subprocess
import sys
import time
import textwrap


###################################################
# Set your Index ID here for convenience (optional)
INDEX_ID = ""
###################################################


def process_title(title):
    if title:
        html = f'<b>{title}</b>'
        return html
    return ''

def process_authors(authors):
    if authors is None:
        return ''
    if isinstance(authors, list):
        return ', '.join(authors).replace('\\"', '"')
    else:
        return authors

def process_url(url):
    if url:
        html = f'<a href="{url}" target="_blank" rel="noopener noreferrer">{url}</a>'
        return html
    return ''

def process_keywords(keywords):
    if keywords is None:
        return ''
    if isinstance(keywords, list):
        return ', '.join(keywords)
    else:
        return keywords

def process_abstract(abstract):
    if abstract:
        return abstract.replace('\\"', '"')
    return ''

def process_duration(duration):
    if duration:
        try:
            return str(int(duration))
        except:
            return ''
    return ''

def process_rating(rating):
    if rating:
        try:
            return format(float(rating), ".1f")
        except:
            return ''
    return ''


def markdown_link(url):
    if url:
        return "[link](" + url + ")"
    return ''

def markdown_abs(abs):
    if abs:
        return abs.replace("<br>", " ").replace("</br>", "").replace("\n", "")
    return ''


description = textwrap.dedent(
    '''
    Globus Search Simple Script
    --------------------------------------------
     * (PACKAGES) Requires globus-sdk and pandas
     * Index_ID can be set in this file. 
     * One of query, provider, authors, keywords, or title must be provided as parameter. 
     * If you want to include '-' in the query, it needs to be written as '\-'.
     * If --limit and --offset are not provided, show all discovered entries. 
     * If --outpath is not set, it will be saved in the current working directory.
    '''
)


epilog = textwrap.dedent(
    '''
    Usage examples
    (IMPORTANT) In these examples, the index id is stored in '$INDEX_ID'. 
    Save your index id to a variable and try the examples, makes changes if necessary.
    --------------------------------------------
    1) python3 HPC-ED_Search.py --index_id $INDEX_ID --query 'parallel'
    Searches for entries with 'parallel' in any fields.

    2) python3 HPC-ED_Search.py --index_id $INDEX_ID --provider 'urn:ogf.org:glue2:access-ci.org:resource:cider:infrastructure.organizations:898'
    Searches for entries published by Cornell University Center for Advanced Computing (urn:ogf.org:glue2:access-ci.org:resource:cider:infrastructure.organizations:898).
    
    3) python3 HPC-ED_Search.py --index_id $INDEX_ID --keywords 'python'
    Searches for entries with 'python' in the keywords.
    
    4) python3 HPC-ED_Search.py --index_id $INDEX_ID --keywords 'python' --authors 'chris'
    Searches for entries with 'python' in the keywords and authored by 'Chris'

    5) python3 HPC-ED_Search.py --index_id $INDEX_ID --keywords 'python' --limit 5 --offset 5
    Searches for entries with 'python' in the keywords. Show 5 entries with 5 offset. 
    
    6) python3 HPC-ED_Search.py --index_id $INDEX_ID --keywords 'python' --outpath python
    Searches for entries with 'python' in the keywords and saves it to 'python.html' in the current working directory.

    7) python3 HPC-ED_Search.py --index_id $INDEX_ID --keywords 'python' --outpath HPC-ED_Docs/python
    Searches for entries with 'python' in the keywords and saves it to 'python.html' in 'HPC-ED_Docs' directory, if it does not exist, the directory will be made. 

    8) python3 HPC-ED_Search.py --index_id $INDEX_ID --keywords 'python' --outpath ~/HPC-ED_Docs/python
    Searches for entries with 'python' in the keywords and saves it to 'python.html' in '~/HPC-ED_Docs/' directory, if it does not exist, the directory will be made. 
    '''
)

def main():
    parser = argparse.ArgumentParser(description=description, epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('--index_id', help='HPC-ED Index ID')
    parser.add_argument('--query', help='Query String (optional).')
    parser.add_argument('--provider', help='Provider_ID (optional).')
    parser.add_argument('--authors', help='Authors (optional).')
    parser.add_argument('--keywords', help='Keywords (optional).')
    parser.add_argument('--title', help='Title (optional).')
    parser.add_argument('--markdown', type=bool, default=False, help='markdown (default false, HTML).')
    parser.add_argument('--limit', type=int, help='Limit (optional).')
    parser.add_argument('--offset', type=int, help='Offset (optional).')
    parser.add_argument('--advanced', type=bool, default=True, help='Advanced search (default true).')
    parser.add_argument('--outpath', help='Output file path (Optional). If not provided, HTML file name is based on time.')

    args = parser.parse_args()

    search_client = globus_sdk.SearchClient()

    # Check Index ID
    index_id = args.index_id
    if index_id is None and len(INDEX_ID) == 0:
        print("[Error] Index ID not provided")
        sys.exit(0)
    elif index_id is None:
        index_id = INDEX_ID

    # Check query string
    if args.query:
        qs = args.query
    elif args.provider or args.authors or args.keywords or args.title:
        qs = []
        if args.provider: qs.append(f'Provider_ID:"{args.provider}"')
        if args.authors: qs.append(f'Authors:{args.authors}')
        if args.keywords: qs.append(f'Keywords:{args.keywords}')
        if args.title: qs.append(f'Title:{args.title}')
        qs = " AND ".join(qs)
    else:
        print("[Error] None of query, provider, authors, keywords, titles are provided")
        sys.exit(0)

    # resolve some issue with -
    qs = qs.replace("\\-", "-")
    print(f"[INFO] Searching: '{qs}'")

    # number of entries to display
    display_all = args.limit is None and args.offset is None
    limit = args.limit if args.limit else 50
    offset = args.offset if args.offset else 0
    
    # Search
    response = search_client.search(index_id, qs, limit=limit, offset=offset, advanced=args.advanced)

    # if no entries
    if response.data['total'] == 0:
        print("[INFO] No entries found")
        sys.exit(0)

    # if entries found

    total = response.data['total']
    count = response.data['count']
    offset2 = response.data['offset']

    if display_all:
        print(f'[INFO] {total} entries found')
    else:
        print(f'[INFO] {total} entries found, displaying {offset2} to {offset2 + count - 1}')

    entries = copy.deepcopy(response.data['gmeta'])

    # get more entries
    if display_all:
        while response.data['has_next_page']:
            offset = offset + limit
            response = search_client.search(index_id, qs, limit=limit, offset=offset, advanced=args.advanced)
            entries = entries + copy.deepcopy(response.data['gmeta'])

    # columns to display, in this order
    columns = ['Title', 'Authors', 'URL', 'Keywords', 'Abstract', 'Duration', 'Rating']

    # Get metadata from the entries
    metadata = []
    for entry in entries:
        res = {}
        for col in columns:
            if col in entry['entries'][0]['content'].keys():
                res[col] = entry['entries'][0]['content'][col]
            else: 
                res[col] = None
        metadata.append(res)


    # Outpath
    outpath = args.outpath if args.outpath else str(time.time())
    if args.markdown:
        absolute_outpath = os.path.abspath(outpath + ".md") 
    else:
        absolute_outpath = os.path.abspath(outpath + ".html") 
    os.makedirs(os.path.split(absolute_outpath)[0], exist_ok=True)
    # Panda Dataframe and to html

    if not args.markdown:
        try:
            df = pd.DataFrame(metadata, columns=columns)
            html = df.to_html(absolute_outpath, escape=False, formatters=[
                process_title, process_authors, process_url, process_keywords, process_abstract, process_duration, process_rating
            ])
        except:
            print("[ERROR] Panda Error")
            sys.exit(0)

        print(f"[INFO] HTML file: {absolute_outpath}")

        # open in browser
        try:
            os.startfile(absolute_path)
        except AttributeError:
            try:
                subprocess.call(['open', absolute_outpath])
            except:
                print('[ERROR] Could not open html file')
    else:
        try:
            df = pd.DataFrame(metadata, columns=columns)
            print(df.iloc[5, 4])
            df.iloc[:,2] = df.iloc[:,2].apply(markdown_link)
            df.iloc[:,4] = df.iloc[:,4].apply(markdown_abs)
            print(df.iloc[5, 4])
            markdown = df.to_markdown(absolute_outpath)
            
            print(f"[INFO] HTML file: {absolute_outpath}")
        except:
            print("[ERROR] Panda Error")
            sys.exit(0)


if __name__ == "__main__":
    main()