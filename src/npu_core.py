# 표준 라벨 상수 정의
LABEL_CROSS = "Cross"
LABEL_X = "X"
LABEL_UNDECIDED = "UNDECIDED"
LABEL_UNKNOWN = "Unknown"


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
