class InfoMessage:
    """Информационное сообщение о тренировке.
    \nСвойства:
    training_type: str - Имя класса тренировки
    duration: float - Длительность тренировки в часах
    distance: float - Дистанция в километрах
    speed: float - Cредняя скорость
    calories: float - Kоличество килокалорий
    """
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

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки.
    \nСвойства:
    action: int - Количество совершённых действий
    duration: float - Длительность тренировки
    weight: float - Вес спортсмена
    name: str - вид тренировки
    """
    LEN_STEP = 0.65
    M_IN_KM = 1000
    DURATION_MINUTES = 60

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
        message = InfoMessage(self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return message


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        spent_calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                          * self.get_mean_speed()
                          + self.CALORIES_MEAN_SPEED_SHIFT)
                          * self.weight / self.M_IN_KM
                          * (self.duration * self.DURATION_MINUTES))

        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба.
    \nДополнительные свойства:
    height: float - рост пользователя
    """
    COEFFICIENT_1 = 0.035
    COEFFICIENT_2 = 0.029
    METERS_PER_SECOND = 0.278
    C_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed() * self.METERS_PER_SECOND
        height_m = self.height / self.C_IN_M
        time_trainung_in_min = self.duration * self.DURATION_MINUTES
        spent_calories = ((self.COEFFICIENT_1 * self.weight
                          + (mean_speed**2 / height_m)
                          * self.COEFFICIENT_2 * self.weight)
                          * time_trainung_in_min)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание.
    \nДополнительные свойства:
    length_pool: float - длина бассейна в метрах
    count_pool: int - сколько раз пользователь переплыл бассейн
    """
    COEFFICIENT_1 = 1.1
    COEFFICIENT_2 = 2
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories = ((self.get_mean_speed() + self.COEFFICIENT_1)
                          * self.COEFFICIENT_2 * self.weight * self.duration)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}

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
