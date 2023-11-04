import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.parse
import requests
import sys

url = str(sys.argv[1])

# Create folders this script uses to export files

folders = ["HTML/img", "PDF"]
for folder in folders:
    try:
        os.makedirs(folder)
    except FileExistsError:
        pass

# Reusible soup function


def createSoup(url):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup


# Cleans soup object by reemoving unecessary components like header and footer


def cleanModule(unitUrl):
    soup = createSoup(unitUrl)

    # Remove header
    header = soup.find("div", class_="header-holder has-default-focus")
    header.decompose()

    # Remove Footer
    footers = soup.find_all("footer")

    for footer in footers:
        footer.decompose()

    # Remove Navs
    navs = soup.find_all("nav")

    for nav in navs:
        nav.decompose()

    # Removes feedback, article header, and mobile nav divs
    uselessDivs = ["ms--unit-user-feedback", "article-header", "mobile-nav"]
    for u in uselessDivs:
        soup.find(id=u).decompose()

    # Add url to unit title
    header = soup.h1
    newTag = soup.new_tag("a", href=unitUrl)
    newTag.string = soup.h1.string
    header.clear()
    header.append(newTag)

    return soup


def downloadImg(soup, baseUrl):
    images = soup.find_all("img")
    if images:
        for image in images:
            imageUrl = urllib.parse.urljoin(baseUrl, image["src"])
            imageName = os.path.basename(urllib.parse.urlparse(imageUrl).path)

            img_data = requests.get(imageUrl).content
            with open(f"HTML/img/{imageName}", "wb") as handler:
                handler.write(img_data)

            # Update image links so calibre can use images stored locally
            image["src"] = "img/" + imageName


# Exports the HTML. First deletes file if already exists


def exportHtml(html, file):
    f = open(f"HTML/{file}.html", "a")
    f.write(html.prettify())
    f.close()


# Does the main parsing of the learn path for modules and their units


def main(url):
    soup = createSoup(url)

    modules = soup.find_all(attrs={"data-bi-name": "module"})

    for module in modules:
        url = module.find_all("a", limit=1)
        url = "https://learn.microsoft.com/en-us/training/" + url[0]["href"].lstrip(
            "./"
        )

        soup = createSoup(url)
        units = soup.find(id="unit-list")
        units = units.find_all("a")

        # Find and extract title
        title = soup.find("h1").get_text().strip()

        # Process and export HTML. Deletes file first if already exists
        fileName = title.replace(" ", "-")

        try:
            os.remove(f"HTML/{fileName}.html")
        except FileNotFoundError:
            pass

        for unit in units:
            cleaned = cleanModule(url + unit["href"])
            downloadImg(cleaned, url + unit["href"])
            exportHtml(cleaned, fileName)

        # Converts the HTML to PDF
        os.system(
            f"ebook-convert HTML/{fileName}.html PDF/{fileName}.pdf --page-breaks-before '//h:h1[position()>1]' --chapter '//h:h1' --chapter-mark 'rule' --use-auto-toc --pretty-print"
        )


main(url)
