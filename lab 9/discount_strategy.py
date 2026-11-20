from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float) -> None:
        self.__percentage = percentage   # e.g. 10 means 10% off

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)


class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float) -> None:
        self.__threshold = threshold   # minimum total to qualify
        self.__amount = amount         # flat amount to subtract

    def apply(self, total: float) -> float:
        return total - self.__amount if total >= self.__threshold else total


class StudentDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total * 0.85   # 15% off for students
