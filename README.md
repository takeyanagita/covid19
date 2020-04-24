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
