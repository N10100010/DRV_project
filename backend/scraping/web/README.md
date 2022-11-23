# Which web-scraping library to use?

## beautifulSoup
| FEATURES | PROS | CONS |
|:-:|:-:|:-:|
| good in working with authentic HTML | good adaptability | pulling huge amounts of data is hard without beeing ip-blaclisted (proxies do not seem to a propper option here) |
| built on well-known parseres (lxml, html5lib) | good documentation |  |
|  | ease of use |  |

## scrapy
| FEATURES | PROS | CONS |
|:-:|:-:|:-:|
| enhanced CSS selectors | simple API | not good with JS-based sites |
| xpath exp | interactive shell for testing CSS selectors and xpath | installation differs between OS's |
| fancy process monitor (not needed) | auto-detection of encodings | *only python 2.7*... |
| built-in support for various export formats |  |  |

## selenium
| FEATURES | PROS | CONS |
|:-:|:-:|:-:|
| fully func. JS interpreter  | webDriver module for multiple usages (auto test, cookie retrieval, etc.) | major: easy to be detected as a scraper |
| can be fast for pages that have a lot of images in them  | has its own weBrowser (not needed) | weBrowsesr in memory for it to run |
|  |  |  |