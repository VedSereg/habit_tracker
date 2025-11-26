from typing import List
from fastapi import HTTPException
from fastapi import APIRouter, status
from habit_tracker.core import services
from habit_tracker.core.models import (
    HabitCreate, 
    HabitResponse, 
    HabitMarkResponse,
    HabitListResponse
)
from habit_tracker.core.services import create_habit, get_all_habits_with_details

router = APIRouter()


@router.post("/habits/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(habit: HabitCreate):
    """Создать новую привычку."""
    created_habit = services.create_habit(habit.name)
    return HabitResponse(id=created_habit.id, name=created_habit.name)



@router.post("/habits/{habit_id}/mark/", response_model=HabitMarkResponse)
def mark_habit(habit_id: int):
    """Отметить выполнение привычки за текущий день."""
    marked_habit = services.mark_habit(habit_id)

    if not marked_habit.marks:
        raise HTTPException(
            status_code=400,
            detail="Habit has no marks - marking may have failed"
        )
    
    last_mark = marked_habit.marks[-1]
    last_marked_at = last_mark.isoformat()
    return HabitMarkResponse(id=marked_habit.id, name=marked_habit.name, last_marked_at=last_marked_at)


@router.get("/habits/", response_model=List[HabitListResponse])
def get_all_habits():
    """Получить список всех привычек."""
    habits_list = services.get_all_habits()
    result = []
    for habit in habits_list:
        marks_str = [mark.isoformat() for mark in habit.marks]
        result.append(HabitListResponse(id=habit.id, name=habit.name, marks=marks_str))
    return result
