from tkinter import *
from tkcalendar import Calendar
from datetime import datetime
from calendar import monthrange
import global_state
import matplotlib.pyplot as plt

def build_calendar_screen(root, show_frame_callback, main_frame, font_regular, font_bold):
    """
    함수명: build_calendar_screen
    역할: 달력 UI를 기반으로 사용자가 날짜별 소비 내역을 확인하고,
         해당 월의 소비 그래프를 출력할 수 있는 캘린더 화면을 구성
    매개변수:
        root (tk.Tk 또는 tk.Frame): 부모 
        show_frame_callback (function): 다른 화면으로 전환하는 함수
        main_frame (tk.Frame): 뒤로가기 시 전환할 메인 화면
        font_regular: 일반 텍스트용 폰트
        font_bold: 강조 텍스트용 폰트
    return 값:
        frame (tk.Frame): 구성된 캘린더 화면 프레임
    """
    frame = Frame(root)
    Label(frame, text="가계부 캘린더", font=font_bold).pack(pady=10)

    today_dt = datetime.today()
    today_str = today_dt.strftime("%Y-%m-%d")

    # 달력 위젯 생성
    cal = Calendar(frame, year=today_dt.year, month=today_dt.month,
                   selectmode='day', locale='ko_KR', date_pattern='yyyy-mm-dd')
    cal.pack()

    # 오늘 날짜 강조
    cal.calevent_create(today_dt, "오늘", "today")
    cal.tag_config("today", background="#ffeb99")

    Label(frame, text="선택 날짜 지출 내역", font=font_regular).pack(pady=5)
    detail_text = Text(frame, height=10, width=40, font=font_regular)
    detail_text.pack()

    def on_date_click(event):
        """
        함수명: on_date_click
        역할: 캘린더에서 날짜 클릭 시 해당 날짜의 지출 내역 및
             오늘일 경우 예산 분석을 텍스트로 출력
        매개변수:
            event: 캘린더 이벤트 
        return 값: 없음
        """
        selected_date = cal.get_date()
        detail_text.delete("1.0", END)

        if selected_date == today_str:
            detail_text.insert(END, f"오늘 ({selected_date}) 예산 분석:\n\n")

            last_day = monthrange(today_dt.year, today_dt.month)[1]
            remaining_days = last_day - today_dt.day + 1

            current_month = today_dt.strftime("%Y-%m")
            for category in global_state.budget_data:
                if category == "수입":
                    continue

                try:
                    budget = int(global_state.budget_data.get(category, 0))

                    monthly_spent = 0
                    for date_str, data in global_state.dated_spending.items():
                        if date_str.startswith(current_month):
                            monthly_spent += data.get(category, 0)

                    remaining = max(0, budget - monthly_spent)
                    per_day = remaining // remaining_days
                    detail_text.insert(END, f"{category}: 하루 {per_day:,}원 사용 가능 (남은 {remaining:,}원)\n")
                except:
                    continue

        if selected_date in global_state.dated_spending:
            detail_text.insert(END, f"{selected_date} 지출 내역:\n")
            for category, amount in global_state.dated_spending[selected_date].items():
                detail_text.insert(END, f"- {category}: {amount:,}원\n")
        else:
            detail_text.insert(END, f"{selected_date}: 지출 내역 없음")

    # 날짜 클릭 시 지출 내역 출력
    cal.bind("<<CalendarSelected>>", on_date_click)

    graph_btn_frame = Frame(frame)
    graph_btn_frame.pack(pady=10)

    def show_spending_graph(sort_by="amount"):
        """
        함수명: show_spending_graph
        역할: 현재 캘린더에서 보고 있는 월의 지출 내역을
             카테고리별로 정렬하여 막대그래프로 출력
        매개변수:
            sort_by (str): 정렬 기준 ("amount" 또는 "name")
        return 값: 없음
        """
        import matplotlib
        matplotlib.rc("font", family="Malgun Gothic")
        matplotlib.rcParams["axes.unicode_minus"] = False

        shown_year = cal.selection_get().year
        shown_month = cal.selection_get().month
        shown_month_str = f"{shown_year}-{str(shown_month).zfill(2)}"

        total_by_category = {}
        for date_str, day_data in global_state.dated_spending.items():
            if date_str.startswith(shown_month_str):
                for cat, amt in day_data.items():
                    total_by_category[cat] = total_by_category.get(cat, 0) + amt

        if sort_by == "amount":
            sorted_items = sorted(total_by_category.items(), key=lambda x: -x[1])
        elif sort_by == "name":
            sorted_items = sorted(total_by_category.items(), key=lambda x: x[0])
        else:
            sorted_items = total_by_category.items()

        categories = [k for k, _ in sorted_items]
        amounts = [v for _, v in sorted_items]

        plt.figure(figsize=(8, 4))
        plt.bar(categories, amounts, color="skyblue")
        plt.title(f"{shown_month_str} 카테고리별 누적 소비")
        plt.ylabel("원")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    Button(graph_btn_frame, text="누적 소비 그래프", command=lambda: show_spending_graph("amount"), font=font_regular).pack(side="left", padx=5)
    Button(graph_btn_frame, text="가나다순", command=lambda: show_spending_graph("name"), font=font_regular).pack(side="left", padx=5)

    Button(frame, text="뒤로가기", command=lambda: show_frame_callback(main_frame), font=font_regular).pack(pady=10)

    return frame
