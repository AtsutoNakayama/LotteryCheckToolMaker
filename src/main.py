# main.py

import tkinter as tk
from modules.app import LotteryApp

if __name__ == "__main__":
    root = tk.Tk()
    app = LotteryApp(master=root)
    app.mainloop()
