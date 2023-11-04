import os
from bs4 import BeautifulSoup
from urllib.request import urlopen

folders = ['HTML','PDF']
for folder in folders:
    try:
        os.makedirs(folder)
    except FileExistsError:
        pass

def createSoup(url):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup

def cleanModule(module, file):
    soup = createSoup(module)

    # Remove header
    header = soup.find('div', class_="header-holder has-default-focus")
    header.decompose()

    # Remove Footer
    footers = soup.find_all('footer')

    for footer in footers:
        footer.decompose()

    # Remove Navs
    navs = soup.find_all('nav')

    for nav in navs:
        nav.decompose()
    
    # Removes feedback, article header, and mobile nav divs
    uselessDivs = ["ms--unit-user-feedback","article-header","mobile-nav"]
    for u in uselessDivs:
        soup.find(id=u).decompose()

    # Add url to unit title
    header = soup.h1
    newTag = soup.new_tag("a", href=module)
    newTag.string = soup.h1.string
    header.clear()
    header.append(newTag)

    f = open(f"HTML/{file}.html", "a")
    f.write(soup.prettify())
    f.close()

def main(url):
    soup = createSoup(url)

    modules = soup.find_all(attrs={"data-bi-name": "module"})

    for module in modules:
        url = module.find_all('a', limit=1)
        url = "https://learn.microsoft.com/en-us/training/" + url[0]['href'].lstrip('./')

        soup = createSoup(url)
        units = soup.find(id="unit-list")
        units = units.find_all('a')
        
        # Find title
        title = soup.find('h1').get_text().strip()

        # Export HTML
        fileName = title.replace(' ','-')

        try:
            os.remove(f"HTML/{fileName}.html")
        except FileNotFoundError:
            pass

        for unit in units:
            cleanModule(url + unit['href'], fileName)

        os.system(f"ebook-convert HTML/{fileName}.html PDF/{fileName}.pdf --page-breaks-before '//h:h1[position()>1]' --chapter '//h:h1' --chapter-mark 'rule' --use-auto-toc --pretty-print")

url = "https://learn.microsoft.com/en-us/training/paths/microsoft-azure-fundamentals-describe-cloud-concepts/"
main(url)