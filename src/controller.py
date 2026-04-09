import json

from src.npu_core import (
    mac_operation,
    compare_scores,
    normalize_label,
    LABEL_CROSS,
    LABEL_X,
)
from src.utils import (
    parse_matrix_input,
    extract_size_from_key,
    validate_matrix_size,
    generate_dummy_matrix,
    measure_mac_performance,
)


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

    def _print_performance_table(self, sizes):
        """(내부 메서드) 주어진 크기 배열에 대한 성능 측정 결과를 표 형태로 출력합니다."""
        print("\n=== 성능 분석 리포트 (Time Complexity: O(N^2)) ===")
        print(f"{'크기(NxN)':<15} | {'연산 횟수(N^2)':<15} | {'평균 시간(ms)':<15}")
        print("-" * 52)

        for size in sizes:
            # 평가를 위한 더미 데이터 생성
            dummy_pattern = generate_dummy_matrix(size, 1.5)
            dummy_filter = generate_dummy_matrix(size, 0.5)

            # 10회 반복 측정 (utils 모듈의 함수 사용)
            avg_time = measure_mac_performance(
                mac_operation, dummy_pattern, dummy_filter, 10
            )
            operations = size * size

            # 소수점 6자리까지 표기하여 미세한 시간 차이도 볼 수 있게 함
            print(f"{f'{size}x{size}':<13} | {operations:<14} | {avg_time:.6f} ms")
        print("-" * 52)

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

        # [추가된 부분] 모드 1 요구사항: 3x3 크기에 대한 성능 분석 출력
        self._print_performance_table([3])
        print("=== 모드 1 종료 ===")

    def run_json_mode(self, file_path="data.json"):
        """모드 2(JSON 파일 자동 평가) 시나리오 진행 메서드"""
        print(f"\n=== 모드 2: JSON 파일 분석 ({file_path}) 시작 ===")

        # 1. 파일 로드 방어 로직
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"[오류] '{file_path}' 파일을 찾을 수 없습니다.")
            return
        except json.JSONDecodeError:
            print(f"[오류] '{file_path}' 파일이 올바른 JSON 형식이 아닙니다.")
            return

        filters_data = data.get("filters", {})
        patterns_data = data.get("patterns", {})

        pass_count = 0
        fail_count = 0
        fail_details = []

        # 2. 패턴별 반복 평가
        for pattern_key, pattern_info in patterns_data.items():
            print(f"\n[Case: {pattern_key}] 평가 중...")

            # 개별 케이스 단위로 예외를 잡아 프로그램 중단을 방지
            try:
                # 크기(N) 추출 및 데이터 매칭
                size_n = extract_size_from_key(pattern_key)
                filter_key = f"size_{size_n}"

                if filter_key not in filters_data:
                    raise ValueError(
                        f"해당 크기의 필터({filter_key})가 JSON에 존재하지 않습니다."
                    )

                filter_cross = filters_data[filter_key].get("cross")
                filter_x = filters_data[filter_key].get("x")
                pattern_input = pattern_info.get("input")
                expected_raw = pattern_info.get("expected")

                if None in (filter_cross, filter_x, pattern_input, expected_raw):
                    raise ValueError(
                        "데이터 일부(input, expected, cross, x)가 누락되었습니다."
                    )

                # 스키마 및 크기 검증
                if not validate_matrix_size(
                    filter_cross, size_n
                ) or not validate_matrix_size(filter_x, size_n):
                    raise ValueError(
                        f"필터 배열 크기가 {size_n}x{size_n} 규칙에 어긋납니다."
                    )
                if not validate_matrix_size(pattern_input, size_n):
                    raise ValueError(
                        f"입력 패턴 배열 크기가 {size_n}x{size_n} 규칙에 어긋납니다."
                    )

                # 라벨 정규화
                expected_label = normalize_label(expected_raw)

                # MAC 연산 및 판정
                score_cross = mac_operation(pattern_input, filter_cross)
                score_x = mac_operation(pattern_input, filter_x)
                result_label = compare_scores(score_cross, score_x)

                print(
                    f"  - {LABEL_CROSS} 점수: {score_cross}, {LABEL_X} 점수: {score_x}"
                )
                print(f"  - 판정: {result_label} (기대값: {expected_label})")

                # PASS/FAIL 결정
                if result_label == expected_label:
                    print("  -> [PASS]")
                    pass_count += 1
                else:
                    print("  -> [FAIL]")
                    fail_count += 1
                    fail_details.append(
                        f"[{pattern_key}] 판정 실패: (예상: {expected_label} != 실제 판정: {result_label})"
                    )

            except Exception as e:
                # 데이터가 깨져있거나 에러가 나더라도 FAIL 처리 후 다음으로 넘어감
                print(f"  -> [FAIL] 오류 발생: {e}")
                fail_count += 1
                fail_details.append(f"[{pattern_key}] 데이터/검증 오류: {e}")

        # 3. 최종 요약 출력
        total_cases = pass_count + fail_count
        print("\n=== 모드 2 최종 결과 리포트 ===")
        print(f"Total: {total_cases} | Pass: {pass_count} | Fail: {fail_count}")

        if fail_count > 0:
            print("\n[FAIL 케이스 원인 분석]")
            for detail in fail_details:
                print(f" - {detail}")
        else:
            if total_cases > 0:
                print(
                    "\n[모든 케이스 SUCCESS!] 라벨 정규화와 Epsilon 정책이 성공적으로 동작했습니다."
                )

        # [추가된 부분] 모드 2 요구사항: 3x3 포함 5x5, 13x13, 25x25 성능 분석 출력
        self._print_performance_table([3, 5, 13, 25])
        print("===============================\n")


# 테스트 및 개별 실행용 진입점
if __name__ == "__main__":
    app = SimulatorController()
    # app.run_manual_mode()
    app.run_json_mode()
