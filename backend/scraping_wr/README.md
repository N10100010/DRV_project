# Usage: _main.py



## Grab a competition and save dump to a JSON file

**Usage**

```
$ python -m scraping_wr._main grabc --help
usage: _main.py grabc [-h] [-i UUID] [-o OUT]

options:
  -h, --help            show this help message and exit
  -i UUID, --uuid UUID  Scrape competition and save as JSON
  -o OUT, --out OUT     Specify path for output
```

**Example:**

```sh
python -m scraping_wr._main grabc --uuid 718b3256-e778-4003-88e9-832c4aad0cc2 --out dump.json
```


## Run remaining test code

```sh
python -m scraping_wr._main
```