# covid19
covid19データと解析ツール
厚生労働省の報道発表資料ページからコピペしたデータ，というか文書を元に，数値処理可能なデータへ編集，視覚化に必要なツール類を作成している．
厚生労働省データが中心だが，東京都が公表しているでーたも合わせて使用する．
今後，その他の道府県で有用なデータが見つかれば，それらも含めていく．
データは日々追加されていく．ツールも必要に応じて追加していく．

2020/04/23 昨日の更新について．cd KouRouData して，
sed -e 'y/、（）：０１２３４５６７８９/,():0123456789/' \
kourouKanjaDay.dat > kourouKanjaDayHankaku.dat
とした．
これで厚労省報道発表資料からのコピペに含まれる邪魔な全角文字を半角へ変換した．
変換結果がkourouKanjaDayHankaku.datである．

2020/04/23 2月18日 和歌山県の行の不具合を修正．

2020/04/24 bin/zen2hanを追加．KouRouData/kourouKanjaDay.dat中の邪魔な全角文字を
半角へ変換する目的で作成したperlスクリプト．bin/zen2han < KouRouData/kouとすれば，変換後のデータが標準出力へ
出力される．
KouRouData/kourouKanjaDayHankaku.datを削除した．
kourouKanjaDay.datへ4月21, 22, 23日公表分を追加した．Dataディレクトリを作成し，
bin/zen2han < KouRouData/kourouKanjaDay.dat > Data/kourouKanjaDayHankaku.dat
とした．

2020/04/25 binへgetPrefDiff,getPrefDiffPlt,getZenkokuDiffのスクリプトを置いた．
前2者はコマンドライン引数で指定した都道府県の各日の感染者数を出力する．
元データに感染者数ゼロのレコードは無いが，グラフ表示等を考慮し感染者数0を
挿入した．getPrefDiffPlt出力の第2項目は2020年1月1日を基点とした通算日，
第3項目は患者，無症状感染者，陽性者の合計である．
getZenkokuDiffは各都道府県の合計感染者．
これらはkourouKanjaDay.datを標準入力から読むことを想定するが，
環境変数KOUROUDATAでkourouKanjaDay.datの格納ディレクトリを指定すれば
標準入力へデータを与える必要はない．
例えば，
export KOUROUDATA=$HOME/covid19work/KouRouData
としておけば，
getPrefDiff 埼玉県
のようにすればよい．

2020/04/26 bin/へgetZenDeathDiff, getZenDeathDiffPlt, getZenDeathSum7を追加．
厚労省4月25日公表分を追加．
getZenDeathSum7は各通算日以前7日間の死亡者合計値のリストを標準出力へ出力．
使用法は他と同じ．

2020/04/27 bin/へgetZenkokuSum7を追加．感染者数の各通算日以前7日間の合計値を
リストする．4月26日公表分データを追加．

2010/05/01 4月27,28,29,30日公表分データを追加．
PCR検査人数のデータをData/PCRinspection.datとして追加．データ・ソースは
https://www.mhlw.go.jp/content/10906000/000626145.pdf である．
これは逐次(不定期?)掲載されていくようだが，過去のの発表データが修正(改変?)
されることがあるので要注意．このファイルは，
https://www.mhlw.go.jp/stf/newpage_11104.html にあるリンクである．
pdfファイルからの転写であるので，誤記があったらご容赦ください．

2020/05/02 今までは厚生労働省公式発表データを扱ってきたが，東京都は感染者データをCSVファイルで提供しているので，東京都についてはこのファイルを使えば細かい解析が可能かと考えていたのだが甘かった．このファイルはスカである．まず死亡者の情報が皆無．他にテーブルがあるかと探したが無い．それなら厚労省データを用いたほうがいいだろう．東京都公表データで価値があるのはPCRの検査数データ．これのみ．

2020/05/08 pythonで書いたコード(deathDiff.py, infectDiff.py, sum7.py)をbin/へ．
厚労省データも5月6日までを追加．
pythonで書いたスクリプト中で使用する市町村名を記述したファイル`shichoson.db`を`KouRouData/`へ．

