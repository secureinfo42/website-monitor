#!/usr/bin/env python3

from requests import session, packages
from hashlib import md5
from socket import gethostbyname
from os import popen
from time import sleep
packages.urllib3.disable_warnings()

# Timing ##########################################################################################

TIME_SLEEP=900
COUNT_MAX=1000000
try:
  TIME_SLEEP = int(argv[1])
  COUNT_MAX  = int(argv[2])
except:
  print("\nUsage: %s [timing count_max]\n" % argv[0].split('/')[-1])
  pass

# Functionz #######################################################################################

def get_date(fmt=""):
  if fmt == "":
    return( popen("date +'%Y/%m/%d, %T'").read().strip() )
  else:
    return( popen(f"date {fmt}").read().strip() )

def get_ip(url):
  hostname = url.split('://')[1].split('/')[0]
  return( gethostbyname(hostname) )

def check_availability(url,headers={}):
  s = session()
  date,status,size,elapsed,h_md5,ip,error = get_date(),"Unknown","0","0","None","Unknown",""
  html_file = url.replace(':','_').replace('/','_')
  date_file = get_date("+%d_%m_%Y@%H-%M-%S")
  html_file = f"history/{html_file}_{date_file}.html"

  try:
    r = s.get(url,headers=headers,verify=False,allow_redirects=False)
    ip = get_ip(url)
    h_md5 = str(md5(r.text.encode()).hexdigest())
    status = str(r.status_code)
    elapsed = str(r.elapsed.microseconds)
    size = len(r.text)
    open(html_file,"w").write(r.text)
    error = "OK"
  except Exception as e:
    error = e

  item = {
    'date': date,
    'status': status,
    'elapsed': elapsed,
    'size': size,
    'md5': h_md5,
    'ip': ip,
    'url': url,
    'error': error,
    'csv_data': f"{date},{status},{size},{elapsed},{h_md5},{ip},{url},{html_file},{error}"
  }
  return(item)

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


csv_header = "date,status,size,elapsed,h_md5,ip,url,html_file,error\n"
open( "report.csv","w" ).write( csv_header )

count = 0
while count < COUNT_MAX:
  count = count + 1
  for url in [ x.strip() for x in open("urls.lst").readlines() ]:
    r = check_availability(url,headers=headers)
    open( "report.csv","a" ).write( r['csv_data'] + "\n" )
  sleep(TIME_SLEEP)


