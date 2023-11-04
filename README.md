# Convert MSFT Learn paths to PDFs

Script to convert MSFT Learn modules to PDFs. Still a POC; needs further testing. Not sure how consistent their HTML layouts are. I tried to remove the consistent divs such as the header and footer instead of selecting the content for better reliability, but we'll see how it goes.

Closer to completion I will update script to properly run from CLI instead of editing the URL variable manually.

This is reliant on Calibre being installed. Testing on Debian 12, where you can install with 

```
apt install calibre
```

See [Calibre docs](https://manual.calibre-ebook.com/generated/en/ebook-convert.html) for more information on ebook-convert