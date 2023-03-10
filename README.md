# website-monitor

Monitor for web sites changes in a CSV report with feature of saving HTML file in history folder.

## Synopsis

```
Usage:
------
 monitor.py [-T timing] [-c count_max] [-t timeout] [-o report.csv] [-f urls.lst] [-H]

Defaults:
---------
 -T 900        = timing 900 seconds between loops
 -c 1000000    = at least a whole day
 -t 45         = 45 timeout per website request
 -o report.csv = default output file is report.csv
 -f urls.lst   = default input file is report.csv
 -H            = save (or not) history in html files under folder history of current dir

Exemples:
---------
 monitor.py # with no args
 monitor.py -f urls.lst
 monitor.py -f urls.lst -t 45 -o url_stats.csv -f url_file-list.txt -c 100 -T 60
 for site in github microsoft ; do monitor.py -f $site.lst -t 45 -o stats-$site.csv ; done
```

## Result

_Note: some website have token/javascript content generated, so md5 could change._
_For exemple protections include token to block bruteforce login._

```
date                 | status          | elapsed         | size   | md5                              | url
-------------------- | --------------- | --------------- | ------ | -------------------------------- | --------------------------------------------------
2023/02/24 03:39:43  | 200             | 219778          | 56944  | 1fcac5ad4c19abdb45b19ecf06ccef59 | https://www.google.com/
2023/02/24 03:39:43  | 200             | 218240          | 15564  | 7bddff4bece9ff5879b5574fb999d573 | https://www.kernel.org/
2023/02/24 03:39:43  | 200             | 34440           | 309948 | a9b7130994d1ecc42dd2214321a3821b | https://www.microsoft.com/
```

## History

In folder history, files' name are like : "https___www.domain.com__day_month_year\@hour-minutes-seconds.html"

## CSV report

_Note: separator is comma (,)_

```
date,status,elapsed,size,md5,ip,url,error
2023/02/24 21:39:43,200,219778,56944,1fcac5ad4c19abdb45b19ecf06ccef59,142.250.74.228,https://www.google.com/,OK
2023/02/24 21:39:43,200,218240,15564,7bddff4bece9ff5879b5574fb999d573,145.40.68.75,https://www.kernel.org/,OK
2023/02/24 21:49:43,200,219778,56944,1fcac5ad4c19abdb45b19ecf06ccef59,142.250.74.228,https://www.google.com/,OK
2023/02/24 21:49:43,200,218240,15564,7bddff4bece9ff5879b5574fb999d573,145.40.68.75,https://www.kernel.org/,OK
2023/02/24 21:59:43,200,219778,56944,1fcac5ad4c19abdb45b19ecf06ccef59,142.250.74.228,https://www.google.com/,OK
2023/02/24 21:59:43,200,218240,15564,7bddff4bece9ff5879b5574fb999d573,145.40.68.75,https://www.kernel.org/,OK
```

## Rules

Reason | Color | Result/description
------ | ----- | -----------------
HTTP code = 2xx | Green | OK
HTTP code = 3xx | Yellow | Redirection
HTTP code = 4xx | Red | Resource access problem 
HTTP code = 5xx | Red |??Internal server
time_elapsed > time_response_max | Red | Page takes time to load
time_response_max/2 < time_elapsed < time_response_max | Yellow | Average time for page to load
time_elapsed < time_response_max/2 | Green | Page does not take time to load
md5 changed | Red | URL changed color from white to red
size > BIG_HTML_FILE_SIZE | Red | Size of HTML page is bigger than reference


