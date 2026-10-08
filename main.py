"""나만의 프롬프트 관리 프로그램 (콘솔)

프로그램 실행 중에만 데이터가 유지되며, 종료하면 초기 상태로 돌아간다.
"""

MENU_ITEMS = [
    ("1", "프롬프트 추가"),
    ("2", "프롬프트 목록"),
    ("3", "카테고리별 조회"),
    ("4", "프롬프트 검색"),
    ("5", "프롬프트 상세 보기"),
    ("6", "즐겨찾기 관리"),
    ("7", "즐겨찾기 목록"),
    ("0", "종료"),
]


def show_menu():
    """메인 메뉴를 출력한다."""
    print()
    print("=== 나만의 프롬프트 관리 ===")
    for key, label in MENU_ITEMS:
        print(f"{key}. {label}")


def main():
    while True:
        show_menu()
        choice = input("선택: ").strip()

        if choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 메뉴 번호(0~7)를 입력해주세요.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램을 종료합니다.")
