from typing import Optional


class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
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
    action: int
    duration: float
    weight: float
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

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
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message: InfoMessage = InfoMessage(self.__class__.__name__,
                                           self.duration,
                                           self.get_distance(),
                                           self.get_mean_speed(),
                                           self.get_spent_calories())
        return message


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        duration_min = self.duration * 60
        calories: float = ((coeff_calorie_1 * self.get_mean_speed()
                            - coeff_calorie_2) * self.weight
                           / self.M_IN_KM * duration_min)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1: float = 0.035
        coeff_calorie_2: int = 2
        coeff_calorie_3: float = 0.029
        duration_min = self.duration * 60
        calories: float = ((coeff_calorie_1 * self.weight +
                            (self.get_mean_speed() ** coeff_calorie_2
                             // self.height) * coeff_calorie_3
                            * self.weight) * duration_min)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: float
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = (self.length_pool * self.count_pool
                        / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1: float = 1.1
        coeff_calorie_2: int = 2
        calories: float = ((self.get_mean_speed() + coeff_calorie_1)
                           * coeff_calorie_2 * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Optional[Training]:
    """Прочитать данные полученные от датчиков."""
    training_dict = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    try:
        training: Training = training_dict[workout_type](*data)
        return training
    except KeyError:
        print(f'Неизвестный тип тренировки {workout_type}')
        return None


def main(training: Optional[Training]) -> None:
    """Главная функция."""
    if training is not None:
        info: InfoMessage = training.show_training_info()
        training_data: str = info.get_message()
        print(training_data)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
