from datetime import date
from typing import List
from pydantic import BaseModel, validator


class Habit:
    """Внутренняя модель привычки для хранения в памяти."""
    
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.marks: List[date] = []
        self.streak: int = 0


class HabitCreate(BaseModel):
    """Модель для создания привычки."""
    name: str
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Habit name cannot be empty.")
        return v.strip()

class HabitResponse(BaseModel):
    """Модель ответа после создания привычки."""
    id: int
    name: str

class HabitMarkResponse(BaseModel):
    """Модель ответа после отметки выполнения."""
    id: int
    name: str
    last_marked_at: str
    streak: int

class HabitListResponse(BaseModel):
    id: int
    name: str
    marks: List[str]
    streak: int

class HabitUpdate(BaseModel):
    name: str

class HabitBase(BaseModel):
    id: int
    name: str

class HabitResponse(HabitBase):
    marks: list[date]
    streak: int

class HabitDetailResponse(HabitResponse):
    id: int
    name: str  
    marks: List[str]
    streak: int
