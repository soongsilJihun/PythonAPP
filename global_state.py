import ast
import os
import json

# 파일에서 딕셔너리 불러오기
def load_dict_from_txt(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                return ast.literal_eval(content)
    return {}

# 딕셔너리를 보기 좋게 파일에 저장하기 (줄바꿈 적용)
def save_dict_to_txt(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))

# 예산 데이터 (budget_data.txt)
budget_data = load_dict_from_txt("budget_data.txt")

# 사용 지출 데이터 (spending_data.txt)
spending_data = load_dict_from_txt("spending_data.txt")

# 날짜별 지출 데이터 (dated_spending.txt)
dated_spending = load_dict_from_txt("dated_spending.txt")

# 저장 인터페이스: 각 dict 변경 시 이 함수들 호출할 것
def save_all():
    save_dict_to_txt(budget_data, "budget_data.txt")
    save_dict_to_txt(spending_data, "spending_data.txt")
    save_dict_to_txt(dated_spending, "dated_spending.txt")

# 최신 상태 다시 불러오기 (UI 업데이트용)
def reload_all():
    global budget_data, spending_data, dated_spending
    budget_data = load_dict_from_txt("budget_data.txt")
    spending_data = load_dict_from_txt("spending_data.txt")
    dated_spending = load_dict_from_txt("dated_spending.txt")
