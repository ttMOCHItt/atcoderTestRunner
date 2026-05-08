import requests
from bs4 import BeautifulSoup as BS
import subprocess
import sys

if len(sys.argv) < 3:
    sys.exit("使用方法：[python atCoderCheck.py <問題URL> <回答ファイル>]")

url = sys.argv[1]
target_file = sys.argv[2]

try:
    html = requests.get(url)
    html.raise_for_status()
except Exception as e:
    sys.exit(f"エラー: URLへのアクセスに失敗しました。({e})")

soup = BS(html.content, "html.parser")
h3_tags = soup.find_all("h3")

test_cases = []
temp_input = ""

for h3 in h3_tags:
    label = h3.get_text()
    
    if "Sample Input" in label:
        temp_input = h3.find_next("pre").get_text().strip() + "\n"
            
    elif "Sample Output" in label:
        temp_output = h3.find_next("pre").get_text().strip()
        test_cases.append({
            "input": temp_input,
            "output": temp_output
        })

total_cases = len(test_cases)

if total_cases == 0:
    sys.exit("エラー: 入出力例が見つかりませんでした。URLが正しいか確認してください。")

print(f"--- Loaded {total_cases} cases. Testing for [{target_file}] ---")

for i, case in enumerate(test_cases, 1):
    in_data = case["input"]
    expected = case["output"]

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
            print(f" [解答]:{expected}")
            print(f" [あなたの出力]:{actual}")
            
    except subprocess.TimeoutExpired:
        print(f"Case {i}: TLE (Timeout)")
    except Exception as e:
        print(f"Case {i}: Error: {e}")