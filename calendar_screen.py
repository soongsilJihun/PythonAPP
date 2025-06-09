from tkinter import *
from tkcalendar import Calendar
from datetime import datetime
from calendar import monthrange
import global_state
import matplotlib.pyplot as plt


def build_calendar_screen(root, show_frame_callback, main_frame):
    frame = Frame(root)
    Label(frame, text="🗕️ 이보다 남은 예산 분석", font=("Arial", 14)).pack(pady=10)

    today_dt = datetime.today()
    today_str = today_dt.strftime("%Y-%m-%d")

    cal = Calendar(frame, year=today_dt.year, month=today_dt.month,
                   selectmode='day', locale='ko_KR', date_pattern='yyyy-mm-dd')
    cal.pack()

    # 오늘 날짜 강조
    cal.calevent_create(today_dt, "오늘", "today")
    cal.tag_config("today", background="#ffeb99")

    Label(frame, text="💸 선택 날짜 지출 내역", font=("Arial", 12)).pack(pady=5)
    detail_text = Text(frame, height=10, width=40)
    detail_text.pack()

    def on_date_click(event):
        selected_date = cal.get_date()
        detail_text.delete("1.0", END)

        if selected_date == today_str:
            detail_text.insert(END, f"📆 오늘 ({selected_date}) 예산 분석:\n\n")

            last_day = monthrange(today_dt.year, today_dt.month)[1]
            remaining_days = last_day - today_dt.day + 1

            for category in global_state.budget_data:
                if category == "수입":
                    continue

                try:
                    budget = int(global_state.budget_data.get(category, 0))
                    spent = global_state.spending_data.get(category, 0)
                    remaining = max(0, budget - spent)
                    per_day = remaining // remaining_days
                    detail_text.insert(END, f"🟢 {category}: 하루 {per_day:,}\uc6d0 \uc0ac용 가능 (남은 {remaining:,}\uc6d0)\n")
                except:
                    continue
            return

        if selected_date in global_state.dated_spending:
            detail_text.insert(END, f"🗓 {selected_date} 지출 내역:\n")
            for category, amount in global_state.dated_spending[selected_date].items():
                detail_text.insert(END, f"- {category}: {amount:,}\uc6d0\n")
        else:
            detail_text.insert(END, f"🗓 {selected_date}: 지출 내역 없음")

    cal.bind("<<CalendarSelected>>", on_date_click)

    # 그래프 보기 버튼 + 정렬 옵션
    graph_btn_frame = Frame(frame)
    graph_btn_frame.pack(pady=10)

    def show_spending_graph(sort_by="amount"):
        import matplotlib
        matplotlib.rc("font", family="Malgun Gothic")
        matplotlib.rcParams["axes.unicode_minus"] = False

        # 1. 현재 캘린더에서 보고 있는 년/월 정보 가져오기
        shown_year = cal.selection_get().year
        shown_month = cal.selection_get().month
        shown_month_str = f"{shown_year}-{str(shown_month).zfill(2)}"

        # 2. 해당 월의 데이터만 필터링
        total_by_category = {}
        for date_str, day_data in global_state.dated_spending.items():
            if date_str.startswith(shown_month_str):  # 예: "2025-06"
                for cat, amt in day_data.items():
                    total_by_category[cat] = total_by_category.get(cat, 0) + amt

        # 3. 정렬 방식에 따른 정렬
        if sort_by == "amount":
            sorted_items = sorted(total_by_category.items(), key=lambda x: -x[1])
        elif sort_by == "name":
            sorted_items = sorted(total_by_category.items(), key=lambda x: x[0])
        else:
            sorted_items = total_by_category.items()

        # 4. 그래프 출력
        categories = [k for k, _ in sorted_items]
        amounts = [v for _, v in sorted_items]

        plt.figure(figsize=(8, 4))
        plt.bar(categories, amounts, color="skyblue")
        plt.title(f"{shown_month_str} 카테고리별 누적 소비")
        plt.ylabel("원")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    Button(graph_btn_frame, text="📊 누적 소비 그래프", command=lambda: show_spending_graph("amount")).pack(side="left", padx=5)
    Button(graph_btn_frame, text="🔤 가나다순", command=lambda: show_spending_graph("name")).pack(side="left", padx=5)

    Button(frame, text="뒤로가기", command=lambda: show_frame_callback(main_frame)).pack(pady=10)
    return frame
