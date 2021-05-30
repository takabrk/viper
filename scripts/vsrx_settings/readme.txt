VSRX Settings
Copyright@takamitu hamada
20180915
Web site : http://valkyrieviper.space

このアプリケーションは、Ubuntu系のLinuxディストリビューションでChromium Browserを使って設定マネージャーを構築した物です。オリジナルOS「Valkyrie Super Remixed Linux」用にスクリプトを書いた物であり、Xfce4 Settingsなどの既存の設定マネージャーからの置き換えを考えて開発を行っています。

◎アプリケーションのインストール
vsrx_web_uiフォルダの直下に、「install_apps」というシェルスクリプトがありますので、端末を起動させて必要となるアプリケーションをインストールしてください。一度アプリケーションをインストールしているのであれば、このシェルスクリプトを起動させる必要はありません。

$./install_apps

◎起動
$python vsrx_settings.py