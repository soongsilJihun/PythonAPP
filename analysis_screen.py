import tkinter as tk
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import global_state

def build_analysis_screen(root, show_frame_callback, main_frame, font_regular, font_bold):
    """
    함수명: build_analysis_screen
    역할: 이번 달과 지난 달의 소비를 비교 분석하는 화면을 구성하여 반환
         - 요약 텍스트와 비교 그래프 기능 포함
    매개변수:
        root (tk.Tk 또는 tk.Frame): 부모 
        show_frame_callback (function): 다른 화면으로 전환하는 함수
        main_frame (tk.Frame): 뒤로가기 시 전환할 메인 화면
        font_regular: 일반 텍스트용 폰트
        font_bold: 강조 텍스트용 폰트
    return 값:
        frame (tk.Frame): 구성된 소비 분석 화면 프레임
    """
    if font_regular is None: font_regular = ("SUITE", 12)
    if font_bold is None: font_bold = ("SUITE", 14, "bold")

    frame = tk.Frame(root)

    today = datetime.today()
    day_limit = today.day

    this_month_str = today.strftime("%Y-%m")
    last_month = today.replace(day=1) - timedelta(days=1)
    last_month_str = last_month.strftime("%Y-%m")

    def accumulate_spending(month_str):
        """
        함수명: accumulate_spending
        역할: 특정 월에 해당하는 날짜별 소비 데이터를 누적하여 총합과 항목별 합계를 계산
        매개변수:
            month_str (str): "yyyy-mm" 형식의 대상 월 문자열
        return 값:
            total (int): 해당 월의 전체 지출 합계
            category_totals (dict): 항목별 누적 지출 딕셔너리
        """
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

    total_this, cat_this = accumulate_spending(this_month_str)
    total_last, cat_last = accumulate_spending(last_month_str)
    all_categories = set(cat_this.keys()).union(cat_last.keys())

    tk.Label(frame, text=f"{day_limit}일 기준 소비 비교 분석", font=font_bold).pack(pady=10)
    tk.Label(frame, text=f"이번 달({this_month_str}) vs 지난 달({last_month_str})",
             font=font_regular).pack()

    summary = tk.Text(frame, height=20, width=70, font=font_regular)
    summary.pack(pady=10)

    summary.insert(tk.END, f"{day_limit}일 기준 누적 소비 비교\n\n")
    summary.insert(tk.END, f"전체 소비:\n - 이번 달: {total_this:,}원\n - 지난 달: {total_last:,}원\n\n")

    summary.insert(tk.END, f"카테고리별 소비:\n")
    for cat in sorted(all_categories):
        this_val = cat_this.get(cat, 0)
        last_val = cat_last.get(cat, 0)
        summary.insert(tk.END, f"- {cat}: 이번 달 {this_val:,}원 vs 지난 달 {last_val:,}원\n")

    def draw_comparison_graph():
        """
        함수명: draw_comparison_graph
        역할: 이번 달과 지난 달의 항목별 지출 금액을 막대그래프로 시각화
        매개변수: 없음
        return 값: 없음
        """
        import matplotlib
        matplotlib.rc("font", family="Malgun Gothic")
        matplotlib.rcParams["axes.unicode_minus"] = False

        categories = sorted(all_categories)
        this_vals = [cat_this.get(cat, 0) for cat in categories]
        last_vals = [cat_last.get(cat, 0) for cat in categories]

        x = range(len(categories))
        width = 0.35

        plt.figure(figsize=(10, 5))
        plt.bar([i - width/2 for i in x], last_vals, width=width, label=last_month_str, color="lightblue")
        plt.bar([i + width/2 for i in x], this_vals, width=width, label=this_month_str, color="salmon")

        plt.xticks(x, categories, rotation=45)
        plt.ylabel("원")
        plt.title(f"{day_limit}일 기준 카테고리별 소비 비교")
        plt.legend()
        plt.tight_layout()
        plt.show()

    tk.Button(frame, text="그래프로 비교", command=draw_comparison_graph,
              font=font_regular).pack(pady=5)
    tk.Button(frame, text="뒤로가기", command=lambda: show_frame_callback(main_frame),
              font=font_regular).pack(pady=5)

    return frame
