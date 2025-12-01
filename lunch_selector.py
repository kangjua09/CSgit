import json
import os
import random

DATA_FILE = "menu_data.json"

def get_initial_data():
    return [
        {"name": "순대국밥", "category": "한식", "price": 9000, "is_spicy": True, "has_soup": True},
        {"name": "짜장면", "category": "중식", "price": 7000, "is_spicy": False, "has_soup": False},
        {"name": "돈까스", "category": "일식", "price": 11000, "is_spicy": False, "has_soup": False},
        {"name": "파스타", "category": "양식", "price": 14000, "is_spicy": False, "has_soup": True},
        {"name": "매운 짬뽕", "category": "중식", "price": 10000, "is_spicy": True, "has_soup": True},
        {"name": "비빔밥", "category": "한식", "price": 8500, "is_spicy": False, "has_soup": False},
        {"name": "라면", "category": "기타", "price": 5000, "is_spicy": True, "has_soup": True}
    ]

def load_data():
    if not os.path.exists(DATA_FILE):
        print(f"데이터 파일({DATA_FILE})이 없습니다. 초기 데이터를 생성합니다.")
        data = get_initial_data()
        save_data(data)
        return data
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(f"데이터 로드 중 오류 발생: {e}. 초기 데이터를 사용합니다.")
        data = get_initial_data()
        save_data(data)
        return data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_user_input(prompt, options, input_type=str):
    while True:
        print(prompt)
        for idx, option in enumerate(options):
            print(f"{idx + 1}. {option}")
        try:
            choice = input(">>> 입력: ")
            if not choice.isdigit():
                raise ValueError("숫자만 입력해 주세요.")
            choice = int(choice)
            if 1 <= choice <= len(options):
                if input_type == int:
                    return choice
                return options[choice - 1]
            else:
                print("메뉴 번호 범위 내에서 선택해 주세요.")
        except ValueError as e:
            print(f"잘못된 입력입니다. {e}")
        except Exception:
            print("알 수 없는 오류가 발생했습니다.")

def filter_menus(data):
    print("\n[Step 1] 어떤 종류를 드시겠습니까?")
    category_options = ["한식", "중식", "일식", "양식", "기타", "전체"]
    selected_category = get_user_input("", category_options)

    print("\n[Step 2] 가격대는 어떠신가요?")
    price_options = ["1만원 이하 (가성비)", "상관없음 (플렉스)"]
    selected_price_option = get_user_input("", price_options)
    max_price = 10000 if selected_price_option == "1만원 이하 (가성비)" else float('inf')

    print("\n[Step 3] 오늘 특별히 땡기는 게 있나요?")
    feature_options = ["국물 필수", "매운 거", "심플한 거", "없음"]
    selected_feature = get_user_input("", feature_options)

    candidates = data

    if selected_category != "전체":
        candidates = [menu for menu in candidates if menu["category"] == selected_category]

    candidates = [menu for menu in candidates if menu["price"] <= max_price]

    if selected_feature == "국물 필수":
        candidates = [menu for menu in candidates if menu.get("has_soup", False)]
    elif selected_feature == "매운 거":
        candidates = [menu for menu in candidates if menu.get("is_spicy", False)]
    elif selected_feature == "심플한 거":
        candidates = [menu for menu in candidates if not menu.get("is_spicy", True) and not menu.get("has_soup", True)]

    return candidates

def recommend_menu(data):
    print("\n................................................")
    print("[검색 중...] 조건 필터링 시작!")
    candidates = filter_menus(data)
    print(f"[검색 중...] 조건 필터링 완료! (후보 {len(candidates)}개)")
    print("................................................")

    if not candidates:
        print("\n!!! 조건에 맞는 식당이 없습니다. !!!")
        print("조건을 다시 설정하거나 맛집 추가 메뉴를 이용해 주세요.")
        return

    final_choice = random.choice(candidates)
    
    tags = []
    tags.append(f"#{final_choice['category']}")
    tags.append("#가성비" if final_choice['price'] <= 10000 else "#플렉스")
    if final_choice.get("has_soup"):
        tags.append("#국물")
    if final_choice.get("is_spicy"):
        tags.append("#매콤")

    print("\n★ 오늘의 추천 메뉴 ★")
    print(f"식당명: [ {final_choice['name']} ]")
    print(f"가격: {final_choice['price']:,}원")
    print(f"특징: {' '.join(tags)}")

    while True:
        feedback = input("마음에 드시나요? (Y/N): ").strip().upper()
        if feedback in ('Y', 'N'):
            if feedback == 'Y':
                print("즐거운 점심시간 되세요! 초기 화면으로 돌아갑니다.")
            else:
                print("아쉽네요. 다음엔 더 좋은 메뉴를 추천해 드릴게요.")
            break
        else:
            print("Y 또는 N으로만 입력해 주세요.")

def add_new_menu(data):
    print("\n================= 🍽️ 신규 맛집 추가 🍽️ =================")
    
    while True:
        name = input("1. 식당 이름: ").strip()
        if name:
            break
        print("식당 이름은 필수 입력입니다.")

    category_options = ["한식", "중식", "일식", "양식", "기타"]
    category = get_user_input("2. 카테고리를 선택하세요:", category_options)
    
    while True:
        try:
            price_input = input("3. 가격 (숫자만 입력): ").strip()
            price = int(price_input)
            if price <= 0:
                raise ValueError
            break
        except ValueError:
            print("올바른 가격(양의 정수)을 숫자로 입력해 주세요.")

    while True:
        is_spicy_input = input("4. 메뉴가 매운가요? (Y/N): ").strip().upper()
        if is_spicy_input in ('Y', 'N'):
            is_spicy = True if is_spicy_input == 'Y' else False
            break
        print("Y 또는 N으로만 입력해 주세요.")

    while True:
        has_soup_input = input("5. 국물이 있나요? (Y/N): ").strip().upper()
        if has_soup_input in ('Y', 'N'):
            has_soup = True if has_soup_input == 'Y' else False
            break
        print("Y 또는 N으로만 입력해 주세요.")

    new_menu = {
        "name": name,
        "category": category,
        "price": price,
        "is_spicy": is_spicy,
        "has_soup": has_soup
    }
    
    data.append(new_menu)
    save_data(data)
    print(f"\n✨ {name} 맛집이 성공적으로 추가 및 저장되었습니다! (총 {len(data)}개)")

def main():
    menu_data = load_data()
    print(f"데이터 파일({DATA_FILE}) 로드 완료! (총 {len(menu_data)}개 맛집)")

    while True:
        print("\n================================================")
        print("[ SMART LUNCH SELECTOR ]")
        print("================================================")
        print("1. 메뉴 추천받기")
        print("2. 맛집 추가하기")
        print("3. 종료")
        print("================================================")

        try:
            choice = input("[입력] 1-3번중 메뉴를 선택하세요 : ").strip()
            
            if choice == '1':
                recommend_menu(menu_data)
            elif choice == '2':
                add_new_menu(menu_data)
            elif choice == '3':
                print("프로그램을 종료합니다.")
                break
            else:
                print("1, 2, 3 중 하나를 입력해 주세요.")
        except KeyboardInterrupt:
            print("\n프로그램을 강제 종료합니다.")
            break
        except Exception:
            print("알 수 없는 오류가 발생했습니다. 다시 시도해 주세요.")

if __name__ == "__main__":
    main()