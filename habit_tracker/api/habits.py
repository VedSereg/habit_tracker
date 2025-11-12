from typing import List
from fastapi import APIRouter, status
from habit_tracker.core import services
from habit_tracker.core.models import (
    HabitCreate, 
    HabitResponse, 
    HabitMarkResponse,
    HabitListResponse
)

router = APIRouter()


@router.post("/habits/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(habit: HabitCreate):
    """Создать новую привычку."""
    # TODO: 1. Вызвать services.create_habit() с habit.name
    created_habit = services.create_habit(habit.name)
    # TODO: 2. Вернуть HabitResponse с id и name созданной привычки
    return HabitResponse(id=created_habit.id, name=created_habit.name)



@router.post("/habits/{habit_id}/mark/", response_model=HabitMarkResponse)
def mark_habit(habit_id: int):
    """Отметить выполнение привычки за текущий день."""
    # TODO: 1. Вызвать services.mark_habit() с habit_id
    marked_habit = services.mark_habit(habit_id)
    # TODO: 2. Получить последнюю дату из habit.marks
    last_mark = marked_habit.marks[-1]
    # TODO: 3. Отформатировать дату в строку (YYYY-MM-DD)
    last_mark_at = last_mark.isoformat()
    # TODO: 4. Вернуть HabitMarkResponse
    return HabitMarkResponse(id=marked_habit.id, name=marked_habit.name, last_marked_at=last_mark_at)


@router.get("/habits/", response_model=List[HabitListResponse])
def get_all_habits():
    """Получить список всех привычек."""
    # TODO: 1. Вызвать services.get_all_habits()
    habits_list = services.get_all_habits()
    # TODO: 2. Для каждой привычки создать HabitListResponse
    result = []
    for habit in habits_list:
        marks_str = [mark.isoformat() for mark in habit.marks]
        result.append(HabitListResponse(id=habit.id, name=habit.name, marks=marks_str))
    # TODO: 3. Преобразовать dates в список строк формата YYYY-MM-DD
    # TODO: 4. Вернуть список
    return result
