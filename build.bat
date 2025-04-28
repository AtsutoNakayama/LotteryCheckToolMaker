@echo off

REM --- 実行開始メッセージ ---
echo LotteryCheckToolMaker.exe をビルド開始します...

REM --- 既存のdistフォルダを削除（クリーンビルド用、あってもなくてもOK） ---
if exist dist (
    echo dist フォルダを削除します...
    rmdir /s /q dist
)

REM --- ビルド実行 ---
pyinstaller --noconsole --onefile --name LotteryCheckToolMaker src/main.py

REM --- ビルド完了後、buildフォルダを削除 ---
if exist build (
    echo build フォルダを削除します...
    rmdir /s /q build
)

REM --- 完了メッセージ ---
echo ビルド完了！
echo /dist/LotteryCheckToolMaker.exe が作成されました。

pause
