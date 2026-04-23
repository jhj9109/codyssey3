from src.constants import LABEL_CROSS, LABEL_X, LABEL_UNDECIDED
from src.npu_core import mac_operation, normalize_label, compare_two_scores
from src.utils import parse_matrix_input, extract_size_from_key, validate_matrix_size


def run_phase1_tests():
    print("=== Phase 1: Core 로직 테스트 시작 ===\n")

    # 1. 라벨 정규화 테스트
    assert normalize_label("+") == LABEL_CROSS
    assert normalize_label("Cross") == LABEL_CROSS
    assert normalize_label("cross") == LABEL_CROSS
    assert normalize_label("x") == LABEL_X
    assert normalize_label("X") == LABEL_X
    print("[PASS] 1. 라벨 정규화 테스트 통과")

    # 2. MAC 연산 테스트
    cross_filter = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    x_filter = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]

    input_pattern = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]

    score_with_cross = mac_operation(input_pattern, cross_filter)
    score_with_x = mac_operation(input_pattern, x_filter)

    print(f"       -> Cross 필터 점수: {score_with_cross}")
    print(f"       -> X 필터 점수: {score_with_x}")

    assert score_with_cross == 5.0
    assert score_with_x == 1.0
    print("[PASS] 2. MAC 연산 테스트 통과")

    # 3. 점수 비교 및 판정 테스트
    result = compare_two_scores(score_with_cross, score_with_x, LABEL_CROSS, LABEL_X)
    assert result == LABEL_CROSS

    assert compare_two_scores(5.0, 5.0, LABEL_CROSS, LABEL_X) == LABEL_UNDECIDED
    assert compare_two_scores(5.0, 5.0000000001, LABEL_CROSS, LABEL_X) == LABEL_UNDECIDED
    print("[PASS] 3. 부동소수점(epsilon) 기반 판정 테스트 통과\n")

    print("=== Phase 1: 모든 코어 로직 정상 동작 확인 완료 ===")


def run_phase2_tests():
    print("\n=== Phase 2: 검증 로직 테스트 시작 ===")

    # 1. 정상 입력 테스트
    valid_input = ["1 0 1", "0 1 0", "1 0 1"]
    parsed = parse_matrix_input(valid_input, 3)
    assert parsed == [[1.0, 0.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 1.0]]
    print("[PASS] 1. 정상 입력 파싱 테스트 통과")

    # 2. 예외 처리 테스트 - 행 부족
    try:
        parse_matrix_input(["1 0 1", "0 1 0"], 3)
        assert False, "행 부족 예외가 발생해야 합니다."
    except ValueError as e:
        assert "행 개수 오류" in str(e)

    # 3. 예외 처리 테스트 - 열 부족
    try:
        parse_matrix_input(["1 0 1", "0 1", "1 0 1"], 3)
        assert False, "열 부족 예외가 발생해야 합니다."
    except ValueError as e:
        assert "열 개수 오류" in str(e)

    # 4. 예외 처리 테스트 - 문자 포함
    try:
        parse_matrix_input(["1 0 1", "0 a 0", "1 0 1"], 3)
        assert False, "숫자 파싱 예외가 발생해야 합니다."
    except ValueError as e:
        assert "숫자 파싱 오류" in str(e)

    print("[PASS] 2. 예외 발생(행/열 불일치, 문자 입력) 방어 테스트 통과")
    print("=== Phase 2: 검증 로직 정상 동작 확인 완료 ===\n")


def run_phase3_tests():
    print("\n=== Phase 3: JSON 검증 유틸리티 테스트 시작 ===")

    # 1. 크기 추출 테스트
    assert extract_size_from_key("size_5_01") == 5
    assert extract_size_from_key("size_13_test") == 13

    try:
        extract_size_from_key("invalid_key")
        assert False, "예외가 발생해야 합니다."
    except ValueError:
        pass
    print("[PASS] 1. 패턴 키에서 크기(N) 추출 테스트 통과")

    # 2. 행렬 크기 검증 테스트
    valid_3x3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    invalid_3x2 = [[1, 2, 3], [4, 5, 6]]
    invalid_3x3_with_hole = [[1, 2, 3], [4, 5], [7, 8, 9]]

    assert validate_matrix_size(valid_3x3, 3) is True
    assert validate_matrix_size(invalid_3x2, 3) is False
    assert validate_matrix_size(invalid_3x3_with_hole, 3) is False
    print("[PASS] 2. 2차원 리스트 N x N 크기/스키마 검증 테스트 통과")

    print("=== Phase 3: 검증 유틸리티 정상 동작 확인 완료 ===\n")


if __name__ == "__main__":
    run_phase1_tests()
    run_phase2_tests()
    run_phase3_tests()
