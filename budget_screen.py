import tkinter as tk
from tkinter import messagebox
import global_state
from datetime import datetime

def build_budget_screen(root, show_frame_callback, main_frame, font_regular, font_bold):
    """
    함수명: build_budget_screen
    역할: 예산 입력 화면을 생성하여 프레임으로 반환한다.
         - 각 항목별 예산 입력 창과 현재 예산/지출 현황 표시
         - 예산 저장 및 시각적 경고 제공
    매개변수:
        root (tk.Tk 또는 tk.Frame): 부모 윈도우 또는 프레임
        show_frame_callback (function): 다른 화면으로 전환하기 위한 콜백 함수
        main_frame (tk.Frame): 메인 화면 프레임 (뒤로가기 버튼에서 사용)
        font_regular: 기본 폰트 스타일
        font_bold: 제목 등에 사용하는 강조 폰트 스타일
    return 값:
        frame (tk.Frame): 구성된 예산 입력 화면 프레임
    """
    frame = tk.Frame(root)

    fields = ["수입", "식비", "옷", "고정", "교통", "기타"]  # 예산 항목
    entries = {}      # 항목별 입력창 저장
    value_labels = {} # 항목별 현재 상태 레이블 저장

    tk.Label(frame, text="예산 입력", font=font_bold).pack(pady=10)

    def is_over_budget(field, budget_val, spend_val):
        """
        함수명: is_over_budget
        역할: 특정 항목에서 예산을 초과했는지 여부를 판단
        매개변수:
            field (str): 항목 이름
            budget_val (str or int): 예산 값
            spend_val (int): 현재까지 사용한 금액
        return 값:
            bool: 초과 여부
        """
        try:
            return field != "수입" and int(spend_val) > int(budget_val)
        except:
            return False

    def calculate_monthly_spending(field):
        """
        함수명: calculate_monthly_spending
        역할: 이번 달 기준 특정 항목의 누적 사용 금액 계산
        매개변수:
            field (str): 항목 이름
        return 값:
            total (int): 이번 달 해당 항목 누적 사용 금액
        """
        now = datetime.now()
        current_month = f"{now.year}-{str(now.month).zfill(2)}"
        total = 0
        for date_str, cat_dict in global_state.dated_spending.items():
            if date_str.startswith(current_month):
                total += cat_dict.get(field, 0)
        return total

    for field in fields:
        container = tk.Frame(frame)
        container.pack(pady=5, anchor="w")

        row = tk.Frame(container)
        row.pack(anchor="w")

        # 항목명 + 입력창
        tk.Label(row, text=f"{field}:", width=6, anchor="w", font=font_regular).pack(side="left")
        entry = tk.Entry(row, width=25, font=font_regular)
        entry.pack(side="left")
        entries[field] = entry

        # 예산 및 사용 금액 표시
        budget_val = global_state.budget_data.get(field, "없음")
        spend_val = calculate_monthly_spending(field) if field != "수입" else 0

        budget_str = f"{int(budget_val):,}" if str(budget_val).isdigit() else budget_val
        spend_str = f"{spend_val:,}"

        if field == "수입":
            label_text = f"(현재: {budget_str})"
            label_color = "gray"
        else:
            label_text = f"(현재: {budget_str} / 사용: {spend_str})"
            label_color = "red" if is_over_budget(field, budget_val, spend_val) else "gray"

        label = tk.Label(container, text=label_text, fg=label_color, font=font_regular)
        label.pack(anchor="w", padx=5)
        value_labels[field] = label

    def submit():
        """
        함수명: submit
        역할: 입력된 예산을 저장하고 화면에 반영
             - 숫자 유효성 검사, 예산 파일 저장, 상태 레이블 갱신 포함
        매개변수: 없음 (외부 변수 사용)
        return 값: 없음
        """
        for f in fields:
            val = entries[f].get().strip()
            if val != "":
                if not val.isdigit():
                    messagebox.showerror("입력 오류", f"'{f}' 항목에는 숫자만 입력해주세요.")
                    return
                global_state.budget_data[f] = val

            budget_val = global_state.budget_data.get(f, "없음")
            spend_val = calculate_monthly_spending(f) if f != "수입" else 0

            budget_str = f"{int(budget_val):,}" if str(budget_val).isdigit() else budget_val
            spend_str = f"{spend_val:,}"

            if f == "수입":
                label_text = f"(현재: {budget_str})"
                label_color = "gray"
            else:
                label_text = f"(현재: {budget_str} / 사용: {spend_str})"
                label_color = "red" if is_over_budget(f, budget_val, spend_val) else "gray"

            value_labels[f].config(text=label_text, fg=label_color)

        global_state.save_dict_to_txt(global_state.budget_data, "budget_data.txt")
        messagebox.showinfo("저장 완료", "예산이 저장되었습니다.")
        print("[예산 업데이트]", global_state.budget_data)

    tk.Button(frame, text="확인", command=submit, font=font_regular).pack(pady=10)
    tk.Button(frame, text="뒤로가기", command=lambda: show_frame_callback(main_frame), font=font_regular).pack()

    return frame
