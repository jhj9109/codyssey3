import json

from src.constants import LABEL_CROSS, LABEL_X, Color
from src.npu_core import (
    mac_operation,
    mac_operation_1d,
    compare_scores,
    normalize_label,
)
from src.utils import (
    parse_matrix_input,
    extract_size_from_key,
    validate_matrix_size,
    generate_dummy_matrix,
    measure_mac_performance,
    generate_random_filter_pattern,
    flatten_matrix,
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
                lines.append(input(f"Row {i}: "))

            try:
                # 순수 함수인 parse_matrix_input을 호출하여 로직만 분리
                matrix = parse_matrix_input(lines, size)
                print(f"-> {matrix_name} 저장 완료!")
                return matrix
            except ValueError as e:
                print(
                    f"{Color.FAIL}[입력 형식 오류] {e}\n다시 입력해주세요.\n{Color.ENDC}"
                )

    def _load_json_file(self, file_path):
        """(내부 메서드) JSON 파일을 로드하여 데이터 구조로 반환합니다. 예외 처리를 포함합니다."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            print(f"-> '{file_path}' 파일 로드 성공!")

            filters_data = data["filters"]
            patterns_data = data["patterns"]

            return filters_data, patterns_data
        except FileNotFoundError:
            print(
                f"{Color.FAIL}[오류] '{file_path}' 파일을 찾을 수 없습니다.{Color.ENDC}"
            )
        except json.JSONDecodeError:
            print(
                f"{Color.FAIL}[오류] '{file_path}' 파일이 올바른 JSON 형식이 아닙니다.{Color.ENDC}"
            )
        except KeyError as e:
            print(
                f"{Color.FAIL}[오류] JSON 데이터에서 필요한 키가 누락되었습니다: {e}{Color.ENDC}"
            )
        except Exception as e:
            print(
                f"{Color.FAIL}[오류] JSON 파일 로드 중 예기치 않은 오류가 발생했습니다: {e}{Color.ENDC}"
            )
        return None

    def _print_performance_table(self, sizes):
        """(내부 메서드) 최적화 전(2D)과 후(1D)의 성능 측정 결과를 비교 출력합니다."""
        print(f"{Color.HEADER}\n=== [보너스] 최적화 성능 분석 리포트 ==={Color.ENDC}")
        print(
            f"{'크기(NxN)':<10} | {'연산 횟수':<10} | {'2D MAC (ms)':<15} | {'1D MAC (ms)':<15}"
        )
        print(f"{Color.HEADER}" + "-" * 70 + f"{Color.ENDC}")

        for size in sizes:
            # 보너스 과제 2: 더미 데이터 대신 '패턴 생성기' 활용
            pattern_2d = generate_dummy_matrix(size)
            filter_2d = generate_random_filter_pattern(size)

            # 보너스 과제 1: 1차원 배열로 변환
            pattern_1d = flatten_matrix(pattern_2d)
            filter_1d = flatten_matrix(filter_2d)

            # 10회 반복 측정
            iterations = 10
            avg_time_2d = measure_mac_performance(
                mac_operation, pattern_2d, filter_2d, iterations
            )
            avg_time_1d = measure_mac_performance(
                mac_operation_1d, pattern_1d, filter_1d, iterations
            )

            operations = size * size

            print(
                f"{f'{size}x{size}':<10}    |  {operations:<12} |   {avg_time_2d:.6f}      | {avg_time_1d:.6f}"
            )
        print(f"{Color.HEADER}" + "-" * 70 + f"{Color.ENDC}")

    def run_manual_mode(self):
        """모드 1(수동 입력) 시나리오 진행 메서드"""
        print(f"{Color.HEADER}\n=== 모드 1: 사용자 입력 (3x3) 시작 ==={Color.ENDC}")

        # 1. 입력 단계 (I/O)
        filter_cross = self._read_matrix_from_console(f"필터 {LABEL_CROSS}", 3)
        filter_x = self._read_matrix_from_console(f"필터 {LABEL_X}", 3)
        pattern = self._read_matrix_from_console("입력 패턴", 3)

        # 2. 연산 및 판정 단계 (순수 함수 조합)
        score_cross = mac_operation(pattern, filter_cross)
        score_x = mac_operation(pattern, filter_x)
        result = compare_scores(score_cross, score_x)

        # 3. 출력 단계 (I/O)
        print(f"{Color.HEADER}\n=== 연산 및 판정 결과 ==={Color.ENDC}")
        print(f"{Color.OKCYAN}{LABEL_CROSS} 필터 점수: {score_cross}{Color.ENDC}")
        print(f"{Color.OKCYAN}{LABEL_X} 필터 점수: {score_x}{Color.ENDC}")
        print(f"{Color.OKGREEN}최종 판정: {result}{Color.ENDC}")

        # [추가된 부분] 모드 1 요구사항: 3x3 크기에 대한 성능 분석 출력
        self._print_performance_table([3])
        print(f"{Color.HEADER}=== 모드 1 종료 ==={Color.ENDC}")

    def run_json_mode(self, file_path="data.json"):
        """모드 2(JSON 파일 자동 평가) 시나리오 진행 메서드"""
        print(
            f"{Color.HEADER}\n=== 모드 2: JSON 파일 분석 ({file_path}) 시작 ==={Color.ENDC}"
        )

        data = self._load_json_file(file_path)
        if data is None:
            print(f"{Color.FAIL}모드 2 실행을 중단합니다.{Color.ENDC}")
            return

        filters_data, patterns_data = data

        pass_count = 0
        fail_count = 0
        fail_details = []

        # 2. 패턴별 반복 평가
        for pattern_key, pattern_info in patterns_data.items():
            print(f"{Color.HEADER}\n[Case: {pattern_key}] 평가 중...{Color.ENDC}")

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

                # MAC 연산 및 판정 (잘못된 인자 존재시 연산과정에서 에러 발생 가능)
                score_cross = mac_operation(pattern_input, filter_cross)
                score_x = mac_operation(pattern_input, filter_x)
                result_label = compare_scores(score_cross, score_x)

                print(
                    f"  - {LABEL_CROSS} 점수: {score_cross}, {LABEL_X} 점수: {score_x}"
                )
                print(f"  - 판정: {result_label} (기대값: {expected_label})")

                # PASS/FAIL 결정
                if result_label == expected_label:
                    print(f"  -> {Color.OKGREEN}[PASS]{Color.ENDC}")
                    pass_count += 1
                else:
                    print(f"  -> {Color.FAIL}[FAIL]{Color.ENDC}")
                    fail_count += 1
                    fail_details.append(
                        f"[{pattern_key}] 판정 실패: (예상: {expected_label} != 실제 판정: {result_label})"
                    )

            except Exception as e:
                # 데이터가 깨져있거나 에러가 나더라도 FAIL 처리 후 다음으로 넘어감
                print(f"  -> {Color.FAIL}[FAIL]{Color.ENDC} 오류 발생: {e}")
                fail_count += 1
                fail_details.append(f"[{pattern_key}] 데이터/검증 오류: {e}")

        # 3. 최종 요약 출력
        total_cases = pass_count + fail_count
        print(f"{Color.HEADER}\n=== 모드 2 최종 결과 리포트 ==={Color.ENDC}")
        print(f"Total: {total_cases} | Pass: {pass_count} | Fail: {fail_count}")

        if fail_count > 0:
            print(f"{Color.FAIL}\n[FAIL 케이스 원인 분석]{Color.ENDC}")
            for detail in fail_details:
                print(f" - {detail}")
        else:
            if total_cases > 0:
                print(
                    f"{Color.OKGREEN}\n[모든 케이스 SUCCESS!] 라벨 정규화와 Epsilon 정책이 성공적으로 동작했습니다.{Color.ENDC}"
                )

        # [추가된 부분] 모드 2 요구사항: 3x3 포함 5x5, 13x13, 25x25 성능 분석 출력
        self._print_performance_table([3, 5, 13, 25])


# 테스트 및 개별 실행용 진입점
if __name__ == "__main__":
    app = SimulatorController()
    # app.run_manual_mode()
    app.run_json_mode()
