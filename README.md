[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/ferru97)

# PyPaperBot_Adapted
PyPaperBot is a Python tool for **downloading scientific papers** using Google Scholar, Crossref, and SciHub.

Adapted for easier use from the original by:

- cli-driven menu.
- automatically finding a valid SciHub-server
- Adding info from latest download to results.csv (instead of replacing results.csv)
- Adding info from latest download to Bibtex (instead of replacing bibtex)
- Added preferences which can be stored between uses for download-location and list of SciHub-servers (to save time)

Features

- Download papers given a query
- Download papers given paper's DOIs
- Download papers given a Google Scholar link
- Generate Bibtex of the downloaded paper

## Installation
Use `pip` to install from pypi:

```bash
pip install PyPaperBot
```

## How to use

run program

````python
python __main__CLI.py
````

choose options:

1. Search with title: enter a query (f.i. title or title + (first) author)
2. Search with DOI (often available in description on sites like Pubmed)
3. Change Download location (default is ''./papers/'') (don't forget '/' at the end)
4. Update list of Sci-Hub Servers: fetches a moderated list from a website, checks these ands saves them to preferences.
5. Quit: quit program

On first-run the download-dir, results.csv and bitex.bib are made.

## SchiHub access
If access to SciHub is blocked in your country, consider using a free VPN service like [ProtonVPN](https://protonvpn.com/) or a paid service like [Mullvad](https://mullvad.net/)

## Disclaimer
This application is for educational purposes only. I do not take responsibility for what you choose to do with this application.


