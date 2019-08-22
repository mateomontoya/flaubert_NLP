"""Download the HTML files of Flaubert's _Madame Bovary_ from www.bovary.fr .

This is the first of two steps in scraping the text of _Madame Bovary_. This
script downloads the HTML files and saves them to disk. In the second stage
(implemented in src/parse.py), we extract out the data we care about. You can
run this script as follows:

    $ python src/download.py

"""

import json
import os
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

HTML_DIR = 'data/html'  # where the HTML files are saved to
METADATA_FILE_NAME = 'data/html/metadata.json'

BASE_URL = 'https://www.bovary.fr'
# This is a JavaScript file that holds the URLs of the folio list pages.
MENU_URL = 'https://www.bovary.fr/jet/lib_js/m_tmp/menu_bov.js'
# This is the pattern of the URLs for the transcription of each folio.
FOLIO_URL = ('https://www.bovary.fr/folio_visu_trans.php?ret=1&'
             'folio={num}&org=2&zoom=50&seq=44&numero=')

# This regex is used to identify the URLs in the file at MENU_URL
CONTENT_LINK_PATTERN = re.compile(r'(contenu.php\?id=4&.*?)\"')
# The version metadata is reliably stored in the URL of the folio list pages.
VERSION_PATTERN = re.compile(r'recueil=(.)')

NO_VALUE = None  # Value to use when we don't find metadata for a field


def parse_version(folio_list_url):
    """Return the version of the folia linked at `folio_list_url`.

    The version metadata is not reliably stored in the HTML file of an
    individual folio. Instead, it is reliably in the URL of the page from which
    the folia are linked (the `folio_list_url`). We find the `folio_list_url`
    while we are searching the site for the folio URLs, so we use this function
    to extract the version number and save it along with the HTML files.

    Returns
    -------
    str
        One of 1-6 (for the brouillons), D (for definitif) or C (for Copiste)

    """
    match = VERSION_PATTERN.search(folio_list_url)
    if match:
        return match.group(1)
    return NO_VALUE


def retrieve_folio_urls():
    """Return URLs of the pages that actually hold the folio data.

    Returns
    -------
    List(tuple(str, str))
        (url, version)

    """
    print('Finding folio URLs')
    response = requests.get(MENU_URL)
    javascript_code = response.text
    relative_urls = CONTENT_LINK_PATTERN.findall(javascript_code)
    absolute_urls = []
    for url in relative_urls:
        url = url.replace('contenu.php?', 'folios_liste.php?type=f&')
        url = urljoin(BASE_URL, url)
        absolute_urls.append(url)
    result = {}
    for url in tqdm(absolute_urls):
        version = parse_version(url)
        if version != 'P':
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, 'html5lib')
            checkboxes = soup.find_all('input', attrs={'type': 'checkbox'})
            for checkbox in checkboxes:
                folio_num = checkbox['value']
                folio_url = FOLIO_URL.format(num=folio_num)
                result[folio_num] = {'url': folio_url, 'version': version}
    print('Finished finding folio URLS')
    return result


def download(url, num):
    """Download folio page at `url` to `num`.html."""
    response = requests.get(url)
    html = response.text
    file_name = os.path.join(HTML_DIR, '{}.html'.format(num))
    with open(file_name, 'w') as file:
        file.write(html)


def main():
    result = retrieve_folio_urls()
    with open(METADATA_FILE_NAME, 'w') as file:
        json.dump(result, file, indent=2)
    print('Downloading folia')
    for num, data in tqdm(result.items()):
        url = data['url']
        download(url, num)
    print('Finished downloading folia')


if __name__ == '__main__':
    main()
