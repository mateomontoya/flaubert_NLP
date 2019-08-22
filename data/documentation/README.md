# Scraping Flaubert

This project scrapes data from [bovary.fr](www.bovary.fr).

## Structure of the project

All the files for the project live in this directory and its subdirectories.
The LICENSE file describes that this software is licensed under the MIT License.
The Makefile contains code to automate some aspects of working on the project.
For example, it automates the process of installing the dependencies and
ensuring good code style is used. If you're not familiar with Makefiles, you can
ignore this. This README.md describes important information about the project.
The requirements subdirectory holds the dependencies (other libraries) used in
the project. The prod.txt file holds the dependencies you'd need to replicate
the scraping, while the dev.txt file holds extra dependencies you'd need to
develop the project. These mainly have to do with the Makefile, so can safely be
ignored. The src subdirectory contains the source code for the project. There
are two Python scripts here: download.py and parse.py. download.py is used to
download the raw HTML files from the website, while parse.py is used to extract
out the relevant information from those HTML files once they've been downloaded.
The data subdirectory is where all the data is held. The raw HTML files are kept
in the html subdirectory of the data subdirectory. Each HTML file is numbered
by the folio number from the website. Outside of the html subdirectory but still
in the data directory is parsed.csv, which holds the parsed data. Each row is
a folio and the columns represent different features. The whole project is
structured as follows:

.
├── LICENSE
├── Makefile
├── README.md
├── requirements
│   ├── dev.txt
│   └── prod.txt
├── data
│   ├── html
│       ├── metadata.json
        ├── 1.html
        ├── ...
|    ├── parsed.csv
└── src
    ├── download.py
    └── parse.py

## How to replicate the scraping

You can replicate the scraping with three easy steps. These steps assume you
have Python 3 installed.

1. Ensure that the dependencies are installed. While in this top-level directory,
you can do this by running `make install`. Alternatively, just make sure you have
all the packages in requirements/prod.txt installed. The specific version numbers
shouldn't be too important (i.e. requests 2.21 should work the same as 2.22).
2. Download the HTML files. While in this top-level directory, you can do this
by running `python src/download.py`. This will print a progress bar to your
screen, and should take just under an hour (it's downloading ~4,500 files!)
3. Parse the relevant data from the HTML files by running `python src/parse.py`,
again while in this top-level directory. This will create parsed.csv which holds
all the data. This should take around 5 minutes.

## How the scraping works

The scraping works in two steps: downloading and parsing.

#### Downloading the HTML files

First, we download all the HTML files from the website. We do this as a separate
step because it takes a decent amount of time (around an hour). If we make any
changes to the parsing code (e.g. perhaps we decide we want to add a new feature)
then we don't want to have to download all those files again. It's also nicer to the
bovary.fr website because we're not taxing their servers as much.

The website has an interesting layout. The menu bar on the lefthand side is not
described in the HTML but in a JavaScript script linked to that page. This means
that the links to the folio pages are found in the JavaScript file not the HTML.
So we download that JavaScript file and extract out the links to the folio list
pages. These pages (or more precisely their URLs) are where the version
information is kept so we parse out this information.

#### Parsing the HTML files

Once we've downloaded the HTML files, we read them in and use BeautifulSoup to
parse them. We then have a function for each feature that we want to extract
out. For details of how the features are extracted, see the function definition
in parse.py.

## Authors
[Geoff Bacon](https://geoffbacon.github.io/)

## License

[MIT](https://choosealicense.com/licenses/mit/)
