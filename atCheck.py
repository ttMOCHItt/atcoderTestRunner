#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup as BS
import subprocess
import sys
import os
import pickle
import getpass

COOKIE_FILE = os.path.join(os.path.expanduser("~"), ".atcoder_session.pkl")


def load_session():
    session = requests.Session()
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, "rb") as f:
            session.cookies.update(pickle.load(f))
    return session


def save_session(session):
    with open(COOKIE_FILE, "wb") as f:
        pickle.dump(session.cookies, f)
    os.chmod(COOKIE_FILE, 0o600)


def login(session):
    print("コンテスト中の問題はログインしないと取得できません。AtCoderアカウントでログインします。")
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    login_page = session.get("https://atcoder.jp/login")
    soup = BS(login_page.text, "html.parser")
    csrf_input = soup.find("input", attrs={"name": "csrf_token"})
    if csrf_input is None:
        sys.exit("エラー: ログインページの取得に失敗しました。")

    res = session.post(
        "https://atcoder.jp/login",
        data={
            "username": username,
            "password": password,
            "csrf_token": csrf_input["value"],
        },
    )

    if "Sign Out" not in res.text:
        sys.exit("エラー: ログインに失敗しました。ユーザー名かパスワードを確認してください。")

    save_session(session)
    print("ログインに成功しました。")


def parse_test_cases(html_content):
    soup = BS(html_content, "html.parser")
    h3_tags = soup.find_all("h3")

    cases = []
    temp_input = ""

    for h3 in h3_tags:
        label = h3.get_text()

        if "Sample Input" in label:
            pre_tag = h3.find_next("pre")
            raw_content = pre_tag.get_text()
            lines = raw_content.splitlines()
            cleaned_lines = [line.strip() for line in lines if line.strip()]

            temp_input = "\n".join(cleaned_lines) + "\n"

        elif "Sample Output" in label:
            temp_output = h3.find_next("pre").get_text().strip()
            cases.append({
                "input": temp_input,
                "output": temp_output
            })

    return cases


if len(sys.argv) < 3:
    sys.exit("使用方法：[atcheck <問題URL> <回答ファイル>]")

url = sys.argv[1]
target_file = sys.argv[2]

session = load_session()

try:
    html = session.get(url)
    html.raise_for_status()
except Exception as e:
    sys.exit(f"エラー: URLへのアクセスに失敗しました。({e})")

if not os.path.exists(target_file):
    sys.exit(f"エラー: 指定されたファイル '{target_file}' が現在のディレクトリに見つかりません。")

test_cases = parse_test_cases(html.content)

if len(test_cases) == 0:
    answer = input("サンプルが取得できませんでした。コンテスト中で未ログインの可能性があります。ログインしますか？(y/N): ")
    if answer.lower() == "y":
        login(session)
        html = session.get(url)
        html.raise_for_status()
        test_cases = parse_test_cases(html.content)

total_cases = len(test_cases)

if total_cases == 0:
    sys.exit("エラー: 入出力例が見つかりませんでした。URLが正しいか確認してください。")


#acTest
print(f"--- Loaded {total_cases} cases. Testing for [{target_file}] ---")

for i, case in enumerate(test_cases, 1):
    in_data = case["input"]
    expected = case["output"]

    try:
        res = subprocess.run(
            [sys.executable, target_file],
            input=in_data,
            capture_output=True,
            text=True,
            timeout=2
        )
        
        actual = res.stdout.strip()
        error_msg = res.stderr.strip()

        if error_msg:
            print(f"Runtime Error: {error_msg}")
        
        try:
            actual_val=float(actual)
            expected_val=float(expected)
            if abs(actual_val-expected_val)<1e-9:
                print(f"-CASE {i}: AC")
            else:
                print(f"-CASE {i}: WA")

                print(f"[入力]:\n{in_data}")
                print(f"[期待される出力]:\n{expected}")
                print(f"[あなたの出力]:\n{actual}")
        except ValueError:
            if actual == expected:
                print(f"-CASE {i}: AC")
            else:
                print(f"-CASE {i}: WA")
                
                print(f"[入力]:\n{in_data}")
                print(f"[期待される出力]:\n{expected}")
                print(f"[あなたの出力]:\n{actual}")
            
    except subprocess.TimeoutExpired:
        print(f"Case {i}: TLE (Timeout)")
    except Exception as e:
        print(f"Case {i}: Error: {e}")