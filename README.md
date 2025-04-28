# LotteryCheckToolMaker

宝くじ番号を入力して、当選判定とポイント獲得を管理するバッチファイル作成ツールです。  
TkinterベースのGUIアプリから簡単にバッチファイル(.bat)を作成できます。

---

## プロジェクト概要

- Python (Tkinter) 製のGUIツール
- 1等賞〜6等賞の賞設定
- 当選番号入力、ポイント設定、判定方法選択（完全一致/下二桁一致/下一桁一致）
- 保存時に当選番号の空欄詰め・昇順ソート
- バッチファイル(.bat)出力（Shift-JIS、色付きエラーメッセージ対応）
- PyInstallerビルド用スクリプト完備
- GitHub運用基準に準拠（developブランチ開発、featureブランチ運用）
- テスト仕様書・証跡ファイル完備（/tests/IT/管理）

---

## ファイル構成

```
LotteryCheckToolMaker/
├── src/
│   ├── main.py
│   └── modules/
│       ├── __init__.py
│       ├── app.py
│       ├── setting_window.py
│       ├── constants.py
│       └── save_tool.py
├── dist/
│   └── LotteryCheckToolMaker.exe（ビルド後）
├── tests/
│   ├── IT/
│   │   ├── 結合テスト仕様書/
│   │   │   ├── TestSpec_LotteryCheckToolMaker_v1.xlsx
│   │   │   └── Evidence_LotteryCheckToolMaker_v1.xlsx
│   │   └── 実施結果/
│   │       └── YYYYMMDD/
│   │           ├── TestSpec_LotteryCheckToolMaker_v1_YYYYMMDD.xlsx
│   │           └── Evidence_LotteryCheckToolMaker_v1_YYYYMMDD.xlsx
│   └── UT/（将来追加予定）
├── build.bat
├── README.md
├── LICENSE
└── .gitignore
```

---

## セットアップ方法

### 必要環境

- Windows 10 / 11
- Python 3.10 以上
- pipでpyinstallerがインストールされていること

```
pip install pyinstaller
```

---

## ビルド方法

### 1. Pythonがインストールされていることを確認

```
pip install pyinstaller
```

### 2. ビルド手順

- プロジェクトルートにある `build.bat` をダブルクリックしてください
- 自動で以下を実行します
  - src/main.py をビルド
  - /dist/LotteryCheckToolMaker.exe を生成
  - 不要なbuild/フォルダを削除

### 3. 完成物

- /dist/LotteryCheckToolMaker.exe が作成されます
- これを配布・利用できます

---

## テスト仕様書・証跡ファイル運用ルール

### 仕様書格納

```
/tests/IT/結合テスト仕様書/
    ├── TestSpec_LotteryCheckToolMaker_v1.xlsx
    └── Evidence_LotteryCheckToolMaker_v1.xlsx
```

### 実施結果保存

- テスト実施時に `/tests/IT/実施結果/YYYYMMDD/` を作成
- 結合テスト仕様書・証跡ファイルをコピー
- ファイル名に実施日 (YYYYMMDD) を付加する

```
TestSpec_LotteryCheckToolMaker_v1_YYYYMMDD.xlsx
Evidence_LotteryCheckToolMaker_v1_YYYYMMDD.xlsx
```

※将来、担当者名を付加する運用も可能（例：_YYYYMMDD_中山）

---

## ブランチ運用方針

- 開発ブランチ：`develop`
- 機能開発ブランチ：`feature/○○`
- リリース時のみ：`main`ブランチへ統合
- 版数管理：自然数（v1, v2, v3, ...）

---

## リリース方法

1. GitHubリポジトリの「Release」タブをクリック
2. 「Draft a new release（新しいリリースを作成）」を選択
3. 入力項目
   - Tag version：例）v1
   - Release title：例）初回リリース
   - Description：任意でリリース内容を記載
4. `/dist/LotteryCheckToolMaker.exe` を添付
5. 「Publish release」ボタンで公開

---

## ライセンス

MIT License

```
MIT License

Copyright (c) 2025 Atsuto Nakayama

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
