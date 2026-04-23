from itertools import chain
from src.constants import EPSILON, LABEL_A, LABEL_B, LABEL_CROSS, LABEL_X, LABEL_UNDECIDED, LABEL_UNKNOWN


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


def is_close(score_a, score_b, epsilon=EPSILON):
    """(순수 함수) 부동소수점으로 인한 오차이내 같은것으로 판정"""
    return abs(score_a - score_b) < epsilon


def compare_two_scores(score_a, score_b, label_a, label_b, tie_label=LABEL_UNDECIDED, epsilon=EPSILON):
    """(순수 함수) 오차를 고려해 판정 결과를 문자열로 반환"""
    if is_close(score_a, score_b, epsilon):
        return tie_label
    elif score_a > score_b:
        return label_a
    else:
        return label_b
    

def get_best_match(scores_dict: dict, tie_label=LABEL_UNDECIDED, epsilon=EPSILON):
    """
    (순수 함수) 딕셔너리로 전달된 여러 점수 중 최고점을 찾고 해당 라벨을 반환합니다.
    최고점과 epsilon 이내의 점수가 2개 이상이면 tie_label을 반환합니다.
    
    Args:
        scores_dict (dict): {'라벨명': 점수} 형태의 딕셔너리
        tie_label (str): 동점일 경우 반환할 라벨
        epsilon (float): 부동소수점 오차 허용 범위
    """
    if not scores_dict:
        return tie_label

    max_score = max(scores_dict.values())
    
    top_labels = [
        label for label, score in scores_dict.items() 
        if is_close(max_score, score, epsilon)
    ]

    if len(top_labels) > 1:
        return tie_label
    else:
        return top_labels[0]


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
