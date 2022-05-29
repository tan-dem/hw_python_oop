from dataclasses import dataclass
from typing import Optional, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE_STR_CONST: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Вернуть строку сообщения с данными о тренировке."""
        message_str = self.MESSAGE_STR_CONST.format(
            training_type=self.training_type,
            duration=self.duration,
            distance=self.distance,
            speed=self.speed,
            calories=self.calories,
        )
        return message_str


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

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
        raise NotImplementedError('Метод не переопределен в дочернем классе')

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

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_min = self.duration * self.MIN_IN_HOUR
        calories: float = (
                (self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed()
                 - self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight
                / self.M_IN_KM * duration_min
        )
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_MEAN_SPEED_EXPONENT: int = 2
    CALORIES_LOCAL_MULTIPLIER_WALK: float = 0.029

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
        duration_min = self.duration * self.MIN_IN_HOUR
        calories: float = (
                (self.CALORIES_WEIGHT_MULTIPLIER
                 * self.weight
                 + (self.get_mean_speed()
                    ** self.CALORIES_MEAN_SPEED_EXPONENT
                    // self.height)
                 * self.CALORIES_LOCAL_MULTIPLIER_WALK
                 * self.weight)
                * duration_min
        )
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_ADDEND: float = 1.1
    CALORIES_LOCAL_MULTIPLIER_SWIM: int = 2

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
        speed: float = (
                self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration
        )
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories: float = (
                (self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_ADDEND)
                * self.CALORIES_LOCAL_MULTIPLIER_SWIM
                * self.weight
        )
        return calories


def read_package(workout_type: str, data: list) -> Optional[Training]:
    """Прочитать данные полученные от датчиков."""
    training_dict: dict[str, Type] = {'SWM': Swimming,
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
