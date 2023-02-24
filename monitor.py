#!/usr/bin/env python3

from sys import argv, exit
from requests import session, packages
from hashlib import md5
from socket import gethostbyname
from os import popen, system
from time import sleep
from socket import timeout
from csv import DictWriter
from colorama import Fore as c
from os import getcwd,chdir
packages.urllib3.disable_warnings()

# Timing ##########################################################################################

TIME_SLEEP=900
COUNT_MAX=1000000
WEB_TIMEOUT=45
TIME_RESPONSE_MAX=1500000
MD5_HISTORY = {}

# Functionz #######################################################################################

def usage(errcode=0):
  print("\nUsage: %s [-T timing] [-c count_max] [-t timeout] [-o report.csv] [-f urls.lst] [-H]\n" % argv[0].split('/')[-1])
  print("Defaults:")
  print(" -T 900 = timing 900 seconds")
  print(" -c 1000000 = at least a whole day")
  print(" -t 45 = 45 timeout per request")
  print(" -o report.csv = default output file is report.csv")
  print(" -f urls.lst = default input file is report.csv")
  print(" -H          = save (or not) history in html files under folder history of current dir")
  print("\nExemples:")
  print("%s")
  print("%s -f urls.lst")
  print("%s -f urls.lst -t 45 -o url_stats.csv -f url_file-list.txt -c 100 -T 60")
  exit(errcode)

def get_date(fmt=""):
  if fmt == "":
    return( popen("date +'%Y/%m/%d %T'").read().strip() )
  else:
    return( popen(f"date {fmt}").read().strip() )

def md5sum(mixed):
  return( str(md5(mixed.encode()).hexdigest()) )

def get_ip(url):
  hostname = url.split('://')[1].split('/')[0]
  return( gethostbyname(hostname) )

def perror(errtxt,errcode):
  print(f"\nError: {errtxt}")
  if errcode:
    exit(errcode)

def load_urls(infile):
  try:
    return([
      x.strip() for x in open(infile).readlines()
    ])
  except:
    perror(f"unable to read file '{infile}'",2)

def display(r,url,what="",time_response_max=""):
  global MD5_HISTORY
  color_status  = ""
  color_elapsed = c.CYAN
  color_date    = c.BLUE
  color_reset   = c.RESET
  color_url     = c.WHITE
  time_response_max = int(time_response_max)
  if what == "head":
    system("clear")
    print("%-20s | %-15s | %-15s | %-6s | %-32s | %s" % ('date', 'status', 'elapsed', 'size', 'md5', 'url'))
    print("%-20s | %-15s | %-15s | %-6s | %-32s | %s" % ('-'*20, '-'*15, '-'*15, '-'*6, '-'*32, '-'*50))
  if what == "data":
    if r['status'][0] == '2':
      color_status = c.GREEN
    if r['status'][0] == '3':
      color_status = c.YELLOW
    if r['status'][0] == '4':
      color_status = c.RED
    if r['status'][0] == '5':
      color_status = c.MAGENTA
    if int(r['elapsed']) > time_response_max:
      color_elapsed = c.RED
    if time_response_max/2 < int(r['elapsed']) < time_response_max:
      color_elapsed = c.RED
    if time_response_max/4 < int(r['elapsed']) < time_response_max/2:
      color_elapsed = c.GREEN
    if url in MD5_HISTORY:
      if len(MD5_HISTORY[url]) != 1:
        color_url = c.RED

    print(f"{color_date}%-20s{color_reset} | {color_status}%-15s{color_reset} | {color_elapsed}%-15s{color_reset} | {color_elapsed}%-6s{color_reset} | %-32s | {color_url}%s{color_reset}" % (get_date() , r['status'] , r['elapsed'] , r['size'] , r['md5'], url))

def csv_write(results,outfile,what=""):
  if what == "head":
    f = open(outfile,"w")
    w = DictWriter(f,results.keys())
    w.writeheader()
  else:
    f = open(outfile,"a")
    w = DictWriter(f,results.keys())
    w.writerow(results)
  f.close()

def save_file(outfile,data):
  try:
    open(outfile,"w").write(data)
  except:
    perror(f"unable to write history file '{outfile}'",3)

def struct(date="",status="",elapsed="",size="",hmd5="",ip="",url="",err=""):
  return({
    'date': date,
    'status': status,
    'elapsed': elapsed,
    'size': size,
    'md5': hmd5,
    'ip': ip,
    'url': url,
    'error': err,
  })

def check_availability(url,headers,save_history):
  global MD5_HISTORY
  s = session()
  date,status,size,elapsed,h_md5,ip,error = get_date(),"Unknown","0","0","None","Unknown",""
  html_file = url.replace(':','_').replace('/','_')
  date_file = get_date("+%d_%m_%Y@%H-%M-%S")
  html_file = f"history/{html_file}_{date_file}.html"

  try:
    r = s.get(url,headers=headers,verify=False,allow_redirects=False)
    ip = get_ip(url)
    h_md5 = md5sum(r.text)
    status = str(r.status_code)
    elapsed = str(r.elapsed.microseconds)
    size = len(r.text)
    if url not in MD5_HISTORY:
      MD5_HISTORY[url] = []
    if h_md5 not in MD5_HISTORY[url]:
      MD5_HISTORY[url].append(h_md5)
    if save_history == True:
      save_file(html_file,r.text)
    error = "OK"
  except Exception as e:
    error = e

  return(struct(date,status,elapsed,size,h_md5,ip,url,error))

# Headers #########################################################################################

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
  'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
  'Accept-Encoding': 'gzip, deflate, br',
  'Connection': 'keep-alive',
  'Upgrade-Insecure-Requests': '1',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'cross-site',
  'sec-ch-ua-platform': 'Windows',
  'sec-ch-ua': 'Google Chrome";v="98", "Chromium";v="98", "Not=A?Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'Pragma': 'no-cache',
  'Cache-Control': 'no-cache',
}

# Main ############################################################################################

### Args ##########################################################################################

timing,count_max,socket_timeout,time_response_max = TIME_SLEEP,COUNT_MAX,WEB_TIMEOUT,TIME_RESPONSE_MAX
url_list,csv_report = "urls.lst","report.csv"
save_history = False

i = 0
while i < len(argv[1:]):
  i = i + 1
  if argv[i] == "-T":
    timing = argv[i+1]
    i = i + 1
  elif argv[i] == "-c":
    count_max = argv[i+1]
    i = i + 1
  elif argv[i] == "-t":
    socket_timeout = argv[i+1]
    i = i + 1
  elif argv[i] == "-o":
    csv_report = argv[i+1]
    i = i + 1
  elif argv[i] == "-f":
    urls_file = argv[i+1]
    i = i + 1
  elif argv[i] == "-a":
    time_response_max = argv[i+1]
    i = i + 1
  elif argv[i] == '-H':
    save_history = True
  else:
    print(argv[i])
    usage()

### Monitoring ####################################################################################

timeout(socket_timeout)

r, count = struct(), 0
csv_write(r,csv_report,"head")

chdir(getcwd())
while count < COUNT_MAX:
  count = count + 1
  display(r,"-","head",time_response_max)
  url_list = load_urls(urls_file)
  try:
    for url in url_list:
      r = check_availability(url,headers,save_history)
      display(r,url,"data",time_response_max)
      csv_write(r,csv_report)
    sleep(int(timing))
  except KeyboardInterrupt:
    perror("user abort operation.",130)

