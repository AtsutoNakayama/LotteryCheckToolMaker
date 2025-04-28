# modules/save_tool.py

from .constants import NUMBERS_PER_LINE

def save_as_bat_file(settings_data, filepath):
    """設定データをもとにバッチファイルを作成して保存する"""

    with open(filepath, "w", encoding="shift_jis") as f:
        # ヘッダー部分
        f.write("@echo off\n\n")
        f.write("echo 以下の設定内容で宝くじを確認します。\n")
        f.write("echo.\n")

        # 設定一覧をecho
        lines = generate_bat_text(settings_data)
        for line in lines.split("\n"):
            if line.strip():
                f.write(f"echo {line}\n")
            else:
                f.write("echo.\n")

        f.write("\n")
        f.write("echo 宝くじの番号を入力してください。\n")
        f.write(":EnterNum\n\n")
        f.write("set Num=\n")
        f.write("set /p Num=\n\n")

        # エラー時の赤色表示
        f.write("if [%Num%] == [] (\n")
        f.write("  echo \x1b[91m------------- ERROR -------------\n")
        f.write("  echo 番号が入力されていません\n")
        f.write("  echo ---------------------------------\x1b[0m\n")
        f.write("  goto :EnterNum\n")
        f.write(")\n\n")

        f.write("call :IsInteger %Num%\n")
        f.write("if %ERRORLEVEL% neq 0 (\n")
        f.write("  echo \x1b[91m------------- ERROR -------------\n")
        f.write("  echo 数値以外の文字が含まれています。\n")
        f.write("  echo ---------------------------------\x1b[0m\n")
        f.write("  goto :EnterNum\n")
        f.write(")\n\n")

        f.write("set /a Last1Digit = %Num% %% 10\n")
        f.write("set /a Last2Digit = %Num% %% 100\n\n")

        # 賞ごとの判定ロジック出力
        for idx, setting in enumerate(settings_data):
            if not setting.get("is_set"):
                continue

            label = prize_label(idx)
            judge = setting.get("judge")
            numbers = setting.get("numbers", [])

            for num in numbers:
                if judge == "完全一致":
                    f.write(f"if %Num% == {num} goto :{label}\n")
                elif judge == "下二桁一致":
                    f.write(f"if %Last2Digit% == {num} goto :{label}\n")
                elif judge == "下一桁一致":
                    f.write(f"if %Last1Digit% == {num} goto :{label}\n")

        f.write("\n")
        f.write("goto :Failed\n\n")

        # 当選時ラベル出力
        for idx, setting in enumerate(settings_data):
            if not setting.get("is_set"):
                continue

            label = prize_label(idx)
            points = setting.get("point")

            f.write(f":{label}\n")
            f.write("echo \x1b[32m=================================\n")
            f.write(f"echo {setting.get('grade')}！{points}ポイント獲得です！\n")
            f.write("echo =================================\x1b[0m\n")
            f.write("goto :EnterNum\n\n")

        # ハズレ時
        f.write(":Failed\n")
        f.write("echo 残念、ハズレです。\n")
        f.write("goto :EnterNum\n\n")

        # 数値判定ルーチン
        f.write(":IsInteger\n")
        f.write("set X=%1\n")
        f.write("if \"%X%\" equ \"\" exit /b -1\n")
        for n in range(10):
            f.write(f"if defined X set X=%X:{n}=%\n")
        f.write("if not defined X exit /b 0\n")
        f.write("exit /b -1\n")

def generate_bat_text(settings_data):
    """設定一覧をバッチファイル用に整形して返す"""

    lines = []
    for setting in settings_data:
        grade = setting.get("grade", "等級不明")
        lines.append(f"〇{grade}")

        if setting.get("is_set"):
            lines.append("・ポイント設定：")
            lines.append(f"{setting.get('point')}ポイント")
            lines.append("・判定方法設定：")
            lines.append(f"{setting.get('judge')}")
            lines.append("・当選番号設定：")
            numbers = setting.get("numbers", [])
            if numbers:
                # 5個ごとにカンマ区切り＋改行
                buffer = []
                for idx, num in enumerate(numbers, 1):
                    buffer.append(str(num))
                    if idx % NUMBERS_PER_LINE == 0:
                        lines.append(", ".join(buffer) + ",")
                        buffer = []
                if buffer:
                    lines.append(", ".join(buffer))
            else:
                lines.append("未設定")
        else:
            lines.append("設定なし")

        lines.append("")  # 空行追加

    return "\n".join(lines)

def prize_label(idx):
    """賞ごとのラベル名を返す"""
    labels = [
        "FirstPrize",
        "SecondPrize",
        "ThirdPrize",
        "FourthPrize",
        "FifthPrize",
        "SixthPrize",
    ]
    return labels[idx] if idx < len(labels) else f"Prize{idx+1}"
