import tkinter as tk
from tkinter import messagebox
import global_state

def build_budget_screen(root, show_frame_callback, main_frame):
    frame = tk.Frame(root)

    fields = ["수입", "식비", "옷", "고정", "교통", "기타"]
    entries = {}
    value_labels = {}

    tk.Label(frame, text="예산 입력 창입니다", font=("Arial", 14)).pack(pady=10)

    def is_over_budget(field, budget_val, spend_val):
        try:
            return field != "수입" and int(spend_val) > int(budget_val)
        except:
            return False

    for field in fields:
        container = tk.Frame(frame)
        container.pack(pady=5, anchor="w")

        row = tk.Frame(container)
        row.pack(anchor="w")

        tk.Label(row, text=f"{field}:", width=6, anchor="w").pack(side="left")
        entry = tk.Entry(row, width=25)
        entry.pack(side="left")
        entries[field] = entry

        budget_val = global_state.budget_data.get(field, "없음")
        spend_val = global_state.spending_data.get(field, 0)

        label_text = f"(현재: {budget_val} / 사용: {spend_val})"
        label_color = "red" if is_over_budget(field, budget_val, spend_val) else "gray"

        label = tk.Label(container, text=label_text, fg=label_color)
        label.pack(anchor="w", padx=5)
        value_labels[field] = label

        def submit():
            for f in fields:
                val = entries[f].get().strip()
                if val != "":
                    if not val.isdigit():
                        messagebox.showerror("입력 오류", f"'{f}' 항목에는 숫자만 입력해주세요.")
                        return  # 하나라도 오류가 있으면 저장 중단
                    global_state.budget_data[f] = val

                budget_val = global_state.budget_data.get(f, "없음")
                spend_val = global_state.spending_data.get(f, 0)

                label_text = f"(현재: {budget_val} / 사용: {spend_val})"
                label_color = "red" if is_over_budget(f, budget_val, spend_val) else "gray"
                value_labels[f].config(text=label_text, fg=label_color)

            # ✅ txt 파일로 저장
            global_state.save_dict_to_txt(global_state.budget_data, "budget_data.txt")

            messagebox.showinfo("저장 완료", "예산이 저장되었습니다.")
            print("[예산 업데이트]", global_state.budget_data)

    tk.Button(frame, text="확인", command=submit).pack(pady=10)
    tk.Button(frame, text="뒤로가기", command=lambda: show_frame_callback(main_frame)).pack()

    return frame
