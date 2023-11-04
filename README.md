# Convert MSFT Learn paths to PDFs

Script to convert MSFT Learn modules to PDFs. Might need more tweaking and testing, but at the moment it's working pretty well. Take a peak at the PDF folder for examples of converted PDFs all the Learn Paths for the AZ-400 Certification.

## Requirements
1. Install pip dependencies from requirements.txt
2. Calibre - https://calibre-ebook.com/download
    - Specifically this script uses the ebook-convert CLI tool
- Optional: Install Amazon's Bookerly font - https://developer.amazon.com/en-US/alexa/branding/echo-guidelines/identity-guidelines/typography
  - Shouldn't break anything if you don't have it, but let me know and I might be able to add some logic to check

## How to use
Once the requiremments are installed, you can simply run with the url as a commandline argument.

```
python3 main.py 'https://learn.microsoft.com/en-us/training/paths/az-400-get-started-devops-transformation-journey/'
```

Alternatively, you can pass a 'Series' name after the URL if you want to keep track of which Certfication the PDFs are for with your EBook manager.
```
python3 main.py 'https://learn.microsoft.com/en-us/training/paths/az-400-get-started-devops-transformation-journey/' 'AZ-400'
```

The structure of these paths is Learning Path -> Module -> Units. PDFs should have a Table of Content with the chapters being the Module names, and sub-chapters being the unit names
