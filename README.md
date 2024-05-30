# Download_ICLR24_paper_pdf

##  Manually Dwonload the openreview website of ICLR 2024 papers
[https://openreview.net/group?id=ICLR.cc/2024/Conference#tab-accept-oral](https://openreview.net/group?id=ICLR.cc/2024/Conference#tab-accept-oral)

* Note every time you press `ctrl+s`, you must select `download all` rather than `single html`.
* Every time it will save the all tabs with current page index, for example, you have the 1st page of the oral, 2nd page of the poster, you will have the all of them in your saved files, so I recommend you to save every page one by one. 
* The saved file should be named as `oral_1.html`, `oral_2.html`, `poster_1.html`, `poster_2.html`, etc. to the `pages` foler.

## Download the pdfs from the saved html files
```bash
python download.py
```

## Extract the pdfs
```bash
python extract_first_page.py
```