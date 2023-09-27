1. `requests`: ウェブページを取得するためのライブラリ。

2. `Beautiful Soup 4`: HTMLとXMLの解析ライブラリ。

3. `selenium`: ウェブブラウザを制御するためのライブラリ。実際にウェブページを操作したり、スクリーンショットを取得したりする場合に使用します。
Seleniumを使用するためには、ChromeDriverをシステムにインストールしてパスを設定する必要があります。

4. `dotenv`: `.env` ファイルから環境変数を読み込むためのライブラリ。

インストールするには、以下のコマンドを実行します：
pip install requests beautifulsoup4 selenium python-dotenv


ChromeDriverのインストール
https://googlechromelabs.github.io/chrome-for-testing/#stable にアクセスして対応するものをインストールする．
例えばWindowsで用いる場合はhttps://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/116.0.5845.96/win64/chromedriver-win64.zip ここでインストールできる．
インストールして展開したらその中に入っているchromedriver.exe(これだけでOK)をこのファイルがあるディレクトリのbinにいれてください．

yahoo メールの設定．
そのままでは送信することができないので設定してください．
yahooメールは送信専用のものを作成することを推奨します．
メールボックスに行って設定を開く(右上の歯車)
IMAP/POP/SMTPアクセスを開く
Yahoo! JAPAN公式サービス以外からのアクセスも有効にする
IMAP, SMTPを有効にする
パスワードを設定していない場合は必ず設定してください．
これらの設定を行ったあとはしっかりと送信ができることを確認するために，test.pyを実行してください．

python3 test.py

c.f.
https://support.yahoo-net.jp/PccMail/s/article/H000007321
https://support.yahoo-net.jp/PccMail/s/article/H000011486

usage:
settings.envに設定を書き込む必要があります．
SEND_EMAIL=送信用のメールアドレス(必ずyahooメールにしてください．)
SEND_PASS=上のyahooメールのパスワード
RECIEVE_EMAIL=受信用のメールアドレス(こちらは任意のメールクライアントを利用できます．)
INTERVAL=何秒間隔で検査するかの指定です．例では60秒ごとに実行されます．
URL=http://www.mnetplan.com/densha.htm 検査するURLです．
SENTENCE=挿入する定型文です．

これらを設定した状態でWebPageMonitor.pyを実行すると動きます．↓

python3 WebPageMonitor.py

