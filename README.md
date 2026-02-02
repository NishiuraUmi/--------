# 10x10 オセロ（カスタム版）

## 概要
PythonのPygameで作成した、通常より広い10x10盤面のオセロゲームです。
CPU対戦機能を搭載し、BGMや効果音による演出にもこだわりました。
.exeファイルのダウンロードは[こちら](https://drive.google.com/file/d/1Qhiyhq0bySYJqFVDWLJTVL-eVaiRthSg/view?usp=drive_link)

制作時期：2026年1月〜2月

## 機能説明
- **10x10盤面**: 通常の8x8よりも戦略性が広がるカスタムサイズ。
- **音声演出**: 石を置く音や対局中のBGMを実装。
- **配布用EXE化**: `PyInstaller`を使用し、アセットを含めて1ファイルで実行可能。

## 遊び方
このゲームはマウスのクリックのみで操作します。

### 1. タイトル画面
ゲームを起動するとタイトル画面が表示されます。
「1」キーで黒（先攻）、「2」キーで白（後攻）を選択して開始します。

<figure>
    <img src="title.png" alt="10x10オセロ タイトル画面">
    <figcaption>タイトル画面</figcaption>
</figure>

### 2. ゲーム画面
盤面をクリックして石を置きます。置ける場所には黄色いヒントが表示されます。

<figure>
    <img src="playing.png" alt="10x10オセロ プレイ中の画面">
    <figcaption>プレイング画面</figcaption>
</figure>
