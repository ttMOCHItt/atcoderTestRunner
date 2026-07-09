# AtCoder Test Runner (atCheck)

AtCoderの問題ページから入出力例を自動でスクレイピングし、ローカルの回答コード（Python）に対してテストを実行する自動化ツールです。※ABCなどのコンテスト中に動かすにはログインが必須となります。

## 主な機能

- **自動スクレイピング**： 指定したURLからサンプルケースをメモリ上に取得
- **ファイルレス実行**： ローカルにファイルを生成せずにメモリ上でテストを実行
- **結果表示**： AC/WA/TLEの判定と、WA時には期待される出力と入力を比較表示

## セットアップ

### 1. 依存ライブラリインストール

**Windows**

```bash
pip install requests beautifulsoup4
```

**Ubuntu(Linux)**

apt経由でシステムパッケージとして入れてください（pipで直接入れようとすると`externally-managed-environment`エラーになります）。

```bash
sudo apt install python3-requests python3-bs4
```

### 2. コマンドとして登録（推奨）

どのディレクトリからでもatcheckコマンドで呼び出せるようにします。

### windowsの場合

1. スクリプトを適当なファイル（例：`C:\tools`）に保存します。
2. 同じフォルダ内に`atcheck.bat`を保存します。
3. `C:\tools` をシステムの環境変数**Path**に追加してください。

### Ubuntu(Linux)の場合

1. `atCheck.py`に実行権限を付与します。

```bash
chmod +x atCheck.py
```

2. `~/.local/bin`（無ければ作成し、`~/.bashrc`等でPATHに追加）に`atcheck`という名前でシンボリックリンクを張ります。

```bash
mkdir -p ~/.local/bin
ln -s "$(pwd)/atCheck.py" ~/.local/bin/atcheck
```

3. `~/.local/bin`がPATHに含まれているか確認します。含まれていなければ`~/.bashrc`に以下を追記して`source ~/.bashrc`してください。

```bash
export PATH="$HOME/.local/bin:$PATH"
```

4. 新しいターミナルで`atcheck <問題URL> <回答ファイル名>`が実行できれば成功です。

### 3. 実行権限の許可（Windowsで動かない場合）

Windowsの初期設定では、自作スクリプトの実行が制限されている場合があります。一般権限のPowerShellで実行した際にエラーが出る場合は、以下の手順を一度だけ実行してください。

1. 管理者権限でPowerShellを開きます。
2. 以下のコマンドを実行します。

```PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. `[Y] はい` を選択して Enter を押します。

これにより、現在のユーザーに対してローカルにある自作スクリプトの実行が許可されます。

## 使い方

回答コード（例`main.py`）があるディレクトリで、以下のコマンドを実行します。

```bash
atcheck <問題URL> <回答ファイル名>
```

### 実行例

```bash
atcheck https://atcoder.jp/contests/abc456/tasks/abc456_a main.py
```

### コンテスト中のログインについて

ABCなどコンテスト開催中は、未ログイン状態だと問題ページのサンプル入出力が取得できません。
`atcheck`実行時にサンプルが1件も取得できなかった場合、自動でログインするか確認されます。`y`と答えるとAtCoderのユーザー名・パスワードの入力を求められます（パスワードは非表示入力）。

- ログイン成功後はセッション情報が`~/.atcoder_session.pkl`に保存され、次回以降は再ログイン不要です（パスワード自体は保存されません）。
- 共有PCなど他人がログインする場合は、このファイルを削除すればログアウトできます。

```bash
rm ~/.atcoder_session.pkl
```

## 実行例の読み方

- AC：出力がサンプルと一致しました。
- WA：出力が異なります。期待される出力と実際の出力が表示されます。
- TLE：実行時間が２秒を超えました。
- Runtime Error：回答コード内でエラー（IndexErrorやValueError）が発生しました。

## 注意事項

- **python3**専用です
- 浮動小数点の誤差判定に対応していますが、WAと出る場合があります。
- AtCoderのHTML構造に大幅な変更が加えられた場合、正常に入出力例を取得できなくなる場合があります。
