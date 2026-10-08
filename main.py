"""나만의 프롬프트 관리 프로그램 (콘솔)

프로그램 실행 중에만 데이터가 유지되며, 종료하면 초기 상태로 돌아간다.
"""

CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]

# 이전 미션(GenAI 기초, 멀티모달 콘텐츠, 노코드 자동화)에서 작성한 프롬프트
DEFAULT_PROMPTS = [
    {
        "title": "블로그 글 작성 도우미",
        "content": (
            "당신은 10년 경력의 전문 블로거입니다.\n"
            "주어진 주제에 대해 SEO에 최적화된 블로그 글을 작성해주세요.\n"
            "서론, 본론, 결론 구조를 갖추고,\n"
            "독자의 관심을 끄는 제목을 3개 제안해주세요."
        ),
        "category": "텍스트 생성",
        "favorite": True,
    },
    {
        "title": "제품 썸네일 생성",
        "content": (
            "흰색 배경 위에 놓인 [제품명]의 미니멀한 제품 사진,\n"
            "부드러운 스튜디오 조명, 45도 각도, 그림자는 은은하게,\n"
            "고해상도, 상업용 광고 스타일, 1:1 비율"
        ),
        "category": "이미지 생성",
        "favorite": False,
    },
    {
        "title": "30초 광고 영상 스크립트",
        "content": (
            "[제품명]을 소개하는 30초 분량의 숏폼 광고 영상 스크립트를 작성해주세요.\n"
            "장면별로 (화면 설명 / 내레이션 / 자막)을 표로 정리하고,\n"
            "첫 3초 안에 시청자의 시선을 사로잡는 훅을 넣어주세요."
        ),
        "category": "영상 생성",
        "favorite": False,
    },
    {
        "title": "IT 컨설턴트 페르소나",
        "content": (
            "당신은 중소기업의 디지털 전환을 돕는 15년 차 IT 컨설턴트입니다.\n"
            "전문 용어는 쉬운 비유로 풀어 설명하고,\n"
            "모든 답변의 마지막에는 '바로 실행할 수 있는 다음 단계' 3가지를 제시하세요."
        ),
        "category": "페르소나",
        "favorite": False,
    },
    {
        "title": "뉴스 요약 자동화",
        "content": (
            "아래 뉴스 기사를 읽고 다음 형식으로 요약해주세요.\n"
            "1) 한 줄 요약 2) 핵심 포인트 3개 3) 우리 업무에 미치는 영향\n"
            "결과는 슬랙 메시지로 바로 보낼 수 있도록 마크다운으로 작성해주세요."
        ),
        "category": "자동화",
        "favorite": True,
    },
]

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


def input_non_empty(message):
    """빈 값이 아닐 때까지 반복해서 입력받는다."""
    while True:
        value = input(message).strip()
        if value:
            return value
        print("입력값이 비어 있습니다. 다시 입력해주세요.")


def input_number(message, min_value, max_value):
    """min_value~max_value 범위의 정수를 입력받는다. 잘못된 입력이면 None을 반환한다."""
    value = input(message).strip()
    try:
        number = int(value)
    except ValueError:
        print("숫자를 입력해주세요.")
        return None
    if number < min_value or number > max_value:
        print(f"{min_value}~{max_value} 사이의 번호를 입력해주세요.")
        return None
    return number


def choose_category():
    """미리 정의된 카테고리 중 하나를 고르거나 직접 입력받는다."""
    custom_number = len(CATEGORIES) + 1
    while True:
        print("카테고리 선택:")
        for number, category in enumerate(CATEGORIES, start=1):
            print(f"{number}) {category}")
        print(f"{custom_number}) 직접 입력")

        number = input_number("선택: ", 1, custom_number)
        if number is None:
            continue
        if number == custom_number:
            return input_non_empty("카테고리 이름: ")
        return CATEGORIES[number - 1]


def add_prompt(prompts):
    """새 프롬프트를 입력받아 목록에 추가한다."""
    print("\n=== 프롬프트 추가 ===")
    title = input_non_empty("제목: ")
    content = input_non_empty("내용: ")
    print()
    category = choose_category()

    prompts.append({
        "title": title,
        "content": content,
        "category": category,
        "favorite": False,
    })
    print("\n프롬프트가 추가되었습니다!")


def print_prompt_line(number, prompt):
    """'번호. [카테고리] 제목 ⭐' 형식으로 한 줄 출력한다."""
    star = " ⭐" if prompt["favorite"] else ""
    print(f"{number}. [{prompt['category']}] {prompt['title']}{star}")


def show_list(prompts):
    """저장된 모든 프롬프트를 번호와 함께 출력한다."""
    print("\n=== 프롬프트 목록 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다. 먼저 프롬프트를 추가해주세요.")
        return

    for number, prompt in enumerate(prompts, start=1):
        print_prompt_line(number, prompt)
    print(f"\n총 {len(prompts)}개의 프롬프트")


def find_prompts(prompts, condition):
    """condition(prompt)가 참인 프롬프트를 (전체 목록 기준 번호, 프롬프트) 목록으로 반환한다.

    전체 목록 기준 번호를 유지해서, 결과에 보이는 번호를
    상세 보기/즐겨찾기 관리에 그대로 입력할 수 있게 한다.
    """
    return [
        (number, prompt)
        for number, prompt in enumerate(prompts, start=1)
        if condition(prompt)
    ]


def print_matches(matches):
    """find_prompts()의 결과를 출력한다."""
    for number, prompt in matches:
        print_prompt_line(number, prompt)


def get_all_categories(prompts):
    """기본 카테고리에 사용자가 직접 입력한 카테고리를 더한 목록을 반환한다."""
    categories = list(CATEGORIES)
    for prompt in prompts:
        if prompt["category"] not in categories:
            categories.append(prompt["category"])
    return categories


def show_by_category(prompts):
    """선택한 카테고리의 프롬프트만 출력한다."""
    print("\n=== 카테고리별 조회 ===")
    categories = get_all_categories(prompts)
    for number, category in enumerate(categories, start=1):
        print(f"{number}) {category}")

    number = input_number("선택: ", 1, len(categories))
    if number is None:
        return
    category = categories[number - 1]

    matches = find_prompts(prompts, lambda prompt: prompt["category"] == category)
    print(f"\n[{category}] 카테고리 프롬프트:")
    if not matches:
        print("이 카테고리에 등록된 프롬프트가 없습니다.")
        return
    print_matches(matches)
    print(f"\n총 {len(matches)}개의 프롬프트")


def search_prompt(prompts):
    """키워드가 제목 또는 내용에 포함된 프롬프트를 찾는다 (대소문자 무시)."""
    print("\n=== 프롬프트 검색 ===")
    keyword = input_non_empty("검색어: ").lower()

    matches = find_prompts(
        prompts,
        lambda prompt: keyword in prompt["title"].lower()
        or keyword in prompt["content"].lower(),
    )
    print("\n검색 결과:")
    if not matches:
        print("검색 결과가 없습니다.")
        return
    print_matches(matches)
    print(f"\n{len(matches)}개의 프롬프트를 찾았습니다.")


def select_prompt(prompts):
    """번호를 입력받아 해당 프롬프트를 반환한다. 잘못된 번호면 None."""
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return None
    number = input_number(f"번호 입력 (1~{len(prompts)}): ", 1, len(prompts))
    if number is None:
        return None
    return prompts[number - 1]


def show_detail(prompts):
    """선택한 프롬프트의 전체 내용을 출력한다."""
    print("\n=== 프롬프트 상세 보기 ===")
    prompt = select_prompt(prompts)
    if prompt is None:
        return

    line = "─" * 40
    print()
    print(line)
    print(f"제목: {prompt['title']}")
    print(f"카테고리: {prompt['category']}")
    print(f"즐겨찾기: {'⭐' if prompt['favorite'] else '-'}")
    print(line)
    print("내용:")
    print(prompt["content"])
    print(line)


def toggle_favorite(prompts):
    """선택한 프롬프트의 즐겨찾기 상태를 추가/해제한다."""
    print("\n=== 즐겨찾기 관리 ===")
    prompt = select_prompt(prompts)
    if prompt is None:
        return

    prompt["favorite"] = not prompt["favorite"]
    if prompt["favorite"]:
        print(f"'{prompt['title']}' 프롬프트를 즐겨찾기에 추가했습니다! ⭐")
    else:
        print(f"'{prompt['title']}' 프롬프트를 즐겨찾기에서 해제했습니다.")


def show_favorites(prompts):
    """즐겨찾기된 프롬프트만 모아서 출력한다."""
    print("\n=== 즐겨찾기 목록 ===")
    matches = find_prompts(prompts, lambda prompt: prompt["favorite"])
    if not matches:
        print("즐겨찾기한 프롬프트가 없습니다. (메뉴 6번에서 추가할 수 있습니다)")
        return
    print_matches(matches)
    print(f"\n총 {len(matches)}개의 즐겨찾기")


def show_menu():
    """메인 메뉴를 출력한다."""
    print()
    print("=== 나만의 프롬프트 관리 ===")
    for key, label in MENU_ITEMS:
        print(f"{key}. {label}")


def main():
    # 기본 데이터를 복사해서 사용한다 (프로그램 실행 중에만 유지)
    prompts = [dict(prompt) for prompt in DEFAULT_PROMPTS]

    while True:
        show_menu()
        choice = input("선택: ").strip()

        if choice == "1":
            add_prompt(prompts)
        elif choice == "2":
            show_list(prompts)
        elif choice == "3":
            show_by_category(prompts)
        elif choice == "4":
            search_prompt(prompts)
        elif choice == "5":
            show_detail(prompts)
        elif choice == "6":
            toggle_favorite(prompts)
        elif choice == "7":
            show_favorites(prompts)
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 메뉴 번호(0~7)를 입력해주세요.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램을 종료합니다.")
