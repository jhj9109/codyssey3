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


# utils.py 기존 코드 아래에 추가


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
