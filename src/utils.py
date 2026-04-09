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
