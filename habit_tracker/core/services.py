from datetime import date
from typing import Dict, List
from fastapi import HTTPException
from habit_tracker.core.models import Habit

# In-memory хранилище
habits_db: Dict[int, Habit] = {}
_next_id = 1


def create_habit(name: str) -> Habit:
    """Создать новую привычку."""
    global _next_id

    if name.strip() == '':
        raise HTTPException(status_code=400, detail="Habit name cannot be empty.")
    for i in habits_db.values():
        if name.lower() == i.name.lower():
            raise HTTPException(status_code=400, detail="Habit with this name already exists.")
    habit = Habit(id=_next_id, name=name)
    habits_db[habit.id] = habit
    _next_id += 1
    return habit


def mark_habit(habit_id: int) -> Habit:
    """Отметить выполнение привычки за текущий день."""
    
    if habit_id not in habits_db:
        raise HTTPException(status_code=404, detail="Habit not found.")
    today = date.today()
    if today in habits_db[habit_id].marks:
        raise HTTPException(status_code=400, detail="Habit already marked for today.")
    habits_db[habit_id].marks.append(today)
    return habits_db[habit_id]


def get_all_habits() -> List[Habit]:
    """Получить список всех привычек."""

    return list(habits_db.values())
