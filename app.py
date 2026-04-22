import tkinter as tk
from tkinter import ttk, messagebox
import random

class LunchLotteryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("午餐抽獎機")
        self.root.geometry("400x550")
        self.root.configure(padx=20, pady=20)

        # 預先建立幾個不同地點的清單
        self.food_lists = {
            "彰師大附近": ["便當店", "學餐", "炒飯", "麵店"],
            "大肚山附近": ["小吃攤", "超商", "滷味"],
            "彰化市區": ["麥當勞", "拉麵", "火鍋", "壽司"],
            "自訂清單": []
        }
        
        # 追蹤當前選擇的地點
        self.current_place = tk.StringVar(value="彰師大附近")

        self.setup_ui()

    def setup_ui(self):
        # 1. 地點選擇區
        tk.Label(self.root, text="選擇地點清單：", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 5))
        self.place_combo = ttk.Combobox(self.root, textvariable=self.current_place, values=list(self.food_lists.keys()), state="readonly", font=("Arial", 11))
        self.place_combo.pack(fill="x", pady=(0, 15))
        self.place_combo.bind("<<ComboboxSelected>>", self.update_listbox) 

        # 2. 新增食物區
        tk.Label(self.root, text="輸入想吃的食物：", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 5))
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill="x", pady=(0, 15))
        
        self.food_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.food_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.food_entry.bind("<Return>", lambda event: self.add_food())
        
        add_btn = tk.Button(input_frame, text="加入清單", command=self.add_food)
        add_btn.pack(side="right")

        # 3. 顯示當前清單區
        tk.Label(self.root, text="目前清單內容：", font=("Arial", 12, "bold")).pack(anchor="w")
        self.listbox = tk.Listbox(self.root, font=("Arial", 11), height=8)
        self.listbox.pack(fill="both", expand=True, pady=(5, 10))

        # 4. 控制按鈕區 (清空與抽獎)
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", pady=10)
        
        clear_btn = tk.Button(btn_frame, text="一鍵刪除全部", command=self.clear_all, fg="red", font=("Arial", 10))
        clear_btn.pack(side="left")
        
        draw_btn = tk.Button(btn_frame, text="抽出午餐！", command=self.draw_food, font=("Arial", 12, "bold"))
        draw_btn.pack(side="right")

        # 5. 抽獎結果顯示區
        self.result_label = tk.Label(self.root, text="今天吃什麼？", font=("Arial", 16, "bold"), fg="#1976d2", pady=20)
        self.result_label.pack()

        # 初始化載入列表
        self.update_listbox()

    def update_listbox(self, event=None):
        """根據選擇的地點更新列表顯示"""
        self.listbox.delete(0, tk.END)
        place = self.current_place.get()
        for item in self.food_lists[place]:
            self.listbox.insert(tk.END, item)
        self.result_label.config(text="今天吃什麼？", fg="#1976d2")

    def add_food(self):
        """將輸入的食物加入當前清單"""
        food = self.food_entry.get().strip()
        if food:
            place = self.current_place.get()
            self.food_lists[place].append(food)
            self.food_entry.delete(0, tk.END)
            self.update_listbox()
        else:
            messagebox.showwarning("提示", "請先輸入食物名稱喔！")

    def clear_all(self):
        """清空當前選擇的清單"""
        place = self.current_place.get()
        if not self.food_lists[place]:
            return
            
        if messagebox.askyesno("確認", f"確定要清空「{place}」的所有食物嗎？"):
            self.food_lists[place].clear()
            self.update_listbox()
            self.result_label.config(text="清單已清空", fg="gray")

    def draw_food(self):
        """從當前清單隨機抽出一樣食物"""
        place = self.current_place.get()
        current_list = self.food_lists[place]
        
        if not current_list:
            messagebox.showwarning("提示", "清單裡面沒有食物，請先加一點進去吧！")
            return
            
        winner = random.choice(current_list)
        self.result_label.config(text=f"決定是你了：{winner}！", fg="#d32f2f")

if __name__ == "__main__":
    root = tk.Tk()
    app = LunchLotteryApp(root)
    root.mainloop()