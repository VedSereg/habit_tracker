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
    
    # TODO: 1. Проверить, что name не пустое
    #          Если пустое - raise HTTPException(status_code=400, detail="Habit name cannot be empty.")
    if name.strip() == '':
        raise HTTPException(status_code=400, detail="Habit name cannot be empty.")
    # TODO: 2. Проверить, что привычка с таким именем не существует
    #          Если существует - raise HTTPException(status_code=400, detail="Habit with this name already exists.")
    for i in habits_db.values():
        if name.lower() == i.name.lower():
            raise HTTPException(status_code=400, detail="Habit with this name already exists.")
    # TODO: 3. Создать объект Habit с текущим _next_id и name
    habit = Habit(id=_next_id, name=name)
    # TODO: 4. Сохранить в habits_db
    habits_db[habit.id] = habit
    # TODO: 5. Увеличить _next_id
    _next_id += 1
    # TODO: 6. Вернуть созданную привычку
    return habit


def mark_habit(habit_id: int) -> Habit:
    """Отметить выполнение привычки за текущий день."""
    
    # TODO: 1. Получить привычку из habits_db по habit_id
    #          Если не найдена - raise HTTPException(status_code=404, detail="Habit not found.")
    if habit_id not in habits_db:
        raise HTTPException(status_code=404, detail="Habit not found.")
    # TODO: 2. Получить сегодняшнюю дату (date.today())
    today = date.today()
    # TODO: 3. Проверить, что today не в habit.marks
    #          Если уже есть - raise HTTPException(status_code=400, detail="Habit already marked for today.")
    if today in habits_db[habit_id].marks:
        raise HTTPException(status_code=400, detail="Habit already marked for today.")
    # TODO: 4. Добавить today в habit.marks
    habits_db[habit_id].marks.append(today)
    # TODO: 5. Вернуть обновленную привычку
    return habits_db[habit_id]


def get_all_habits() -> List[Habit]:
    """Получить список всех привычек."""
    # TODO: Вернуть список всех привычек из habits_db
    return list(habits_db.values())
