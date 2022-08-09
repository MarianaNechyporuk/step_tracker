class InfoMessage:
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
        return (f'Training type: {self.training_type}; '
                f'Duration: {self.duration:.3f} h.; '
                f'Distance: {self.distance:.3f} km; '
                f'Mid. speed: {self.speed:.3f} km/h; '
                f'Burned ccal: {self.calories:.3f}.')


class Training:
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.LEN_STEP = 0.65
        self.M_IN_KM = 1000

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
    pass

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    coeff1 = 18
    coeff2 = 20

    def get_spent_calories(self) -> float:
        return ((self.coeff1 * self.get_mean_speed() - self.coeff2)
                * self.weight / self.M_IN_KM * (self.duration * 60))


class SportsWalking(Training):
    coeff1 = 0.035
    coeff2 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.coeff1 * self.weight + (self.get_mean_speed() * 2
                 // self.height)
                 * self.coeff2 * self.weight) * (self.duration * 60))


class Swimming(Training):
    coeff1 = 1.1
    coeff2 = 2
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed()
                + self.coeff1) * self.coeff2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    training: dict = {'SWM': Swimming,
                      'RUN': Running,
                      'WLK': SportsWalking}
    return training[workout_type](*data)


def main(training: Training) -> None:
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
        