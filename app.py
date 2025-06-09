# app.py

import tkinter as tk
from budget_screen import build_budget_screen
from spending_screen import build_spending_screen
from calendar_screen import build_calendar_screen
from analysis_screen import show_analysis_window
# 앱 초기화
root = tk.Tk()
root.title("가계부 앱")
root.geometry("500x700")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# 화면 전환 함수
def show_frame(f):
    f.tkraise()

# 프레임 생성
main_frame = tk.Frame(root, bg="#f8f8f8")
budget_frame = build_budget_screen(root, show_frame, main_frame)
spending_frame = build_spending_screen(root, show_frame, main_frame)
calendar_frame = build_calendar_screen(root, show_frame, main_frame)

for frame in (main_frame, budget_frame, spending_frame, calendar_frame):
    frame.grid(row=0, column=0, sticky="nsew")

# 메인 화면 구성
def build_main_screen():
    tk.Label(main_frame, text="가계부 메인화면", font=("Arial", 16)).pack(pady=30)

    tk.Button(main_frame, text="예산 입력", bg="#ff9999", fg="white", width=20,
              command=lambda: show_frame(budget_frame)).pack(pady=10)

    tk.Button(main_frame, text="오늘 지출", bg="#99ccff", fg="white", width=20,
              command=lambda: show_frame(spending_frame)).pack(pady=10)

    # ✅ 소비 분석 버튼 추가
    tk.Button(main_frame, text="소비 분석", bg="#ccccff", fg="black", width=20,
          command=show_analysis_window).pack(pady=10)

    calendar_btn = tk.Button(main_frame, text="📅", bg="#99ffcc", fg="black",
                             width=3, height=1, font=("Arial", 14), borderwidth=0,
                             command=lambda: show_frame(calendar_frame))
    calendar_btn.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

build_main_screen()
show_frame(main_frame)
root.mainloop()
