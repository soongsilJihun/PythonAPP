import tkinter as tk
import global_state
from datetime import date, datetime
import tkinter.font as tkFont
import os

def build_spending_screen(root, show_frame_callback, main_frame, font_regular, font_bold):
    """
    함수명: build_spending_screen
    역할: 오늘 지출 입력 화면을 구성하고 반환
         - 카테고리 선택, 금액 입력, 지출 정보 저장 및 시각적 정보 제공
    매개변수:
        root (tk.Tk 또는 tk.Frame): 부모 위젯
        show_frame_callback (function): 다른 화면으로 전환할 수 있는 콜백 함수
        main_frame (tk.Frame): 뒤로가기 시 전환할 메인 화면
        font_regular: 일반 폰트
        font_bold: 강조 폰트
    return 값:
        frame (tk.Frame): 구성된 지출 입력 화면
    """
    font_regular = ("SUITE", 12)
    font_bold = ("SUITE", 14, "bold")

    frame = tk.Frame(root)
    tk.Label(frame, text="오늘 지출 입력", font=font_bold).pack(pady=10)

    selected_category = tk.StringVar(value="")
    selected_label = tk.Label(frame, text="선택된 카테고리: 없음", font=font_regular)
    selected_label.pack()

    info_label = tk.Label(frame, text="", justify="left", font=font_regular)
    info_label.pack(pady=5)

    category_frame = tk.Frame(frame)
    category_frame.pack(pady=10, fill="x")

    categories = ["식비", "옷", "고정", "교통", "기타"]

    def select_category(cat):
        """
        함수명: select_category
        역할: 카테고리를 선택하면 상태를 저장하고 정보 레이블을 갱신
        매개변수:
            cat (str): 선택된 카테고리 이름
        return 값: 없음
        """
        selected_category.set(cat)
        update_info_label(cat)

    for idx, cat in enumerate(categories):
        row = idx // 3
        col = idx % 3
        btn = tk.Button(category_frame, text=cat, width=10, font=font_regular,
                        command=lambda c=cat: select_category(c))
        btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    for i in range(3):
        category_frame.grid_columnconfigure(i, weight=1)

    entry_frame = tk.Frame(frame)
    entry_frame.pack(pady=10)
    tk.Label(entry_frame, text="금액:", font=font_regular).pack(side="left")
    amount_entry = tk.Entry(entry_frame, width=15, font=font_regular)
    amount_entry.pack(side="left")

    def update_info_label(cat):
        """
        함수명: update_info_label
        역할: 선택된 카테고리의 예산, 월간 누적 지출, 오늘 지출을 화면에 표시
        매개변수:
            cat (str): 선택된 카테고리
        return 값: 없음
        """
        global_state.reload_all()
        today = datetime.today()
        today_str = today.date().isoformat()
        month_prefix = today.strftime("%Y-%m")

        monthly_total = 0
        for date_str, data in global_state.dated_spending.items():
            if date_str.startswith(month_prefix):
                monthly_total += data.get(cat, 0)

        today_spent = global_state.dated_spending.get(today_str, {}).get(cat, 0)
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
        """
        함수명: submit_spending
        역할: 입력된 금액을 현재 선택된 카테고리의 오늘 지출에 추가하고 저장
             - 입력 유효성 검사, 저장, 정보 레이블 갱신 포함
        매개변수: 없음
        return 값: 없음
        """
        category = selected_category.get()
        amount_str = amount_entry.get()
        today = date.today().isoformat()

        if not category:
            selected_label.config(text="카테고리를 선택하세요")
            return

        try:
            amount = int(amount_str)
        except ValueError:
            selected_label.config(text="금액은 숫자로 입력하세요")
            return

        if today not in global_state.dated_spending:
            global_state.dated_spending[today] = {}

        prev_today = global_state.dated_spending[today].get(category, 0)
        global_state.dated_spending[today][category] = prev_today + amount

        global_state.save_all()

        total_by_category = global_state.compute_total_spending()
        total_amount = total_by_category.get(category, 0)

        selected_label.config(
            text=f"{category}에 {amount}원 추가됨 (총: {total_amount:,}원)"
        )
        amount_entry.delete(0, tk.END)
        update_info_label(category)

    tk.Button(frame, text="확인", command=submit_spending, font=font_regular).pack(pady=5)
    tk.Button(frame, text="뒤로가기", command=lambda: show_frame_callback(main_frame), font=font_regular).pack()

    return frame
