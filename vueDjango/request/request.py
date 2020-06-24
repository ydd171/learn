import requests
url = 'http://www.cntour.cn'
strhtml = requests.get(url)
print(strhtml.text)