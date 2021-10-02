# ニコニコのフォロワーのデータ収集するやつ

## 目的

- 自分がどんな人にフォローされているのか気になった
- あわよくば人気のクリエイターを見つけられたら面白い動画見つかりそうと思った

## 使い方

- 適当な場所にgit cloneする
- docker-compose up -d する
- docker-compose exec app bash でコンテナに入る
- python nico_follower_scraping.py で実行する
- 処理終了後、csvフォルダにcsvファイルが作成されるので自由に使う

なお、デフォルトではurlが設定されていないので

tmp_follower_url_list = follower_list(driver, 'https://www.nicovideo.jp/user/2090155/follow/follower?ref=pc_userpage_top')

この部分のurlを、自分がスクレイピングしたいURLに設定してから使ってください。

例：tmp_follower_url_list = follower_list(driver, 'https://www.nicovideo.jp/user/2090155/follow/follower?ref=pc_userpage_top')

ちなみにフォロワー一覧、フォロー一覧に対応してます。
ログイン処理の問題があるので、URLがmypageのものを使わないよう気をつけてください。

## 仕様

- ニコニコのフォロワー一覧表示の仕組みが特殊で、読み込み具合に応じてコンテンツが非表示になったりするので、さらに表示をするたびにユーザー一覧を読み込んでる
- さらに、そのデータを配列にappendするために都度forしている
- その結果、表示ユーザー数が増えるほど処理が重くなっている
- なにかいい方法があったら改善して使ってください
- なければ我慢して使ってください
- また取得漏れが発生しがちです。より厳密に使うのであれば、more.click()の前だけでなく後ろでも読み込むといいですが、単純に表示だけで2倍の時間がかかります。

あと、dockerでselenium回してみて思ったけど、やたら重い。（メモリ系のバグっぽい挙動もたびたびある）
よりストレスフリーに使うならいっそdocker使わないというのも手かもしれないと思った。

## wait

- スクレイピングによる負荷をかけすぎないように、アクセスごとに10秒のtime.sleepがかかるようになってます（clickは3秒だけど処理の重さの関係上、かなりのwaitが擬似的にかかってる状態）
- 必要に応じて変更するなりしてください
