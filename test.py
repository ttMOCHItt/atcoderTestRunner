import requests
from bs4 import BeautifulSoup as BS 

url="https://atcoder.jp/contests/abc147/tasks/abc147_a"

html=requests.get(url)
soup=BS(html.content,"html.parser")

testCase=soup.find_all("pre")

l=len(testCase)
if l%2==0:
    l=l//2

for i in range (1,l,2):
    print(testCase[i].get_text())
    print(testCase[i+1].get_text())