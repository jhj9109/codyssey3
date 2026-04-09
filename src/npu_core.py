from itertools import chain
from src.constants import LABEL_CROSS, LABEL_X, LABEL_UNDECIDED, LABEL_UNKNOWN


def mac_operation(pattern, filter_matrix):
    """(순수 함수) 입력 패턴과 필터의 MAC 연산 결과를 float로 반환"""
    n = len(pattern)
    score = 0.0
    for i in range(n):
        for j in range(n):
            score += pattern[i][j] * filter_matrix[i][j]
    return score


def normalize_label(label):
    """(순수 함수) 입력 라벨을 표준 라벨로 변환하여 반환"""
    label_str = str(label).strip().lower()
    if label_str in ["+", "cross"]:
        return LABEL_CROSS
    elif label_str in ["x"]:
        return LABEL_X
    return LABEL_UNKNOWN


def compare_scores(score_cross, score_x, epsilon=1e-9):
    """(순수 함수) 오차를 고려해 판정 결과를 문자열로 반환"""
    if abs(score_cross - score_x) < epsilon:
        return LABEL_UNDECIDED
    elif score_cross > score_x:
        return LABEL_CROSS
    else:
        return LABEL_X


def mac_operation_1d(pattern_1d, filter_1d):
    """
    (보너스) 1차원 배열로 최적화된 MAC 연산을 수행합니다.
    데이터가 메모리에 연속적으로 존재하므로 캐시 히트율(Cache Hit Rate)이 높아질 수 있습니다.
    """
    n_squared = len(pattern_1d)
    score = 0.0

    # 중첩 루프(N x N)가 아닌 단일 루프(N^2) 사용

    for i in range(n_squared):
        score += pattern_1d[i] * filter_1d[i]

    return score


def mac_operation_chain(pattern, filter_matrix):

    return sum(
        p * f
        for p, f in zip(
            chain.from_iterable(pattern), chain.from_iterable(filter_matrix)
        )
    )


def mac_operation_array(flat_array, weight_array):

    n_squared = len(flat_array)
    score = 0.0
    for i in range(n_squared):
        score += flat_array[i] * weight_array[i]

    return score
