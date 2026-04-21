from dataclasses import dataclass
from typing import List


@dataclass
class Matrix:
    """N x N 2차원 행렬 데이터를 안전하게 다루기 위한 데이터 클래스"""

    data: List[List[float]]

    def __post_init__(self):
        """
        객체가 생성되는 즉시 자동으로 호출되는 검증 메서드입니다.
        이 클래스로 만들어진 객체는 무조건 완벽한 N x N 정방행렬임이 보장됩니다.
        """
        if not self.data:
            raise ValueError("빈 행렬을 생성할 수 없습니다.")

        n = len(self.data)
        for row in self.data:
            if not isinstance(row, list) or len(row) != n:
                raise ValueError(
                    f"정방 행렬(N x N) 구조가 아닙니다. (기대 크기: {n}x{n})"
                )

    @property
    def size(self) -> int:
        """행렬의 크기 N을 반환합니다. (예: matrix.size 로 접근)"""
        return len(self.data)

    def to_1d(self) -> List[float]:
        """(보너스 과제) 2차원 배열을 1차원 배열(길이 N^2)로 평탄화하여 반환합니다."""
        return [val for row in self.data for val in row]

    # --- 파이썬 매직 메서드 (Magic Methods) ---
    def __getitem__(self, index):
        """matrix.data[i][j] 대신 matrix[i][j] 형태로 편리하게 접근할 수 있게 해줍니다."""
        return self.data[index]

    def __len__(self):
        """len(matrix)를 호출하면 행렬의 크기 N을 반환합니다."""
        return len(self.data)
