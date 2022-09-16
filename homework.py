class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        training_type = self.training_type
        duration = self.duration
        distance = self.distance
        speed = self.speed
        calories = self.calories
        ans_str = (f'Тип тренировки: {training_type};'
                   f' Длительность: {duration:.3f} ч.;'
                   f' Дистанция: {distance:.3f} км;'
                   f' Ср. скорость: {speed:.3f} км/ч;'
                   f' Потрачено ккал: {calories:.3f}.'
                   )
        return ans_str


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.LEN_STEP = 0.65

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        weight = self.weight
        M_IN_KM = self.M_IN_KM
        time = self.duration
        coeff_1 = 18
        coeff_2 = 20

        return (coeff_1 * mean_speed - coeff_2) * weight / M_IN_KM * time * 60


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.LEN_STEP = 0.65
        self.height = height

    def get_spent_calories(self) -> float:
        coeff_1 = 0.035
        coeff_2 = 0.029
        weight = self.weight
        mean_speed = self.get_mean_speed()
        height = self.height
        time = self.duration
        return (coeff_1 * weight + (mean_speed**2 // height)
                * coeff_2 * weight) * time * 60


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

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
        length = self.length_pool
        count_pool = self.count_pool
        time = self.duration
        M_IN_KM = self.M_IN_KM

        return length * count_pool / M_IN_KM / time

    def get_spent_calories(self) -> float:
        mean_speed = self. get_mean_speed()
        cooff_1 = 1.1
        cooff_2 = 2
        weight = self.weight

        return (mean_speed + cooff_1) * cooff_2 * weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    diction = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return diction[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
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
