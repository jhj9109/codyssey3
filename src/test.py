from npu_core import (
    mac_operation,
    normalize_label,
    compare_scores,
    LABEL_CROSS,
    LABEL_X,
    LABEL_UNDECIDED,
)


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
    result = compare_scores(score_with_cross, score_with_x)
    assert result == LABEL_CROSS

    assert compare_scores(5.0, 5.0) == LABEL_UNDECIDED
    assert compare_scores(5.0, 5.0000000001) == LABEL_UNDECIDED
    print("[PASS] 3. 부동소수점(epsilon) 기반 판정 테스트 통과\n")

    print("=== Phase 1: 모든 코어 로직 정상 동작 확인 완료 ===")


if __name__ == "__main__":
    run_phase1_tests()
