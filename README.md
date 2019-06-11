# todoServer
[![CircleCI](https://circleci.com/gh/jadelonghans/todoServer/tree/master.svg?style=svg)](https://circleci.com/gh/jadelonghans/todoServer/tree/master)

A simple HTTP server in python3 to maintain a To Do List using GET and POST

使用言語：　python３

## 概要：
python3のHTTPServerを用いた簡単なTODO管理サービス用のhTTPサーバーである。

TODO イベントを POST で登録，GET で取得できる HTTP サーバを作成する．
データのやり取りはJSONで行う。
TODOイベントのデータはサーバーの実行中のみメインメモリ上に保存される。

## 構成：
todoserver.py: HTTPSサーバーのソースファイル
test_server.py: GET,POSTのテストを記述したソースファイル

## 仕様：


```
## API 一覧：
# イベント登録 API request
POST /api/v1/event
{"deadline": "2019-06-11T14:00:00+09:00", "title": "レポート提出", "memo": ""}

# イベント登録 API response
200 OK
{"status": "success", "message": "registered", "id": 1}

400 Bad Request
{"status": "failure", "message": "invalid date format"}
```

```
# イベント全取得 API request
GET /api/v1/event

# イベント全取得 API response
200 OK
{"events": [
    {"id": 1, "deadline": "2019-06-11T14:00:00+09:00", "title": "レポート提出", "memo": ""},
    ...
]}
```
最初のレコードがインデックス１で取得できる。
```
# イベント1件取得 API request
GET /api/v1/event/${id}

# イベント1件取得 API response
200 OK
{"id": 1, "deadline": "2019-06-11T14:00:00+09:00", "title": "レポート提出", "memo": ""}

404 Not Found
```

日付は RFC3339 形式の文字列．RFC3339 の仕様は https://tools.ietf.org/html/rfc3339#section-5.6 ご参照ください。
