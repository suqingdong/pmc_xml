import re
import pathlib
import datetime

import requests
from dateutil.parser import parse as parse_date
from w3lib import html


def safe_open(filename: str, mode='r'):
    file = pathlib.Path(filename)

    if 'w' in mode and not file.parent.exists():
        file.parent.mkdir(parents=True)

    if filename.endswith('.gz'):
        import gzip
        return gzip.open(filename, mode=mode)

    return file.open(mode=mode)


def check_email(text: str):
    res = re.findall(r'([^\s]+?@.+)\.', text)
    return res[0] if res else None


def replace_entities(text: str):
    """
        multi level entites:
            - eg. PMCID=PMC9678136:  '&amp;lt;10' => '&lt;10' => '<10'
    """
    raw_text = text
    n = 5
    while n > 0:
        if re.search(r'&\w{2,7};', text):
            text = html.replace_entities(text)
        else:
            break
        n -= 1

    if n == 0:
        print(f'too many levels for: {repr(raw_text)}')
    return text


def get_pmc_xml(pmcid):
    """get pmc xml with eutils
    """
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id={pmcid}&format=xml'
    return requests.get(url).text


def check_date(element):
    year = element.findtext('Year')
    month = element.findtext('Month')
    day = element.findtext('Day')

    if not month:
        date = parse_date(year).strftime('%Y')
    elif not day:
        date = parse_date(f'{year}-{month}').strftime('%Y-%m')
    else:
        date = parse_date(f'{year}-{month}-{day}').strftime('%Y-%m-%d')

    return date
