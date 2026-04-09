from src.utils import parse_matrix_input
from src.npu_core import mac_operation, compare_scores, LABEL_CROSS, LABEL_X


def get_matrix_from_user(matrix_name, size=3):
    """
    사용자로부터 N x N 크기의 행렬을 입력받습니다.
    오류 시 정상적인 값을 입력할 때까지 무한 반복합니다.
    """
    print(
        f"\n[{matrix_name}] {size}x{size} 크기로 입력해주세요. (각 줄의 숫자는 공백으로 구분)"
    )

    while True:
        lines = []
        for i in range(size):
            line = input(f"Row {i+1}: ")
            lines.append(line)

        try:
            # utils 모듈의 검증 함수 호출
            matrix = parse_matrix_input(lines, size)
            print(f"-> {matrix_name} 저장 완료!")
            return matrix
        except ValueError as e:
            # 예외 발생 시 에러 메시지 출력 후 반복문 처음(재입력)으로 돌아감
            print(f"[입력 형식 오류] {e}")
            print("다시 입력해주세요.\n")


def run_mode_1():
    """
    모드 1(사용자 입력 모드)의 전체 실행 흐름을 제어합니다.
    """
    print("\n=== 모드 1: 사용자 입력 (3x3) 시작 ===")

    # 1. 필터 A, B 입력
    filter_cross = get_matrix_from_user(f"필터 {LABEL_CROSS}", 3)
    filter_x = get_matrix_from_user(f"필터 {LABEL_X}", 3)

    # 2. 패턴 입력
    pattern = get_matrix_from_user("입력 패턴", 3)

    # 3. MAC 연산 및 판정
    print("\n=== 연산 및 판정 결과 ===")
    score_cross = mac_operation(pattern, filter_cross)
    score_x = mac_operation(pattern, filter_x)

    print(f"{LABEL_CROSS} 필터 점수: {score_cross}")
    print(f"{LABEL_X} 필터 점수: {score_x}")

    result = compare_scores(score_cross, score_x)
    print(f"최종 판정: {result}")

    # 성능 분석 출력은 Phase 4에서 상세히 연동될 예정입니다.
    print("=== 모드 1 종료 ===")


# 개별 파일 실행 테스트용
if __name__ == "__main__":
    run_mode_1()
