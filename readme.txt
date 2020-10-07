The Python application "Viper Tools"
Web site URL : http://vsrx.work
Created by takamitsu hamada

詳しいリファレンスは、http://vsrx.work/viperdocs/index.htmlで公開しています。

このアプリケーションを使うには、Pythonなどをインストールする必要があります。
「install_libraryapps」というシェルスクリプトがありますので、これを端末で起動させれば、必要なソフトウェアやライブラリをインストールします。

$ scripts/install_libraryapps

[主な機能]
・カスタムカーネルビルド機能
・APTでアプリケーションをインストールした時にエラーが発生した場合に再度正常にインストール出来るようにする機能
・競艇予想や数字選択式宝くじ予想などの機能を追加します。
・Ubuntu系LinuxディストリビューションにオリジナルのLinuxディストリビューションであるVSRXで構築しているデスクトップ環境を導入
・jsay.pyでは、OpenJtalkを使ってコンピューターを喋らせる
・tmpfs_ramdisk_slider.pyでは、tmpfsのRAMDISK量を調整
・animationSVGのフォルダにあるスクリプトで、アニメーションGIFのようなアニメーションSVG、APNGを作成
Ubuntu系Linuxディストリビューションのリマスター機能
・人工知能によって自動的に作文を行い、それを読み上げる機能
・システムのチューンアップ機能
・UNetbootinを使ってポータブルSSDにLiveUSB環境を構築
・Linux版ePSXeをインストール
・D-bus版Jackサーバを起動
・youtube-dlを使ったダウンロード機能
・VAAPI対応ffmpegとiHD Driverを使ったQSVハードウェアエンコード機能
・PulseAudio+Jack Mode、PulseAudio Modeの切り替え

◇カスタムカーネルをビルドする
Viper Toolsの「Build Custom Kernel(BMQ)」「Build Custom Kernel(MuQSS+CK1)」のボタンを押すとビルドを開始し、ビルド後はインストールします。また、端末上でのコマンド入力による実行も可能です。この機能を使う事でカスタムカーネル「VSRXカーネル」を半自動で作る事が出来ます。使い方は、エミュレータで以下のコマンドを入力して実行します。

1.zen-tuneカーネルに、Aufs・UKSM・Ubuntu・zstd・grasky's gccの各パッチを当てて、ベースとなるカスタムカーネルのソースコードを作成

$./build.sh -e base

2.BMQ版PVLカーネルをビルド

$./build.sh -e bmq

3.MuQSS版PVLカーネルをビルド

$./build.sh -e muqss

4.PREEMPT_RT版PVLカーネルをビルド

$./build.sh -e rt

◇UNetbootinを使ってポータブルSSDにLiveUSB環境を構築
$cd scripts
$./unetbootin_command

◇Linux版ePSXeをインストール
$cd scripts
$./install_epsxe

◇D-bus版Jackサーバを起動
$cd scripts
$./jack_start

◇PulseAudio+Jack Audio Connection Kitで高音質化

$cd sounds
$./hq-sounds.sh

◇APTでアプリケーションをインストールした時にエラーが発生した場合に再度正常にインストール出来るようにする機能
Viper Toolsの「Install Application fixed」ボタンを押します。


◇Ubuntu系Linuxディストリビューション対応のアプリケーションのインストール
vipertools.pyにPCSX2・ffmpeg・Virtualbox・Flash・Firefox・LaTex・R・gedaのインストール項目、Pepper Flash Pluginのアップデート項目がありますので、これらを使って、色々なソフトウェアをインストール出来ます。

◇viperクラスとメソッドを使う
必要なライブラリのインストールは、端末で以下のようにして実行します。
$python viper.py import

各種メソッドは、viper.pyを該当するスクリプトにimport文を使ってインポートして使っていきます。

◇ブラウザ機能
端末で以下のようにして起動
$cd browser
$browser.py

◇Valkyrie SRXのデスクトップ環境を構築する機能
端末から「python vipertools.py」と入力して起動して項目を選択する。

◇Valkyrie SRXの起動音声を切り替える機能
端末から「python vipertools.py」と入力して起動して項目を選択する。

◇tmpfs_ramdisk_slider.py
端末から「python vipertools.py」と入力して起動して項目を選択する。
tmpfsのRAMディスクの容量を変更出来ます。

◇コンピューターに喋らせる機能
端末から「python vipertools.py」と入力して起動して項目を選択する。

・端末を使って以下のように入力して使います。
$python viper.py jsay こんにちは string

・特定のテキストファイルを読ませる
$python viper.py jsay テキストファイル名 data

◇宝くじ予想機能
端末から「python vipertools.py」と入力して起動して項目を選択する。

◇競艇予想機能
端末から「python vipertools.py」と入力して起動して項目を選択する。
・コマンド入力で選手の登録番号を入力する事で予想を行います
$python kyotei.py 1111 2222 3333 4444 5555 6666

データベースはSQLiteを使っています。

出力された結果は、そのままでは当たらない事が多いので、3連単で選ぶ例を示しておきます。
順位はこのスクリプトで出した指数順位
・6位-2位-3位
・4位-3位-2位
・3位-2位-1位
・5位-2位-3位
・4位-2位-3位
・3位-2位-5位
・1位-5位-6位
・1位-3位−5位

◇アニメーションSVG機能
端末から「python vipertools.py」と入力して起動して項目を選択する。

1.アニメーションSVGの作成する
TumblrなどでアニメーションGIFを公開しているケースが多いですが、256色の色制限などがあります。
ベクターグラフィックスのSVGには、パラパラアニメを実現する機能が搭載されています。
これを使って、アニメーションSVGを作ることが可能です。
このPythonスクリプトは、連番になっている画像ファイルを一つのフォルダにまとめておいて、コマンドでアニメーションSVGを生成するものです。
ファイルをダウンロードした後に、zipを解凍して、中に入っているスクリプトと画像フォルダを同じ場所に設置します。
使用する画像フォーマットはJPEGです。
このスクリプトの対応OSは、シェルスクリプトが使用出来るLinuxなどのUNIX系OSです。
ここでは画像フォルダを「test」とし、出力する画像サイズは640x480とします。
速度を変更したい場合は、３つ目の引数でアニメーションの実行時間を変更します。
ここでは5秒でアニメーションが終わるように設定しています。
コマンドは以下の通りです。

$python viper.py asvg test 640 480 5

これで同じディレクトリに「test.svg」が生成されます。

２．パラパラアニメのJavaScript付きのHTMLを生成する
ahtml.pyは、パラパラアニメを行なうJavaScript付きのHTMLを生成します。
asvg.pyでは、画像ファイルをBase64に変換してSVGの中に画像データを取り込んでいますが、ahtml.pyを使いますと、一つのHTMLと画像フォルダの組み合わせでパラパラアニメを実現することができ、アニメーションSVGよりも負荷が低くなっています。
３つ目の引数は、setIntervalの時間を設定します。これを変更することでアニメーション速度を変更出来ます。
ここでは50msに設定しています。
コマンドは以下の通りです。

$python viper.py ahtml test 640 480 50

ディレクトリに「test.html」が生成されます。

3.PNG画像を一括でJPEGにする
このモードは、複数のPNG画像を一括でJPEG画像に変換する物です。
ターミナルエミュレーターで以下のコマンドを使います。
ここでは、PNG画像をまとめたフォルダを「inputdir」、JPEG画像をまとめたフォルダを「outputdir」とします。
各フォルダはスクリプトと同じディレクトリに置いてください。

$python viper.py png2jpg inputdir outputdir 640 480 80

このコマンドの意味は、「inputdirに入っているPNG画像を一括で640x480の解像度・80%の圧縮率のJPEGに変換する」というものです。

4.JPEG画像を一括で回転させて保存する
このモードは、一括でJPEG画像を任意の角度に回転させる物です。
ターミナルエミュレーターで以下のコマンドを使います。
ここでは、JPEG画像をまとめたフォルダを「inputdir」とします。
各フォルダはスクリプトと同じディレクトリに置いてください。

$python viper.py rotatejpg inputdir -90

このコマンドの意味は、「inputdirに入っているJPEG画像を一括で-90度回転させて上書き保存する」というものです。


◇音声ファイルエンコード機能
この機能には、「MP3→AAC,Ogg Vorbis(mp3aac,mp3ogg)」、「AAC→MP3,Ogg Vorbis(aacmp3,aacogg)」、「Ogg Vorbis→MP3(oggmp3)」の５方式の音声ファイルのフォーマットやコンテナをエンコードする事が出来ます。
以下のコマンドを入力して使います。

$python viper.py mp3ogg xxx 128

上の例は、xxx.mp3というファイルをOgg Vorbisで作成したxxx.oggというファイルにビットレート128kbpsで変換する事が出来ます。
Pythonモジュールであるviper.pyの後に、モード・ファイル名（拡張子含まない）・ビットレートの順に指定していきます。

ffmpegを使っていますので、Ubuntu 16.04LTSをベースにしたLinuxディストリビューションを使っている場合には、viper.pyで必要なライブラリなどをインストールする事が可能です。
この機能を使うには、以下のようにします。

$python viper.py import

◇ペネトレーションテストツールのインストール
vipertools.pyを起動させて、「Install Penatration Test」の項目にチェックをしてOKボタンを押すとインストールが可能です。
サーバなどにおいてネットワークの脆弱性を発見するのに役立つツールをインストールします。

◇Waifu2Xを使用する
waifu2x.pyをベースにしたスクリプトが組み込まれており、画像を綺麗に拡大する事が可能になります。
使い方は、「Waifu2x」ボタンを押してアプリを起動させます。
入力ファイルと出力ファイルを記載し、Modelの項目には「scale2x」「noise1」「noise2」のいずれかを指定します。

◇JPEGファイルの容量を軽量化する
Imagetoolsには、JPEGエンコーダー「Guetzli」が使えるようになっており、これを使う事でJPEGファイルを軽量化出来ます。

◇ChromiumにGoogle Chrome内蔵のWidevineを入れる
最近のGoogle Chromeには、Widevineプラグインと呼ばれるデジタル著作権管理されているコンテンツを見る為のプラグインを搭載しています。
Chromiumには搭載していないので、これをGoogle Chromeから抜き出してChromiumでも使えるようにしようという機能を搭載しています。
但し、これを使っても完全にオンデマンドサービスで公開されている映像コンテンツが視聴出来るわけではありませんので注意してください。
