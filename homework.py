from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Возвращает сообщения об тренировки."""
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action: float = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Возвращает дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Возвращает среднюю скорость движения."""
        average = self.get_distance() / self.duration
        return average

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise Exception('Базовый класс не высчитывает калории')

    def show_training_info(self) -> InfoMessage:
        """Возвращает информационное сообщение о выполненной тренировке."""
        return InfoMessage(training_type=self.__class__.__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    RATIO_1: float = 18
    RATIO_2: float = 20
    minutes: float = 60

    def get_spent_calories(self) -> float:
        """Возвращвет количетсво калорий при беге."""
        calories = ((self.RATIO_1
                    * self.get_mean_speed()
                    - self.RATIO_2)
                    * self.weight
                    / self.M_IN_KM
                    * (self.duration
                    * self.minutes))
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    RATIO_1: float = 0.035
    RATIO_2: float = 0.029
    RATIO_3: float = 2
    MINUTES: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Возвращает количество калорий при ходьбе."""
        calories = ((self.RATIO_1 * self.weight
                     + (self.get_mean_speed()**self.RATIO_3 // self.height)
                     * self.RATIO_2
                     * self.weight) * (self.duration * self.MINUTES))
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    RATIO_1: float = 1.1
    RATIO_2: float = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Возвращает среднюю скорость движения."""
        speed = (self.length_pool * self.count_pool
                 / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        calories = (self.get_mean_speed() + self.RATIO_1
                     * self.RATIO_2 * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Возвращает данные полученные от датчиков."""
    workout: Dict[str, type] = {'SWM': Swimming,
                                'RUN': Running,
                                'WLK': SportsWalking}
    if workout_type in workout:
        return workout[workout_type](*data)
    else:
        raise KeyError(f'{workout_type} нет в списке тренеровок.')


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
