import requests
from bs4 import BeautifulSoup as BS 
import subprocess 

string=input().split(" ")
print(string)
url=string[0]
target_file=string[1]

html=requests.get(url)
soup=BS(html.content,"html.parser")

testCase=soup.find_all("pre")

l=len(testCase)
if l%2==0:
    l=l//2

for i in range (1,l,2):
    print(testCase[i].get_text())
    print(testCase[i+1].get_text())
    
    caseNum=(i+1)//2

    in_path="in"+str(caseNum)+".txt"
    f_in=open(in_path,"w")
    f_in.write(testCase[i].get_text())
    f_in.close()

    out_path="out"+str(caseNum)+".txt"
    f_out=open(out_path,"w")
    f_out.write(testCase[i+1].get_text())
    f_out.close()
print(f"Loaded {l} test cases. Starting tests for {target_file}...\n")

for i in range(1, l ):
    with open(f"in{i}.txt", "r") as f:
        in_data = f.read()
    with open(f"out{i}.txt", "r") as f:
        expected = f.read().strip()

    try:
        res = subprocess.run(
            ["python", target_file],
            input=in_data,
            capture_output=True,
            text=True,
            timeout=2
        )
        
        actual = res.stdout.strip()

        if actual == expected:
            print(f"Case {i}: AC")
        else:
            print(f"Case {i}: WA")
            print(f"  [Expected]: {expected}")
            print(f"  [Actual]:   {actual}")
            
    except subprocess.TimeoutExpired:
        print(f"Case {i}: TLE")
    except Exception as e:
        print(f"Case {i}: Error: {e}")