import tkinter as tk
import global_state
from datetime import date

from datetime import datetime
def build_spending_screen(root, show_frame_callback, main_frame):
    frame = tk.Frame(root)
    tk.Label(frame, text="오늘 지출 창입니다", font=("Arial", 14)).pack(pady=10)

    selected_category = tk.StringVar(value="")
    selected_label = tk.Label(frame, text="선택된 카테고리: 없음")
    selected_label.pack()

    info_label = tk.Label(frame, text="", justify="left")
    info_label.pack(pady=5)

    category_frame = tk.Frame(frame)
    category_frame.pack(pady=10, fill="x")

    categories = ["식비", "옷", "고정", "교통", "기타"]

    def select_category(cat):
        selected_category.set(cat)
        update_info_label(cat)

    for idx, cat in enumerate(categories):
        row = idx // 3
        col = idx % 3
        btn = tk.Button(category_frame, text=cat, width=10,
                        command=lambda c=cat: select_category(c))
        btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    for i in range(3):
        category_frame.grid_columnconfigure(i, weight=1)

    entry_frame = tk.Frame(frame)
    entry_frame.pack(pady=10)
    tk.Label(entry_frame, text="금액:").pack(side="left")
    amount_entry = tk.Entry(entry_frame, width=15)
    amount_entry.pack(side="left")

    def update_info_label(cat):
        
        global_state.reload_all()
        today = datetime.today()
        today_str = today.date().isoformat()
        month_prefix = today.strftime("%Y-%m")

        # 이번 달 누적 소비
        monthly_total = 0
        for date_str, data in global_state.dated_spending.items():
            if date_str.startswith(month_prefix):
                monthly_total += data.get(cat, 0)

        # 오늘 소비
        today_spent = global_state.dated_spending.get(today_str, {}).get(cat, 0)

        # 예산
        budget = global_state.budget_data.get(cat, "없음")
        budget_formatted = f"{int(budget):,}" if str(budget).isdigit() else budget

        selected_label.config(text=f"선택된 카테고리: {cat}")
        info_label.config(
            text=(
                f"예산: {budget_formatted}원\n"
                f"누적 사용 금액: {monthly_total:,}원\n"
                f"오늘 사용 금액: {today_spent:,}원"
            ),
            fg="red" if str(budget).isdigit() and monthly_total > int(budget) else "black"
        )
    def submit_spending():
        category = selected_category.get()
        amount_str = amount_entry.get()
        today = date.today().isoformat()

        if not category:
            selected_label.config(text="❗ 카테고리를 선택하세요")
            return

        try:
            amount = int(amount_str)
        except ValueError:
            selected_label.config(text="❗ 금액은 숫자로 입력하세요")
            return

        prev = global_state.spending_data.get(category, 0)
        global_state.spending_data[category] = prev + amount

        if today not in global_state.dated_spending:
            global_state.dated_spending[today] = {}
        prev_today = global_state.dated_spending[today].get(category, 0)
        global_state.dated_spending[today][category] = prev_today + amount

        global_state.save_all()

        selected_label.config(
            text=f"{category}에 {amount}원 추가됨 (총: {global_state.spending_data[category]}원)"
        )
        amount_entry.delete(0, tk.END)
        update_info_label(category)

    tk.Button(frame, text="확인", command=submit_spending).pack(pady=5)
    tk.Button(frame, text="뒤로가기", command=lambda: show_frame_callback(main_frame)).pack()

    return frame
