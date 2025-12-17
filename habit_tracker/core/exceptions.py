"""Кастомные исключения для Habit Tracker."""

from fastapi import HTTPException


class HabitNotFoundException(HTTPException):
    """Привычка не найдена."""
    def __init__(self, detail: str = "Habit not found."):
        super().__init__(status_code=404, detail=detail)


class HabitAlreadyMarkedTodayException(HTTPException):
    """Привычка уже отмечена сегодня."""
    def __init__(self, detail: str = "Habit already marked for today."):
        super().__init__(status_code=409, detail=detail)  # ← 409, а не 400!


class HabitNameConflictException(HTTPException):
    """Дубликат имени привычки."""
    def __init__(self, detail: str = "Habit with this name already exists."):
        super().__init__(status_code=400, detail=detail)


class InvalidInputException(HTTPException):
    """Некорректный ввод."""
    def __init__(self, detail: str = "Invalid input data."):
        super().__init__(status_code=400, detail=detail)
        