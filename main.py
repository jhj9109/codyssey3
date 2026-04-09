from src.controller import SimulatorController


def main():
    # 시뮬레이터 진행을 담당하는 컨트롤러 객체 생성
    app = SimulatorController()

    # 지금은 모드 1만 실행하지만, Phase 3 이후 메뉴 선택 로직이 추가될 예정입니다.
    app.run_manual_mode()


if __name__ == "__main__":
    main()
