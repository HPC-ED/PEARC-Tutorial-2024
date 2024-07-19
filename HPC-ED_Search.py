import argparse
import copy
import distutils
import globus_sdk
import os
import pandas as pd
import subprocess
import sys
import datetime
import textwrap


###################################################
# Set your Index ID here for convenience (optional)
INDEX_ID = ""
###################################################


def html_title(title):
    if title:
        title = f'<b>{title}</b>'
        return title
    return ''

def html_authors(authors):
    if authors is None:
        return ''
    if isinstance(authors, list):
        return ', '.join(authors).replace('\\"', '"')
    else:
        return authors

def html_url(url):
    if url:
        url = f'<a href="{url}" target="_blank" rel="noopener noreferrer">{url}</a>'
        return url
    return ''

def html_keywords(keywords):
    if keywords is None:
        return ''
    if isinstance(keywords, list):
        return ', '.join(keywords)
    else:
        return keywords

def html_abstract(abstract):
    if abstract:
        return abstract.replace('\\"', '"')
    return ''

def html_duration(duration):
    if duration:
        try:
            return str(int(duration))
        except:
            return ''
    return ''

def html_rating(rating):
    if rating:
        try:
            return format(float(rating), ".1f")
        except:
            return ''
    return ''


def markdown_title(title):
    if title:
        title = f'**{title}**'
        return title
    return ''

def markdown_link(url):
    if url:
        return "[link](" + url + ")"
    return ''

def markdown_abs(abs):
    if abs:
        return abs.replace("<br>", " ").replace("</br>", "").replace("\n", " ").replace("\r", " ")
    return ''


def str2bool(v):
    '''
    Provides flexible parameter input
    '''
    return bool(distutils.util.strtobool(v))

description = textwrap.dedent(
    '''
    Globus Search Simple Script
    --------------------------------------------
     * (PACKAGES) Requires globus-sdk and pandas
     * Index_ID can be set in the file. 
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

    7) python3 HPC-ED_Search.py --index_id $INDEX_ID --keywords 'python' --outpath ~/HPC-ED_Docs/python
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

    parser.add_argument('--limit', type=int, help='Limit (optional).')
    parser.add_argument('--offset', type=int, help='Offset (optional).')
    parser.add_argument("--advanced", type=str2bool, nargs='?',
                        const=True, default=True,
                        help='Advanced search (default true).')

    parser.add_argument("--markdown", type=str2bool, nargs='?',
                        const=True, default=False,
                        help='markdown (default false, output is HTML).')
    parser.add_argument('--outpath', help='Output file path (Optional). If not provided, file name is based on time.')

    args = parser.parse_args()

    # Make a search client
    search_client = globus_sdk.SearchClient()

    try:
        INDEX_ID
    except:
        INDEX_ID = ""

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
        print("[Error] None of query, provider, authors, keywords, and titles are provided")
        sys.exit(0)

    # resolve some issue with -
    qs = qs.replace("\\-", "-")
    qs_info = f"[INFO] Searching query: '{qs}'"
    print(qs_info)

    # number of entries to display
    display_all = args.limit is None and args.offset is None
    limit = args.limit if args.limit else 50
    offset = args.offset if args.offset else 0
    
    # Search
    try:
        response = search_client.search(index_id, qs, limit=limit, offset=offset, advanced=args.advanced)
    except:
        print("[Error] Please check your internet connection, check the INDEX_ID, \
                and check the query string for possible errors.")
        sys.exit(0)

    # if no entries
    if response.data['total'] == 0:
        print("[INFO] No entries found")
        sys.exit(0)

    # if entries found
    try:
        total = response.data['total']
        count = response.data['count']
        response_offset = response.data['offset']
    except:
        print("[Error] Globus Search Failed. Please email HPC-ED.")
        sys.exit(0)

    # show how many are displayed
    
    if display_all:
        display = f'[INFO] {total} entries found'
    else:
        display = f'[INFO] {total} entries found, displaying {response_offset} to {response_offset + count - 1}'
    print(display)

    # copy (save) data
    entries = copy.deepcopy(response.data['gmeta'])

    # get more entries
    try:
        if display_all:
            while response.data['has_next_page']:
                offset = offset + limit
                response = search_client.search(index_id, qs, limit=limit, offset=offset, advanced=args.advanced)
                entries = entries + copy.deepcopy(response.data['gmeta'])
    except:
        print("[Error] Please check your internet connection, check the INDEX_ID, \
                and check the query string for possible errors.")
        sys.exit(0)

    # columns to display in the table, in this order
    columns = ['Title', 'Authors', 'URL', 'Keywords', 'Abstract', 'Duration', 'Rating']

    # Get metadata from the entries
    try:
        metadata = []
        for entry in entries:
            res = {}
            for col in columns:
                if col in entry['entries'][0]['content'].keys():
                    res[col] = entry['entries'][0]['content'][col]
                else: 
                    res[col] = None
            metadata.append(res)
    except:
        print("[Error] Globus Search Failed. Please email HPC-ED.")
        sys.exit(0)

    # Set outpath
    outpath = args.outpath if args.outpath else datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    if args.markdown:
        absolute_outpath = os.path.abspath(outpath + ".md") 
    else:
        absolute_outpath = os.path.abspath(outpath + ".html") 
    os.makedirs(os.path.split(absolute_outpath)[0], exist_ok=True)

    # Panda Dataframe and to file
    if not args.markdown:
        # Make Pandas Dataframe and to html
        try:
            df = pd.DataFrame(metadata, columns=columns)
            df.to_html(absolute_outpath, escape=False, formatters=[
                html_title, html_authors, html_url, html_keywords, html_abstract, html_duration, html_rating
            ])

            # with open(absolute_outpath, "r+") as f:
            #     s = f.read() 
            #     f.seek(0)
            #     f.write(qs_info + "<br>" + display + "<br>" + s)

        except:
            print("[ERROR] Pandas Error")
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
            # Make Pandas Dataframe and to md
            df = pd.DataFrame(metadata, columns=columns)
            df.iloc[:,0] = df.iloc[:,0].apply(markdown_title)
            df.iloc[:,1] = df.iloc[:,1].apply(html_authors)
            df.iloc[:,2] = df.iloc[:,2].apply(markdown_link)
            df.iloc[:,3] = df.iloc[:,3].apply(html_keywords)
            df.iloc[:,4] = df.iloc[:,4].apply(markdown_abs)
            df.iloc[:,5] = df.iloc[:,5].apply(html_duration)
            df.iloc[:,6] = df.iloc[:,6].apply(html_rating)
            df.to_markdown(absolute_outpath)

            # with open(absolute_outpath, "r+") as f:
            #     s = f.read()
            #     f.seek(0)
            #     f.write(qs_info + "<br>" + display + "\n" + s)

            print(f"[INFO] Markdown file: {absolute_outpath}")
        except:
            print("[ERROR] Pandas Error")
            sys.exit(0)


if __name__ == "__main__":
    main()