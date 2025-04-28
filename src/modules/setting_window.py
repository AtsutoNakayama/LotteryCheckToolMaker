import tkinter as tk
from tkinter import ttk, messagebox
from .constants import MAX_DIGITS_FULL, MAX_DIGITS_LAST2, MAX_DIGITS_LAST1, GRADE_NAMES, NUMBERS_PER_LINE

class SettingWindow(tk.Toplevel):
    def __init__(self, master, title, idx, saved_data):
        super().__init__(master)
        self.master = master
        self.idx = idx
        self.saved_data = saved_data or {}
        self.title(title)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.create_widgets()
        self.load_saved_data()

    def create_widgets(self):
        """ポイント設定、判定方法設定、当選番号設定を作成する"""
        frame_point = ttk.LabelFrame(self, text="ポイント設定")
        frame_point.pack(padx=10, pady=5, fill="x")

        self.point_var = tk.StringVar()
        point_entry = ttk.Entry(frame_point, textvariable=self.point_var, width=10, validate="key")
        point_entry.pack(side="left", padx=5, pady=5)
        point_entry["validatecommand"] = (self.register(self.validate_point_input), "%P")

        label_point = ttk.Label(frame_point, text="ポイント")
        label_point.pack(side="left", padx=5, pady=5)

        frame_judge = ttk.LabelFrame(self, text="判定方法設定")
        frame_judge.pack(padx=10, pady=5, fill="x")

        self.judge_var = tk.StringVar(value="完全一致")
        methods = ["完全一致", "下二桁一致", "下一桁一致"]
        for method in methods:
            r = ttk.Radiobutton(frame_judge, text=method, variable=self.judge_var, value=method, command=self.update_entries_validation)
            r.pack(side="left", padx=5)

        frame_number = ttk.LabelFrame(self, text="当選番号設定")
        frame_number.pack(padx=10, pady=5, fill="both", expand=True)

        self.entries = []
        for row in range(6):
            for col in range(NUMBERS_PER_LINE):
                entry = ttk.Entry(frame_number, width=10, validate="key")
                entry.grid(row=row, column=col, padx=5, pady=5)
                entry["validatecommand"] = (self.register(self.validate_number_input), "%P")
                entry.bind("<Return>", self.move_down)
                entry.bind("<Up>", self.move_up)
                entry.bind("<Down>", self.move_down)
                entry.bind("<Left>", self.move_left)
                entry.bind("<Right>", self.move_right)
                self.entries.append(entry)

        frame_buttons = ttk.Frame(self)
        frame_buttons.pack(padx=10, pady=10)

        btn_save = ttk.Button(frame_buttons, text="保存", command=self.save_settings)
        btn_save.pack(side="left", padx=5)

        btn_cancel = ttk.Button(frame_buttons, text="キャンセル", command=self.on_close)
        btn_cancel.pack(side="left", padx=5)

    def on_close(self):
        if self.idx in self.master.setting_windows:
            del self.master.setting_windows[self.idx]
        self.destroy()

    def load_saved_data(self):
        if not self.saved_data.get("is_set"):
            return
        self.point_var.set(self.saved_data.get("point", ""))
        self.judge_var.set(self.saved_data.get("judge", "完全一致"))
        numbers = self.saved_data.get("numbers", [])
        for idx, num in enumerate(numbers):
            if idx < len(self.entries):
                self.entries[idx].insert(0, num)

    def validate_point_input(self, value):
        if value == "":
            return True
        if len(value) > MAX_DIGITS_FULL:
            return False
        try:
            value.encode('ascii')
        except UnicodeEncodeError:
            return False
        return value.isdigit()

    def validate_number_input(self, value):
        if value == "":
            return True
        limit = self.get_current_max_digits()
        if len(value) > limit:
            return False
        try:
            value.encode('ascii')
        except UnicodeEncodeError:
            return False
        return value.isdigit()

    def get_current_max_digits(self):
        judge = self.judge_var.get()
        if judge == "完全一致":
            return MAX_DIGITS_FULL
        elif judge == "下二桁一致":
            return MAX_DIGITS_LAST2
        elif judge == "下一桁一致":
            return MAX_DIGITS_LAST1
        return MAX_DIGITS_FULL

    def update_entries_validation(self):
        limit = self.get_current_max_digits()
        for entry in self.entries:
            entry["validatecommand"] = (self.register(self.validate_number_input), "%P")
            text = entry.get()
            if text and len(text) > limit:
                entry.delete(0, tk.END)

    def move_up(self, event):
        idx = self.entries.index(event.widget)
        if idx - NUMBERS_PER_LINE >= 0:
            self.entries[idx - NUMBERS_PER_LINE].focus()
        return "break"

    def move_down(self, event):
        idx = self.entries.index(event.widget)
        if idx + NUMBERS_PER_LINE < len(self.entries):
            self.entries[idx + NUMBERS_PER_LINE].focus()
        return "break"

    def move_left(self, event):
        idx = self.entries.index(event.widget)
        if idx % NUMBERS_PER_LINE != 0:
            self.entries[idx - 1].focus()
        return "break"

    def move_right(self, event):
        idx = self.entries.index(event.widget)
        if (idx + 1) % NUMBERS_PER_LINE != 0 and (idx + 1) < len(self.entries):
            self.entries[idx + 1].focus()
        return "break"

    def save_settings(self):
        point = self.point_var.get().strip()
        judge = self.judge_var.get()

        numbers = [entry.get().strip() for entry in self.entries]
        numbers = [num for num in numbers if num]

        limit = self.get_current_max_digits()

        if not point:
            messagebox.showerror("エラー", "ポイント設定が空欄です。")
            return
        if not self.is_valid_number(point, MAX_DIGITS_FULL):
            messagebox.showerror("エラー", f"ポイント設定は半角数字{MAX_DIGITS_FULL}桁以内で入力してください。")
            return
        if not numbers:
            messagebox.showerror("エラー", "当選番号を1つ以上入力してください。")
            return
        if any(not self.is_valid_number(num, limit) for num in numbers):
            messagebox.showerror("エラー", f"当選番号は半角数字{limit}桁以内で入力してください。")
            return
        if len(numbers) != len(set(numbers)):
            messagebox.showerror("エラー", "当選番号が重複しています。")
            return

        numbers.sort(key=lambda x: int(x))

        for entry in self.entries:
            entry.delete(0, tk.END)
        for idx, num in enumerate(numbers):
            self.entries[idx].insert(0, num)

        self.master.settings_data[self.idx] = {
            "grade": GRADE_NAMES[self.idx],
            "is_set": True,
            "point": point,
            "judge": judge,
            "numbers": numbers
        }

        self.master.update_status_label(self.idx)

        messagebox.showinfo("保存完了", f"{self.title()}の設定を保存しました。")
        self.on_close()

    def is_valid_number(self, value, limit):
        if value == "":
            return False
        if len(value) > limit:
            return False
        try:
            value.encode('ascii')
        except UnicodeEncodeError:
            return False
        return value.isdigit()
