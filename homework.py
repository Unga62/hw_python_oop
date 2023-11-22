from dataclasses import dataclass, astuple


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке.
    \nСвойства:
    training_type: str - Имя класса тренировки
    duration: float - Длительность тренировки в часах
    distance: float - Дистанция в километрах
    speed: float - Cредняя скорость в км/ч
    calories: float - Kоличество килокалорий
    """
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    DEFAULT_MESSAGE = ('Тип тренировки: {}; Длительность: {:1.3f} ч.; '
                       'Дистанция: {:1.3f} км; Ср. скорость: {:1.3f} км/ч; '
                       'Потрачено ккал: {:1.3f}.')

    def get_message(self) -> str:
        infomessage = InfoMessage(self.training_type, self.duration,
                                  self.distance, self.speed, self.calories)
        data: tuple = astuple(infomessage)
        formatted_message: str = self.DEFAULT_MESSAGE.format(*data)
        return formatted_message


class Training:
    """Базовый класс тренировки.
    \nСвойства:
    action: int - Количество совершённых действий
    duration_hr: float - Длительность тренировки
    weight_kg: float - Вес спортсмена
    name: str - вид тренировки
    """
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    DURATION_MINUTES: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration_hr = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_hr

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Метод определяется в дочерних классах')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.__class__.__name__,
                              self.duration_hr,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return message


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        spent_calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                                 * self.get_mean_speed()
                                 + self.CALORIES_MEAN_SPEED_SHIFT)
                                 * self.weight_kg / self.M_IN_KM
                                 * (self.duration_hr * self.DURATION_MINUTES))

        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба.
    \nДополнительные свойства:
    height: float - рост пользователя
    """
    COEFFICIENT_1: float = 0.035
    COEFFICIENT_2: float = 0.029
    METERS_PER_SECOND: float = 0.278
    C_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height_cm = height

    def get_spent_calories(self) -> float:
        mean_speed: float = self.get_mean_speed() * self.METERS_PER_SECOND
        height_in_m: float = self.height_cm / self.C_IN_M
        time_trainung_in_min: float = self.duration_hr * self.DURATION_MINUTES
        spent_calories: float = ((self.COEFFICIENT_1 * self.weight_kg
                                  + (mean_speed**2 / height_in_m)
                                  * self.COEFFICIENT_2 * self.weight_kg)
                                 * time_trainung_in_min)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание.
    \nДополнительные свойства:
    length_pool: float - длина бассейна в метрах
    count_pool: int - сколько раз пользователь переплыл бассейн
    """
    COEFFICIENT_1: float = 1.1
    COEFFICIENT_2: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed: float = (self.length_pool_m * self.count_pool
                             / self.M_IN_KM / self.duration_hr)
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories: float = ((self.get_mean_speed() + self.COEFFICIENT_1)
                                 * self.COEFFICIENT_2 * self.weight_kg
                                 * self.duration_hr)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}

    if workout_type not in training_type:
        raise ValueError('Неверный тип тренировки')
    else:
        return training_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    return print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
