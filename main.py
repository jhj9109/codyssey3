from src.controller import SimulatorController
from src.constants import Color


def main():
    app = SimulatorController()

    try:
        while True:
            print(f"{Color.HEADER}\n==============================={Color.ENDC}")
            print(f"{Color.OKBLUE} Mini NPU Simulator 메인 메뉴 {Color.ENDC}")
            print(f"{Color.HEADER}==============================={Color.ENDC}")
            print(f"{Color.OKCYAN}1. 모드 1: 사용자 수동 입력 (3x3){Color.ENDC}")
            print(f"{Color.OKCYAN}2. 모드 2: JSON 자동 평가 (data.json){Color.ENDC}")
            print(f"{Color.OKCYAN}3. 프로그램 종료{Color.ENDC}")
            print(f"{Color.HEADER}==============================={Color.ENDC}")
            choice = input(
                f"{Color.OKGREEN}원하시는 기능의 번호를 입력하세요: {Color.ENDC}"
            )

            try:
                if choice == "1":
                    app.run_manual_mode()
                elif choice == "2":
                    app.run_json_mode("data.json")
                elif choice == "3":
                    print(f"{Color.OKGREEN}프로그램을 종료합니다.{Color.ENDC}")
                    break
                else:
                    print(
                        f"{Color.FAIL}잘못된 입력입니다. 다시 선택해주세요.{Color.ENDC}"
                    )
            except (KeyboardInterrupt, EOFError):
                print(
                    f"{Color.WARNING}\n입력 인터럽트가 감지되어 모드를 종료하고 메인페이지로 돌아갑니다.{Color.ENDC}"
                )

    except (KeyboardInterrupt, EOFError):
        print(
            f"{Color.WARNING}\n입력 인터럽트가 감지되어 프로그램을 종료합니다.{Color.ENDC}"
        )


if __name__ == "__main__":
    main()
