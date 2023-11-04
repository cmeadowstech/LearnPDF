# Convert MSFT Learn paths to PDFs

Script to convert MSFT Learn modules to PDFs. Might need more tweaking and testing, but at the moment it's working pretty well. Take a peak at the PDF folder for examples of converted PDFs from the Learn Path [AZ-400: Get started on a DevOps transformation journey](https://learn.microsoft.com/en-us/training/paths/az-400-get-started-devops-transformation-journey/)

## Requirements
1. Install pip dependencies from requirements.txt
2. Calibre - https://calibre-ebook.com/download
    - Specifically this script uses the ebook-convert CLI tool

## How to use
Once the requiremments are installed, you can simply run with the url as a commandline argument.

```
python3 main.py 'https://learn.microsoft.com/en-us/training/paths/az-400-get-started-devops-transformation-journey/'
```