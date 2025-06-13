import ast
import os
import json

def load_dict_from_txt(file_path):
    """
    함수명: load_dict_from_txt
    역할: 텍스트 파일로부터 문자열 형태의 딕셔너리를 읽어 실제 딕셔너리로 변환하여 반환
    매개변수:
        file_path (str): 불러올 파일 경로
    return 값:
        dict: 변환된 딕셔너리 객체 (파일이 없거나 내용이 없으면 빈 딕셔너리)
    """
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                return ast.literal_eval(content)
    return {}

def save_dict_to_txt(data, file_path):
    """
    함수명: save_dict_to_txt
    역할: 딕셔너리를 사람이 보기 좋도록 JSON 형식으로 텍스트 파일에 저장
    매개변수:
        data (dict): 저장할 딕셔너리 데이터
        file_path (str): 저장할 파일 경로
    return 값: 없음
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))

# 날짜별 지출 데이터 불러오기
dated_spending = load_dict_from_txt("dated_spending.txt")

def compute_total_spending():
    """
    함수명: compute_total_spending
    역할: 모든 날짜의 지출 내역을 합산하여 항목별 누적 사용 금액을 계산
    매개변수: 없음
    return 값:
        total (dict): 카테고리별 누적 지출 금액 딕셔너리
    """
    total = {}
    for date, day_data in dated_spending.items():
        for cat, amt in day_data.items():
            total[cat] = total.get(cat, 0) + amt
    return total

# 예산 데이터 불러오기
budget_data = load_dict_from_txt("budget_data.txt")

def save_all():
    """
    함수명: save_all
    역할: 현재 메모리 상의 예산 데이터와 지출 데이터를 각각 텍스트 파일로 저장
    매개변수: 없음
    return 값: 없음
    """
    save_dict_to_txt(budget_data, "budget_data.txt")
    save_dict_to_txt(dated_spending, "dated_spending.txt")

def reload_all():
    """
    함수명: reload_all
    역할: 텍스트 파일에서 예산 데이터와 지출 데이터를 다시 불러와 전역 변수에 갱신
    매개변수: 없음
    return 값: 없음
    """
    global budget_data, dated_spending
    budget_data = load_dict_from_txt("budget_data.txt")
    dated_spending = load_dict_from_txt("dated_spending.txt")
