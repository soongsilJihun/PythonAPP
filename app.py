# app.py

import tkinter as tk
from budget_screen import build_budget_screen         # 예산 입력 화면 구성 함수
from spending_screen import build_spending_screen     # 지출 입력 화면 구성 함수
from calendar_screen import build_calendar_screen     # 캘린더 화면 구성 함수
from analysis_screen import build_analysis_screen     # 소비 분석 화면 구성 함수

from font_config import init_fonts  # 폰트 설정 모듈 (글꼴 불러오기)

# 앱 초기화
root = tk.Tk()
root.title("가계부 앱")
root.geometry("500x700")
root.grid_rowconfigure(0, weight=1)     # 세로 방향 비율 설정
root.grid_columnconfigure(0, weight=1)  # 가로 방향 비율 설정

# 폰트 초기화 (모든 화면에 전달할 수 있도록 전역 변수로 저장)
font_regular, font_bold = init_fonts(root)

# 화면 전환용 함수 정의
def show_frame(f):
    """
    함수명: show_frame
    역할: 특정 프레임(f)을 현재 화면 위로 올려서 표시
    매개변수:
        f (tk.Frame): 보여줄 프레임 객체
    반환값: 없음
    """
    f.tkraise()

# 프레임 생성 (각 화면을 미리 생성해둠)
main_frame = tk.Frame(root, bg="#f8f8f8")  # 메인 화면 (홈 화면)
budget_frame = build_budget_screen(root, show_frame, main_frame, font_regular, font_bold)
spending_frame = build_spending_screen(root, show_frame, main_frame, font_regular, font_bold)
calendar_frame = build_calendar_screen(root, show_frame, main_frame, font_regular, font_bold)
analysis_frame = build_analysis_screen(root, show_frame, main_frame, font_regular, font_bold)

# 프레임들을 화면에 등록
for frame in (main_frame, budget_frame, spending_frame, calendar_frame, analysis_frame):
    frame.grid(row=0, column=0, sticky="nsew")

# 메인화면 UI 구성 함수
def build_main_screen():
    """
    함수명: build_main_screen
    역할: 앱의 메인 메뉴 화면 UI 구성 (버튼 및 제목 배치)
    매개변수: 없음 (전역 변수들을 활용)
    반환값: 없음 (main_frame에 위젯들을 직접 배치함)
    """
    tk.Label(main_frame, text="가계부 메인화면", font=font_bold).pack(pady=30)

    # 예산 입력 버튼
    tk.Button(main_frame, text="예산 입력", bg="#ff9999", fg="white", width=20,
              command=lambda: show_frame(budget_frame), font=font_regular).pack(pady=10)

    # 오늘 지출 버튼
    tk.Button(main_frame, text="오늘 지출", bg="#99ccff", fg="white", width=20,
              command=lambda: show_frame(spending_frame), font=font_regular).pack(pady=10)

    # 소비 분석 버튼
    tk.Button(main_frame, text="소비 분석", bg="#ccccff", fg="black", width=20,
              font=font_regular, command=lambda: show_frame(analysis_frame)).pack(pady=10)

    # 캘린더 버튼 (오른쪽 상단 위치)
    calendar_btn = tk.Button(main_frame, text="📅", bg="#99ffcc", fg="black",
                             width=3, height=1, font=font_bold, borderwidth=0,
                             command=lambda: show_frame(calendar_frame))
    calendar_btn.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

# 메인화면 실행
build_main_screen()

# 처음에 보여줄 화면 지정 (메인 화면)
show_frame(main_frame)

# 이벤트 루프 시작
root.mainloop()
