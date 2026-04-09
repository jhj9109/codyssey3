from src.controller import SimulatorController


def main():
    app = SimulatorController()

    while True:
        print("\n===============================")
        print(" Mini NPU Simulator 메인 메뉴")
        print("===============================")
        print("1. 모드 1: 사용자 수동 입력 (3x3)")
        print("2. 모드 2: JSON 자동 평가 (data.json)")
        print("3. 프로그램 종료")
        print("===============================")
        choice = input("원하시는 기능의 번호를 입력하세요: ")

        if choice == "1":
            app.run_manual_mode()
        elif choice == "2":
            app.run_json_mode("data.json")
        elif choice == "3":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")


if __name__ == "__main__":
    main()
