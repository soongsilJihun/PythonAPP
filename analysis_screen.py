# analysis_screen.py

import tkinter as tk
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import global_state


def show_analysis_window():
    window = tk.Toplevel()
    window.title("📊 소비 비교 분석")
    window.geometry("600x600")

    today = datetime.today()
    day_limit = today.day

    this_month_str = today.strftime("%Y-%m")
    last_month = today.replace(day=1) - timedelta(days=1)
    last_month_str = last_month.strftime("%Y-%m")

    # 누적 데이터 수집 함수
    def accumulate_spending(month_str):
        total = 0
        category_totals = {}
        for date_str, day_data in global_state.dated_spending.items():
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                if date.strftime("%Y-%m") == month_str and date.day <= day_limit:
                    for cat, amt in day_data.items():
                        category_totals[cat] = category_totals.get(cat, 0) + amt
                        total += amt
            except:
                continue
        return total, category_totals

    # 누적 소비 계산
    total_this, cat_this = accumulate_spending(this_month_str)
    total_last, cat_last = accumulate_spending(last_month_str)

    # UI 표시
    tk.Label(window, text=f"🟢 이번 달({this_month_str}) vs 🔵 지난 달({last_month_str})", font=("Arial", 14)).pack(pady=10)

    summary = tk.Text(window, height=20, width=65)
    summary.pack()

    summary.insert(tk.END, f"📆 {day_limit}일 기준 누적 소비 비교\n\n")
    summary.insert(tk.END, f"전체 소비:\n - 🟢 이번 달: {total_this:,}원\n - 🔵 지난 달: {total_last:,}원\n\n")

    all_categories = set(cat_this.keys()).union(cat_last.keys())
    summary.insert(tk.END, f"카테고리별 소비:\n")
    for cat in sorted(all_categories):
        this_val = cat_this.get(cat, 0)
        last_val = cat_last.get(cat, 0)
        summary.insert(tk.END, f"- {cat}: 🟢 {this_val:,}원 vs 🔵 {last_val:,}원\n")

    # 그래프 출력
    def draw_comparison_graph():
        import matplotlib
        matplotlib.rc("font", family="Malgun Gothic")
        matplotlib.rcParams["axes.unicode_minus"] = False

        categories = sorted(all_categories)
        this_vals = [cat_this.get(cat, 0) for cat in categories]
        last_vals = [cat_last.get(cat, 0) for cat in categories]

        x = range(len(categories))
        width = 0.35

        plt.figure(figsize=(10, 5))
        plt.bar([i - width/2 for i in x], last_vals, width=width, label=f"{last_month_str}", color="lightblue")
        plt.bar([i + width/2 for i in x], this_vals, width=width, label=f"{this_month_str}", color="salmon")

        plt.xticks(x, categories, rotation=45)
        plt.ylabel("원")
        plt.title(f"{day_limit}일 기준 카테고리별 소비 비교")
        plt.legend()
        plt.tight_layout()
        plt.show()

    tk.Button(window, text="📊 그래프로 비교", command=draw_comparison_graph).pack(pady=10)
    tk.Button(window, text="뒤로가기", command=window.destroy).pack(pady=10)
