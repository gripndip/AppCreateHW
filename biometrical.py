from abc import ABC, abstractmethod
from typing import List


# Хранение биометрических данных
class BiometricData:
    """Класс для хранения биометрических данных пользователя."""

    def __init__(self, fingerprint: str, iris: str):
        self.fingerprint = fingerprint  # Отпечаток пальца
        self.iris = iris  # Радужка глаза

    def __str__(self):
        return f"Биометрические данные [Отпечаток пальца: {self.fingerprint}, Радужка глаза: {self.iris}]"


class User:
    """Класс для представления пользователя."""

    def __init__(self, name: str, biometric_data: BiometricData):
        self.name = name
        self.biometric_data = biometric_data  # Биометрические данные пользователя

    def __str__(self):
        return f"Пользователь [Имя: {self.name}]"


class AccessEvent:
    """Класс для представления события доступа."""

    def __init__(self, user: User, success: bool):
        self.user = user  # Пользователь, связанный с событием
        self.success = success  # Успешность попытки доступа

    def __str__(self):
        status = "УСПЕШНО" if self.success else "ПРОВАЛЕНО"
        return f"Событие доступа [Пользователь: {self.user.name}, Статус: {status}]"


# Фабрика для создания объектов биометрических данных

class BiometricDataFactory:
    """Фабрика для создания объектов биометрических данных"""

    @staticmethod
    def create_biometric_data(fingerprint: str, iris: str) -> BiometricData:
        """Создает и возвращает объект BiometricData."""
        return BiometricData(fingerprint, iris)


# Наблюдатель для контроля за событиями доступа

class Observer(ABC):
    """Класс наблюдателя."""

    @abstractmethod
    def update(self, event: AccessEvent):
        """Вызываемается для обновления наблюдателя при событии"""
        pass


class AccessControlSystem:
    """Система управления доступом"""

    def __init__(self):
        self.observers: List[Observer] = []  # Список наблюдателей

    def add_observer(self, observer: Observer):
        """Добавляет наблюдателя в список"""
        self.observers.append(observer)

    def remove_observer(self, observer: Observer):
        """Удаляет наблюдателя из списка"""
        self.observers.remove(observer)

    def notify_observers(self, event: AccessEvent):
        """Уведомляет всех наблюдателей о событии"""
        for observer in self.observers:
            observer.update(event)

    def process_access(self, user: User, allowed_users: List[User]):
        """Обрабатка попытки доступа пользователя и уведомление наблюдателей"""
        if user in allowed_users:  # Проверка, есть ли пользователь в списке разрешенных
            event = AccessEvent(user, success=True)
        else:
            event = AccessEvent(user, success=False)

        # Уведомляет всех наблюдателей о событии
        self.notify_observers(event)


# Уведомление наблюдателей

class AdminNotifier(Observer):
    """Наблюдатель для уведомления администратора о событиях доступа."""

    def update(self, event: AccessEvent):
        """Выводит уведомление для администратора."""
        if not event.success:  # Если попытка доступа несанкционированная
            print(f"[ALERT] Несанкционированный доступ! Пользователь: {event.user.name}")


class Logger(Observer):
    """Логирование событий доступа"""

    def update(self, event: AccessEvent):
        """Записывает событие в лог"""
        print(f"[LOG] {event}")


# Пример использования системы

if __name__ == "__main__":
    # Создаем фабрику биометрических данных
    factory = BiometricDataFactory()

    # Создаем биометрические данные для пользователей
    biometric_data_user1 = factory.create_biometric_data("fingerprint1", "iris1")
    biometric_data_user2 = factory.create_biometric_data("fingerprint2", "iris2")

    # Создаем пользователей
    user1 = User("Иван", biometric_data_user1)
    user2 = User("Ольга", biometric_data_user2)
    unknown_user = User("Мактрахер", factory.create_biometric_data("fingerprint3", "iris3"))

    # Список разрешенных пользователей
    allowed_users = [user1, user2]

    # Создаем систему управления доступом
    access_control = AccessControlSystem()

    # Добавляем наблюдателей
    admin_notifier = AdminNotifier()
    logger = Logger()

    access_control.add_observer(admin_notifier)
    access_control.add_observer(logger)

    # Обрабатываем попытки доступа
    print("Попытка доступа пользователя Иван:")
    access_control.process_access(user1, allowed_users)

    print("\nПопытка доступа пользователя Ольга:")
    access_control.process_access(user2, allowed_users)

    print("\nПопытка доступа неизвестного пользователя:")
    access_control.process_access(unknown_user, allowed_users)
