from dataclasses import asdict, dataclass
from typing import Dict, List, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    ANSWER_TEAMPLATE = (
        'Тип тренировки: {training_type};'
        ' Длительность: {duration:.3f} ч.;'
        ' Дистанция: {distance:.3f} км;'
        ' Ср. скорость: {speed:.3f} км/ч;'
        ' Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.ANSWER_TEAMPLATE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    MIN_IN_HU: int = 60
    LEN_STEP: float = 0.65

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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'Данного метода нет у класса {(self).__name__}'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=type(self).__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    LEN_STEP: float = 0.65
    COEFF_1: int = 18
    COEFF_2: int = 20

    def get_spent_calories(self) -> float:
        return (
            (self.COEFF_1 * self.get_mean_speed() - self.COEFF_2)
            * self.weight / self.M_IN_KM
            * self.duration * self.MIN_IN_HU
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP: float = 0.65
    COEFF_1: float = 0.035
    COEFF_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            (self.COEFF_1 * self.weight
             + (self.get_mean_speed()**2 // self.height)
             * self.COEFF_2 * self.weight)
            * self.duration * self.MIN_IN_HU
        )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_1: float = 1.1
    COEFF_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.count_pool = count_pool
        self.length_pool = length_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFF_1)
                * self.COEFF_2 * self.weight)


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    diction: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if not (workout_type in diction):
        raise ValueError(': no key in diction')
    return diction[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('WL', [1, 2])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
