# jantama
jantama_app

# 雀魂の点数を管理してグラフにできるよ
使った技術
- Django
- Chart.js

# 実行方法
乗っけてるファイル全部引っ張ってくる
jantamaディレクトリで py manage.py runserver
ローカル環境で実行
/jantama_app/

# 問題点
ユーザー登録しようとした時にエラー

ValueError at /jantama_app/post/create/
The Match could not be created because the data didn't validate.

# 工夫点

なるべく最小の入力でランクの増減や累計ポイントを計算するようにした

Matchモデルを登録した際に、nameが同名のUserモデルのnow_total_pointも更新

# 詰まった点

## Chart.jsが上手く表示されない
- DateオブジェクトをそのままLabelに送っていたのでダメだったっぽい
- Dateオブジェクトを文字列に変換して無事解決

# 今後の目標
3麻に対応

ユーザー登録時のエラーを無くす

コードを綺麗にする

短期で制作したので変数がわかりにくい（というか麻雀自体の点数がゴチャゴチャしててわかりにくい）

他の麻雀ゲームにも対応できるように

Bootstrapを使って見栄えをよくしたい

# 議論点

果たしてランク更新時に貰える点は累計に含めてグラフに乗せるべきか
  － おそらく難しい！
  
  - 初期点ありきのアルゴリズム
  - 最初から含めてやっちゃったので直すと滅茶苦茶時間がかかる
