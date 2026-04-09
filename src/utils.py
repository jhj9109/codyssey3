import time
import random
import array

from src.constants import LABEL_CROSS, LABEL_X


def parse_matrix_input(input_lines, expected_size):
    """
    (순수 함수) 문자열 리스트를 검증하고 2차원 float 배열로 반환.
    오류가 있으면 예측 가능한 예외(ValueError)를 던집니다.
    """
    if len(input_lines) != expected_size:
        raise ValueError(f"행 개수 오류: {expected_size}줄을 입력해야 합니다.")

    matrix = []
    for line in input_lines:
        elements = line.strip().split()
        if len(elements) != expected_size:
            raise ValueError(
                f"열 개수 오류: 각 줄에 {expected_size}개의 숫자를 입력하세요."
            )

        row = []
        for val in elements:
            try:
                row.append(float(val))
            except ValueError:
                raise ValueError(
                    "숫자 파싱 오류: 숫자(정수 또는 실수)만 입력 가능합니다."
                )
        matrix.append(row)

    return matrix


def extract_size_from_key(pattern_key):
    """
    (순수 함수) 'size_5_01' 형태의 패턴 키 문자열에서 크기(N)를 정수로 추출합니다.
    """
    try:
        parts = pattern_key.split("_")
        if len(parts) >= 2 and parts[0] == "size":
            return int(parts[1])
    except (ValueError, TypeError, AttributeError):
        pass

    raise ValueError(f"키 형식 오류: '{pattern_key}'에서 크기(N)를 추출할 수 없습니다.")


def validate_matrix_size(matrix, expected_size):
    """
    (순수 함수) JSON에서 로드한 2차원 리스트가 정확히 N x N 크기인지 검증합니다.
    (정상이면 True, 비정상이면 False 반환)
    """
    if not isinstance(matrix, list) or len(matrix) != expected_size:
        return False
    for row in matrix:
        if not isinstance(row, list) or len(row) != expected_size:
            return False
    return True


def generate_dummy_matrix(size, value=1.0):
    """
    (순수 함수) 성능 측정을 위해 N x N 크기의 임의의 실수 배열을 생성합니다.
    """
    return [[value for _ in range(size)] for _ in range(size)]


def measure_mac_performance(mac_func, pattern, filter_matrix, iterations=10):
    """
    (순수 함수) MAC 연산 함수의 순수 실행 시간을 N회 반복 측정하여 평균을 ms 단위로 반환합니다.
    I/O(입출력) 시간은 포함되지 않습니다.
    """
    total_time = 0.0

    for _ in range(iterations):
        # 파이썬에서 성능 측정에 가장 적합한 고해상도 타이머 사용
        start_time = time.perf_counter()
        mac_func(pattern, filter_matrix)
        end_time = time.perf_counter()

        total_time += end_time - start_time

    # 초(s) 단위를 밀리초(ms) 단위로 변환하여 반환
    average_time_ms = (total_time / iterations) * 1000
    return average_time_ms


def generate_cross_pattern(size):
    """(보너스) 크기 N의 십자가(Cross) 패턴을 자동 생성합니다."""
    matrix = [[0.0 for _ in range(size)] for _ in range(size)]
    mid = size // 2
    for i in range(size):
        matrix[mid][i] = 1.0  # 가로줄
        matrix[i][mid] = 1.0  # 세로줄
    return matrix


def generate_x_pattern(size):
    """(보너스) 크기 N의 X 패턴을 자동 생성합니다."""
    matrix = [[0.0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        matrix[i][i] = 1.0  # \ 방향 대각선
        matrix[i][size - 1 - i] = 1.0  # / 방향 대각선
    return matrix


def generate_filter_pattern(size, label):
    pattern = None
    if label == LABEL_CROSS:
        pattern = generate_cross_pattern(size)
    elif label == LABEL_X:
        pattern = generate_x_pattern(size)
    return pattern


def generate_random_filter_pattern(size):
    filter_options = [LABEL_CROSS, LABEL_X]
    filter_selected = random.choice(filter_options)
    return generate_filter_pattern(size, filter_selected)


def flatten_matrix(matrix):
    """(보너스) 2차원 배열을 1차원 배열(길이 N^2)로 변환합니다."""
    return [val for row in matrix for val in row]


def flatten_array(matrix):
    """(보너스) 2차원 배열을 1차원 배열(길이 N^2)로 변환합니다."""
    return array.array("d", [val for row in matrix for val in row])
