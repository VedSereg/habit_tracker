from typing import List
from fastapi import APIRouter, status
from habit_tracker.core import services
from habit_tracker.core.models import (
    HabitCreate, 
    HabitResponse, 
    HabitBase,
    HabitUpdate, 
    HabitMarkResponse,
    HabitStatsResponse
)
from habit_tracker.core.services import (
    get_all_habits_with_details,
    get_habit_by_id_with_details,
    create_habit,
    update_habit,
    delete_habit, 
    mark_habit,
    get_habit_by_id,
    calculate_habit_stats
)
from habit_tracker.core.exceptions import HabitNotFoundException

router = APIRouter()


@router.post("/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit_endpoint(habit: HabitCreate):
    """Создать новую привычку."""
    created_habit = create_habit(habit)
    return HabitResponse(
        id=created_habit.id,
        name=created_habit.name,
        marks=created_habit.marks,  
        streak=created_habit.streak
    )
    
@router.get("/", response_model=List[HabitResponse])
def get_all_habits_endpoint():
    """Получить список всех привычек."""
    habits_data = get_all_habits_with_details()
    result = []
    for habit_dict in habits_data:
        habit_response = HabitResponse(
            id=habit_dict["id"],
            name=habit_dict["name"], 
            marks=habit_dict["marks"],
            streak=habit_dict["streak"]
        )
        result.append(habit_response)
    return result
     
@router.get("/{habit_id}/", response_model=HabitResponse)
def get_habit_by_id_endpoint(habit_id: int):
    """Получить привычку по id."""
    habit = get_habit_by_id_with_details(habit_id)
    if habit is None:
        raise HabitNotFoundException()
    
    return HabitResponse(
        id=habit["id"],
        name=habit["name"],
        marks=habit["marks"],
        streak=habit["streak"]
    )

@router.put("/{habit_id}/", response_model=HabitBase)
def update_habit_endpoint(habit_id: int, habit_data: HabitUpdate):
    """Обновить привычку."""
    updated_habit = update_habit(habit_id, habit_data)
    return HabitBase(
        id=updated_habit.id,
        name=updated_habit.name
    )
    
@router.delete("/{habit_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit_endpoint(habit_id: int):
    delete_habit(habit_id)

@router.post("/{habit_id}/mark/", response_model=HabitMarkResponse)
def mark_habit_endpoint(habit_id: int):
    mark = mark_habit(habit_id)
    return HabitMarkResponse(
        id=mark["id"],
        name=mark["name"],
        last_marked_at=mark["last_marked_at"],
        streak=mark["streak"]
    )

@router.get("/{habit_id}/stats/", response_model=HabitStatsResponse)
def get_habit_stats(habit_id: int):
    """Получить статистику по привычке."""
    habit = get_habit_by_id(habit_id)
    stats = calculate_habit_stats(habit)
    
    return HabitStatsResponse(
        id=habit.id,
        name=habit.name,
        **stats
    )