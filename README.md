# 動画圧縮ツール(dougaayuku)

iPhoneで録画した動画を、Claudeにアップロードできるサイズ(30MB以下)に圧縮するブラウザツールです。

**公開URL: https://mameogalaxy.github.io/dougaayuku/**

## 特徴

- **インストール不要** — ブラウザで開くだけ。iPhoneのSafariでもPCでも動きます
- **完全にプライベート** — 動画はサーバーに送信されず、すべて端末内で処理されます
- **かんたん** — 動画を選んで目標サイズ(10 / 20 / 28 MB)を選ぶだけ
- **音声のみ抽出** — 動画から音声だけを切り出してダウンロードすることもできます(iPhoneでは .m4a / AAC)
- **音声を動画に合成** — 音声が消えてしまった動画に、音声ファイルを付け直せます(編集で無音になった動画+抽出しておいた音声、など)
- **日本語文字起こし(SRT)** — 抽出した音声をGoogle Colab上のfaster-whisperでタイムスタンプ付きSRTに変換できます([ノートブックを開く](https://colab.research.google.com/github/mameogalaxy/dougaayuku/blob/main/transcribe_colab.ipynb))。PCなら `transcribe.py` でも同じことができます(`pip install faster-whisper` して `python transcribe.py 音声ファイル`)
- 再エンコードにより位置情報などのメタデータも取り除かれます

## 使い方

1. https://mameogalaxy.github.io/dougaayuku/ を開く
2. 「動画を選択」をタップして、圧縮したい動画を選ぶ
3. 目標サイズと解像度を選んで「圧縮を開始」
4. 完了したら「ダウンロード」で保存
5. Claudeの📎(添付)からダウンロードしたファイルを選んでアップロード

> **注意:** 圧縮は動画を再生しながら行うため、動画の長さと同じくらいの時間がかかります。処理中は画面を開いたままにしてください。

## 仕組み

`<video>` 要素でハードウェアデコードした映像を Canvas に描画し、`MediaRecorder` で指定ビットレートに再エンコードします。ビットレートは「目標サイズ ÷ 動画の長さ」から自動計算されます。外部ライブラリ・外部通信は一切ありません(index.html 1ファイルのみ)。

## デプロイ

`main` ブランチへの push で GitHub Actions が自動的に GitHub Pages へデプロイします(`.github/workflows/deploy-pages.yml`)。
