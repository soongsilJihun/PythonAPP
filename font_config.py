from tkinter import font

def init_fonts(root):
    """
    함수명: init_fonts
    역할: 전체 애플리케이션에서 사용할 기본 폰트(font_regular)와
         강조 폰트(font_bold)를 설정하여 반환
    매개변수:
        root (tk.Tk): 폰트 객체에 연결할 루트
    return 값:
        font_regular (tkinter.font.Font): 기본 텍스트에 사용할 일반 폰트
        font_bold (tkinter.font.Font): 제목 등 강조 텍스트에 사용할 굵은 폰트
    """
    font_regular = font.Font(root=root, family="SUITE", size=12)
    font_bold = font.Font(root=root, family="SUITE", size=14, weight="bold")
    return font_regular, font_bold
