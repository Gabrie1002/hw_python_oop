class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    HOUR_MIN = 60

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
        speed = Training.get_distance(self) / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        return super().get_distance()

    def get_mean_speed(self) -> float:
        return super().get_mean_speed()

    def get_spent_calories(self) -> float:
        kcal = ((self.coeff_calorie_1*Running.get_mean_speed(self)-self.coeff_calorie_2)*
                 self.weight/
                 self.M_IN_KM * self.duration*self.HOUR_MIN)
        return kcal

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    const1 = 0.035
    const2 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.height = height

    def get_distance(self) -> float:
        return super().get_distance()

    def get_mean_speed(self) -> float:
        return super().get_mean_speed()

    def get_spent_calories(self) -> float:
        kcal = ((self.const1 * self.weight +
                (SportsWalking.get_mean_speed(self) ** 2 // self.height)*
                 self.const2 * self.weight) * self.duration*self.HOUR_MIN)
        return kcal

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    pool_const1 = 1.1
    pool_const2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = (self.action * self.LEN_STEP) / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        speed = self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        return speed

    def get_spent_calories(self) -> float:
        kcal = (Swimming.get_mean_speed(self)+self.pool_const1) * self.pool_const2 * self.weight
        return kcal

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()

def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_type = {'RUN': Running,
                     'WLK': SportsWalking,
                     'SWM': Swimming}

    training1 = training_type[workout_type](*data)
    return training1

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
