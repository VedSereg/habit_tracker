from datetime import date
from typing import List
from pydantic import BaseModel


class Habit:
    """Внутренняя модель привычки для хранения в памяти."""
    
    def __init__(self, id: int, name: str, marks: List[date] = None):
        self.id = id
        self.name = name
        self.marks = marks if marks is not None else []
        self.streak: int = 0  


class HabitBase(BaseModel):
    """Базовая модель привычки."""
    id: int
    name: str


class HabitCreate(BaseModel):
    """Модель для создания привычки."""
    name: str
    

class HabitUpdate(BaseModel):
    """Модель для обновления привычки."""
    name: str


class HabitResponse(HabitBase):
    """Полная информация о привычке (используется и для списка и для деталей)."""
    marks: List[date]  
    streak: int    


class HabitMarkResponse(BaseModel):
    """Модель ответа после отметки выполнения."""
    id: int
    name: str
    last_marked_at: str
    streak: int

class HabitStatsResponse(BaseModel):
    """Модель для статистики привычки."""
    id: int
    name: str
    total_marks: int
    current_streak: int
    max_streak: int
    success_rate: float
    last_dates: List[date]
    
    class Config:
        json_encoders = {
            date: lambda v: v.isoformat()
        }