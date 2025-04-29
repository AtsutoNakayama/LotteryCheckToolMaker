# modules/app.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from .setting_window import SettingWindow
from .constants import VERSION, GRADE_NAMES
from .save_tool import save_as_bat_file

class LotteryApp(tk.Frame):
    """親画面（メインウィンドウ）"""

    def __init__(self, master=None):
        super().__init__(master)
        self.master.title(f"当選番号判定アプリ ver.{VERSION}")
        self.pack(fill="both", expand=True)
        self.grade_frames = []
        self.setting_windows = {}
        self.settings_data = [{"grade": grade, "is_set": False} for grade in GRADE_NAMES]
        self.create_main_screen()

    def create_main_screen(self):
        """メイン画面に等賞設定とボタン類を配置する"""
        for idx, grade in enumerate(GRADE_NAMES):
            frame = ttk.LabelFrame(self, text=grade)
            frame.pack(padx=10, pady=5, fill="x")
            self.grade_frames.append(frame)

            var = tk.StringVar(value="off")
            frame.var = var

            r1 = ttk.Radiobutton(frame, text="設定する", variable=var, value="on", command=lambda f=frame: self.update_button_state(f))
            r1.pack(side="left", padx=10)

            r2 = ttk.Radiobutton(frame, text="設定しない", variable=var, value="off", command=lambda f=frame: self.update_button_state(f))
            r2.pack(side="left", padx=10)

            button = ttk.Button(frame, text="設定", command=lambda idx=idx: self.open_setting_window(idx))
            button.pack(side="right", padx=10)
            button.state(["disabled"])
            frame.button = button

            label = ttk.Label(frame, text="", foreground="green")
            label.pack(side="right", padx=10)
            frame.status_label = label

            if self.settings_data[idx]["is_set"]:
                frame.status_label.config(text="設定済み ✅")

        # 確認ボタンとツール作成ボタンを横並びに配置
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        confirm_button = ttk.Button(button_frame, text="確認", command=self.open_confirm_window)
        confirm_button.pack(side="left", padx=5)

        create_tool_button = ttk.Button(button_frame, text="ツール作成", command=self.create_tool)
        create_tool_button.pack(side="left", padx=5)

    def update_button_state(self, frame):
        """ラジオボタン選択時に設定ボタンの有効/無効を切り替える"""
        if frame.var.get() == "on":
            frame.button.state(["!disabled"])
        else:
            frame.button.state(["disabled"])

    def open_setting_window(self, idx):
        """設定ウィンドウを開く"""
        if idx in self.setting_windows and self.setting_windows[idx].winfo_exists():
            messagebox.showwarning("警告", f"{idx+1}等賞設定はすでに開いています。")
            return
        window = SettingWindow(self, f"{idx + 1}等賞設定", idx, self.settings_data[idx])
        self.setting_windows[idx] = window

    def update_status_label(self, idx):
        """設定ボタン保存時に「設定済み ✅」を更新"""
        frame = self.grade_frames[idx]
        if self.settings_data[idx]["is_set"]:
            frame.status_label.config(text="設定済み ✅")
        else:
            frame.status_label.config(text="")

    def check_unconfigured(self):
        """設定するラジオボタンがONかつ未設定ならエラー"""
        for idx, frame in enumerate(self.grade_frames):
            if frame.var.get() == "on" and not self.settings_data[idx].get("is_set", False):
                grade_name = self.settings_data[idx]["grade"]
                messagebox.showerror("エラー", f"{grade_name}が未設定です。")
                return False
        return True

    def open_confirm_window(self):
        """確認ボタン押下時の動作"""
        if not self.check_unconfigured():
            return
        ConfirmWindow(self, self.settings_data)

    def create_tool(self):
        """ツール作成ボタン押下時の動作"""
        if not self.check_unconfigured():
            return

        filepath = filedialog.asksaveasfilename(
            title="ツール作成先を選択",
            initialfile="LotteryCheck.bat",
            defaultextension=".bat",
            filetypes=[("バッチファイル", "*.bat"), ("すべてのファイル", "*.*")]
        )

        if not filepath:
            return

        save_as_bat_file(self.settings_data, filepath)
        messagebox.showinfo("作成完了", f"ツールを作成しました！\n{filepath}")

class ConfirmWindow(tk.Toplevel):
    """確認ウィンドウ"""

    def __init__(self, master, settings_data):
        super().__init__(master)
        self.title("設定確認")
        self.geometry("600x600")

        text_area = tk.Text(self, wrap="word")
        text_area.pack(padx=10, pady=10, fill="both", expand=True)

        confirm_text = generate_settings_text(settings_data)
        text_area.insert("end", confirm_text)
        text_area.config(state="disabled")

def generate_settings_text(settings_data):
    """確認画面に表示するためのテキストを作成する"""
    lines = []
    for setting in settings_data:
        grade = setting.get("grade", "等級不明")
        lines.append(f"〇{grade}")
        if setting.get("is_set"):
            lines.append("・ポイント設定：")
            lines.append(f"{setting.get('point')}ポイント\n")
            lines.append("・判定方法設定：")
            lines.append(f"{setting.get('judge')}\n")
            lines.append("・当選番号設定：")
            numbers = setting.get("numbers", [])
            if numbers:
                for i in range(0, len(numbers), 5):
                    line = ", ".join(numbers[i:i+5])
                    lines.append(line)
                lines.append("")
            else:
                lines.append("未設定\n")
        else:
            lines.append("設定なし\n")
    return "\n".join(lines)
