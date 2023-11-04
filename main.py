import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.parse
import requests
import sys

learnPath = str(sys.argv[1])

if len(sys.argv) == 3:
    series = str(sys.argv[2])
else:
    series = "Microsoft Learn"

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

    # Remove scripts and links
    for tag in soup(["link", "script"]):
        tag.decompose()

    # Add url to unit title
    header = soup.h1
    newTag = soup.new_tag("a", href=unitUrl)
    newTag.string = soup.h1.string
    header.clear()
    header.append(newTag)
    header.name = "h3"

    # Change h2 to h4
    h3 = soup.find_all("h2")
    for h in h3:
        h.name = "h4"

    # Fix links
    links = soup.find_all("a")

    for link in links:
        try:
            if link["data-linktype"] in ["absolute-path", "relative-path"]:
                link["href"] = urllib.parse.urljoin(unitUrl, link["href"])
        except:
            pass

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
    fileName = (
        soup.find("h1").get_text().strip().replace(" ", "-")
    )  # Get filename before conversion otherwise nothing is found

    # Find and extract title. Yeah this is really hacky.
    title = soup.h1
    title.string.wrap(soup.new_tag("a"))
    title.a["href"] = url
    title.a.wrap(soup.new_tag("h1"))
    title.h1.wrap(soup.new_tag("html"))
    title = title.html.extract()

    # Process and export HTML. Deletes file first if already exists

    try:
        os.remove(f"HTML/{fileName}.html")
    except FileNotFoundError:
        pass

    exportHtml(title, fileName)

    modules = soup.find_all(attrs={"data-bi-name": "module"})

    for module in modules:
        # Find unit urls for this module
        url = module.find_all("a", limit=1)
        url = "https://learn.microsoft.com/en-us/training/" + url[0]["href"].lstrip(
            "./"
        )

        soup = createSoup(url)

        # Add h2 for module title
        moduleTitle = soup.h1
        moduleTitle.string.wrap(soup.new_tag("a"))
        moduleTitle.a["href"] = url
        moduleTitle.a.wrap(soup.new_tag("h2"))
        moduleTitle.h2.wrap(soup.new_tag("html"))
        moduleTitle = moduleTitle.html.extract()
        exportHtml(moduleTitle, fileName)

        units = soup.find(id="unit-list")
        units = units.find_all("a")

        for unit in units:
            cleaned = cleanModule(url + unit["href"])
            downloadImg(cleaned, url + unit["href"])
            exportHtml(cleaned, fileName)

    # Converts the HTML to PDF
    os.system(
        f"ebook-convert 'HTML/{fileName}.html' 'PDF/{fileName}.pdf' --page-breaks-before '//h:h2[position()>1]' \
        --chapter '//h:h2' --use-auto-toc --level1-toc '//h:h2' --level2-toc '//h:h3' \
        --pdf-page-numbers --pretty-print --pdf-serif-family 'Bookerly' --base-font-size 10\
        --authors 'Microsoft' --title '{title.find('a').string}' --series '{series}'"
    )


main(learnPath)
