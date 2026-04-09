from src.npu_core import mac_operation, compare_scores, LABEL_CROSS, LABEL_X
from src.utils import parse_matrix_input


class SimulatorController:
    """
    시뮬레이터의 전체적인 실행 흐름과 I/O를 제어하는 컨트롤러 클래스입니다.
    """

    def __init__(self):
        pass  # 추후 모드 2를 위한 설정값이나 상태를 가질 수 있습니다.

    def _read_matrix_from_console(self, matrix_name, size):
        """콘솔 입출력을 담당하는 내부 메서드 (사이드 이펙트 격리)"""
        print(f"\n[{matrix_name}] {size}x{size} 크기로 입력해주세요. (공백 구분)")
        while True:
            lines = []
            for i in range(size):
                lines.append(input(f"Row {i+1}: "))

            try:
                # 순수 함수인 parse_matrix_input을 호출하여 로직만 분리
                matrix = parse_matrix_input(lines, size)
                print(f"-> {matrix_name} 저장 완료!")
                return matrix
            except ValueError as e:
                print(f"[입력 형식 오류] {e}\n다시 입력해주세요.\n")

    def run_manual_mode(self):
        """모드 1(수동 입력) 시나리오 진행 메서드"""
        print("\n=== 모드 1: 사용자 입력 (3x3) 시작 ===")

        # 1. 입력 단계 (I/O)
        filter_cross = self._read_matrix_from_console(f"필터 {LABEL_CROSS}", 3)
        filter_x = self._read_matrix_from_console(f"필터 {LABEL_X}", 3)
        pattern = self._read_matrix_from_console("입력 패턴", 3)

        # 2. 연산 및 판정 단계 (순수 함수 조합)
        score_cross = mac_operation(pattern, filter_cross)
        score_x = mac_operation(pattern, filter_x)
        result = compare_scores(score_cross, score_x)

        # 3. 출력 단계 (I/O)
        print("\n=== 연산 및 판정 결과 ===")
        print(f"{LABEL_CROSS} 필터 점수: {score_cross}")
        print(f"{LABEL_X} 필터 점수: {score_x}")
        print(f"최종 판정: {result}")
        print("=== 모드 1 종료 ===")


# 테스트 및 개별 실행용 진입점
if __name__ == "__main__":
    controller = SimulatorController()
    controller.run_manual_mode()
