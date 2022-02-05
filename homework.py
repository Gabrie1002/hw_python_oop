from dataclasses import dataclass
from typing import Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    HOUR_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = (self.action * self.LEN_STEP) / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    KCAL_1: int = 18
    KCAL_2: int = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_distance(self):
        return super().get_distance()

    def get_mean_speed(self):
        return super().get_mean_speed()

    def get_spent_calories(self):
        kcal = ((self.KCAL_1 * self.get_mean_speed()
                - self.KCAL_2) * self.weight
                / self.M_IN_KM * self.duration * self.HOUR_MIN)
        return kcal

    def show_training_info(self):
        return super().show_training_info()


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    KCAL_1: float = 0.035
    KCAL_2: float = 0.029

    def __init__(self,
                 action,
                 duration,
                 weight,
                 height: int):
        super().__init__(action, duration, weight)
        self.height = height

    def get_distance(self):
        return super().get_distance()

    def get_mean_speed(self):
        return super().get_mean_speed()

    def get_spent_calories(self):
        kcal = ((self.KCAL_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.KCAL_2 * self.weight) * self.duration * self.HOUR_MIN)
        return kcal

    def show_training_info(self):
        return super().show_training_info()


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    POOL_1: float = 1.1
    POOL_2: float = 2

    def __init__(self,
                 action,
                 duration,
                 weight,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self):
        """Получить дистанцию в км."""
        distance = (self.action * self.LEN_STEP) / self.M_IN_KM
        return distance

    def get_mean_speed(self):
        speed = (self.length_pool * self.count_pool / self.M_IN_KM
                 / self.duration)
        return speed

    def get_spent_calories(self):
        kcal = ((self.get_mean_speed() + self.POOL_1)
                * self.POOL_2 * self.weight)
        return kcal

    def show_training_info(self):
        return super().show_training_info()


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_type: Dict[str, Training] = {'RUN': Running,
                                          'WLK': SportsWalking,
                                          'SWM': Swimming}
    training = training_type[workout_type](*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
