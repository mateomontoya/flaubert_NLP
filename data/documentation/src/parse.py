"""Extract out the data we care about from the downloaded HTML files.

This is the second of two steps in scraping the text of _Madame Bovary_. This
script parses HTML files and extracts out the data we want. It assumes that
the HTML files have already been downloaded (implemented in src/download.py).
The parsed data is saved as a CSV file to the data directory. You can run this
script as follows:

    $ python src/parse.py

"""

import json
import os
import re
from unicodedata import normalize

import ftfy
import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import Tag
from tqdm import tqdm

from download import HTML_DIR, METADATA_FILE_NAME, NO_VALUE

PARSED_FILE_NAME = 'data/parsed.csv'  # file the parsed data is saved in

# The chapter metadata seems to be listed in one of two ways
CHAPTER_PATTERN = re.compile(r'chap\.\s?(\d+)')
SECOND_CHAPTER_PATTERN = re.compile(r',\s?(\d+)\s?:')
FOLIO_PATTERN = re.compile(r'folio\s+(\d+\w?)')
# These last three regexes are used for retrieving the whole word when only a
# part of the word is marked in a tag (e.g. underlined)
PREFIX_PATTERN = re.compile(r'(\w+)$')
SUFFIX_PATTERN = re.compile(r'^(\w+)')
WHITESPACE_PATTERN = re.compile(r'\s')


def soupify(num):
    """Return BeautifulSoup soup object from downloaded HTML file `num`."""
    file_name = os.path.join(HTML_DIR, '{}.html'.format(num))
    with open(file_name) as file:
        html = file.read().strip()
    return BeautifulSoup(html, 'html5lib')


def clean_text(text):
    """Clean `text` of junk."""
    text = ftfy.fix_encoding(text)
    text = text.replace('&nbsp;', ' ')
    text = text.replace('\xa0', ' ')
    text = re.sub(r'\s+', r' ', text)
    text = normalize('NFC', text)
    return text.strip()


def parse_metadata(soup):
    """Return the metadata line in `soup`."""
    try:
        metadata = soup.find('hors-corpus').text
    # Some HTML files don't have 'hors-corpus' marked. In this case, I belive
    # the metadata is in the first HTML table.
    except AttributeError:
        metadata = soup.find('table').text
    return clean_text(metadata)


def parse_chapter(metadata):
    """Return the chapter number in `metadata`.

    Returns
    -------
    str
        Represents a number

    """
    match = CHAPTER_PATTERN.search(metadata)
    if match:
        return match.group(1)
    match = SECOND_CHAPTER_PATTERN.search(metadata)
    if match:
        return match.group(1)
    return NO_VALUE


def parse_folio_number(metadata):
    """Return the folio number in `metadata`.

    Returns
    -------
    str
        Represents a number, sometimes followed by a letter e.g. '6v'

    """
    match = FOLIO_PATTERN.search(metadata)
    if match:
        return match.group(1)
    return NO_VALUE


# The functions below all take the BeutifulSoup soup object and parse out some
# of the data we want


def parse_full_text(soup):
    """Return the full text on the page, minus the metadata.

    By inspecting the HTML of the pages, it became clear that all the data is
    stored in HTML tables. The first table holds the metadata, while the second
    holds the rest of the text. So the method used here for extracting the full
    text is to find the second table and extract the text from it.

    Returns
    -------
    str

    """
    table = soup.find_all('table')[1]
    return clean_text(table.text)


def parse_struck_through(soup):
    """Return all text that has been struck through.

    No magic here, we just look for all HTML elements that are tagged as <s>
    and join them together.

    Returns
    -------
    str

    """
    struck_through = soup.find_all('s')
    return ' '.join([clean_text(elem.text) for elem in struck_through])


def parse_previous_text(soup):
    """Return the original text of the folio.

    This is the text that is black on the screen, although we're not using CSS
    to find it. We look for all text that is not enclosed by <i> tags.

    Returns
    -------
    str

    """
    table = soup.find_all('table')[1]
    table_rows = table.find_all('td')
    result = ''
    for row in table_rows:
        contents = row.contents
        for c in contents:
            if isinstance(c, str):
                result += c + ' '
            elif isinstance(c, Tag):
                if c.name != 'i':
                    result += c.text + ' '
    return clean_text(result)


def parse_previous_no_struck(soup):
    """Return the original text that hasn't been struck through.

    We use an identical approach as above but then exclude text that is
    enclosed in <s> tags too.

    Returns
    -------
    str

    """
    table = soup.find_all('table')[1]
    table_rows = table.find_all('td')
    result = ''
    for row in table_rows:
        contents = row.contents
        for c in contents:
            if isinstance(c, str):
                result += c + ' '
            elif isinstance(c, Tag):
                if c.name not in ['i', 's']:
                    result += c.text + ' '
    return clean_text(result)


def parse_previous_struck(soup):
    """Return original text that has been struck through.

    Returns
    -------
    str

    """
    table = soup.find_all('table')[1]
    table_rows = table.find_all('td')
    result = ''
    for row in table_rows:
        contents = row.contents
        for c in contents:
            if isinstance(c, Tag):
                if c.name == 's':
                    result += c.text + ' '
    return clean_text(result)


def parse_marginalia(soup):
    """Return text that is in the margins.

    By inspecting the HTML, it looks like the marginalia are stored in <i>
    tags.

    Returns
    -------
    str

    """
    table = soup.find_all('table')[1]
    italics = table.find_all('i')
    return ' '.join([clean_text(i.text) for i in italics])


def parse_marginalia_no_struck(soup):
    """Return text in the margins that hasn't been struck through.

    Returns
    -------
    str

    """
    table = soup.find_all('table')[1]
    italics = table.find_all('i')
    result = ''
    for i in italics:
        contents = i.contents
        for c in contents:
            if isinstance(c, str):
                result += c + ' '
            elif isinstance(c, Tag):
                if c.name != 's':
                    result += c.text + ' '
    return clean_text(result)


def parse_marginalia_struck(soup):
    """Return text in the margins that *has* been struck through.

    Returns
    -------
    str

    """
    table = soup.find_all('table')[1]
    italics = table.find_all('i')
    result = ''
    for i in italics:
        contents = i.contents
        for c in contents:
            if isinstance(c, Tag):
                if c.name == 's':
                    result += c.text + ' '
    return clean_text(result)


def startswith_whitespace(s):
    """Return True if `s` starts with whitespace."""
    return WHITESPACE_PATTERN.match(s)


def whole_word(tag):
    """Return the whole word of `tag`.

    Sometimes only part of a word is underlined, yet we want all of the word.
    This function looks at the text to the left and right of the word. If
    there's no whitespace separating the text in this tag from the text to the
    left/right, then it must be part of the same word and we take it too.

    """
    text = tag.text
    previous, following = tag.previous_sibling, tag.next_sibling
    if isinstance(previous, Tag):
        previous = previous.text
    if isinstance(following, Tag):
        following = following.text
    word = ''
    # if the text in the tag itself starts with whitespace then there's no way
    # that the previous text is part of this word.
    if not startswith_whitespace(text):
        if previous:
            match = PREFIX_PATTERN.search(previous)
            if match:
                word += match.group(1)
    word += text
    if not startswith_whitespace(text[::-1]):
        if following:
            match = SUFFIX_PATTERN.search(following)
            if match:
                word += match.group(1)
    return clean_text(word)


def parse_underlined(soup):
    """Return text that has been underlined.

    Returns
    -------
    str

    """
    underlined = soup.find_all('u')
    return ' '.join([whole_word(u) for u in underlined])


def parse(soup):
    """Parse all the data we want from a HTML file.

    Except for the version, which comes from the metadata.json file.

    Returns
    -------
    dict

    """
    data = {}
    metadata = parse_metadata(soup)  # feature 4 in project description
    data['metadata'] = metadata
    data['chapter'] = parse_chapter(metadata)  # feature 2
    data['folio'] = parse_folio_number(metadata)  # feature 3
    data['text'] = parse_full_text(soup)  # feature 5
    data['struck'] = parse_struck_through(soup)  # feature 7
    data['previous'] = parse_previous_text(soup)  # feature 8
    data['previous_no_struck'] = parse_previous_no_struck(soup)  # feature 9
    data['previous_struck'] = parse_previous_struck(soup)  # feature 10
    data['margins'] = parse_marginalia(soup)  # feature 11
    data['margins_no_struck'] = parse_marginalia_no_struck(soup)  # feature 12
    data['margins_struck'] = parse_marginalia_struck(soup)  # feature 13
    data['underlined'] = parse_underlined(soup)  # feature 14
    return data


def main():
    with open(METADATA_FILE_NAME) as file:
        metadata = json.load(file)
    result = []
    for num, data in tqdm(metadata.items()):
        soup = soupify(num)
        parsed = parse(soup)
        parsed['version'] = data['version']
        result.append(parsed)
    result = pd.DataFrame(result)
    result.to_csv(PARSED_FILE_NAME, index=False)
    return result


if __name__ == '__main__':
    main()
