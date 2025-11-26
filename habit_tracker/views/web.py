from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from habit_tracker.core.services import (
    get_all_habits_with_details, 
    is_habit_marked_today,
    get_habit_by_id_with_details,
    create_habit,
    update_habit,
    delete_habit,
    mark_habit
)
from habit_tracker.core.models import HabitCreate, HabitUpdate

router = APIRouter()
templates = Jinja2Templates(directory="habit_tracker/templates")


@router.get("/", name="main-page")
def get_all_habits_form(request: Request):
    """Получение главной страницы."""
    habits = get_all_habits_with_details()
    return templates.TemplateResponse("index.html", 
        {
            "request": request,
            "habits": habits,
            "is_marked_today": is_habit_marked_today
        }
    )

@router.get("/habit/{habit_id}/", name="habit-detail")
def get_habit_detail(request: Request, habit_id: int):
    """Получение детальной страницы привычки."""
    habit = get_habit_by_id_with_details(habit_id)
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    return templates.TemplateResponse("habit_detail.html", 
        {
            "request": request,
            "habit": habit
        }
    )

@router.post("/habit/add", name="add_habit_from_form")
def create_habit_form(name: str = Form(...)): 
    """Добавление привычки из формы."""
    try:
        habit_data = HabitCreate(name=name)
        create_habit(habit_data)
        return RedirectResponse(
            url=router.url_path_for("main-page"),
            status_code=303
        )
    except ValueError:
        return RedirectResponse(
            url=router.url_path_for("main-page"), 
            status_code=303
        )

@router.post("/habit/{habit_id}/mark", name="mark_habit_from_form")
def mark_habit_form(habit_id: int):
    """Отметка привычки из формы."""
    try:
        mark_habit(habit_id)
        return RedirectResponse(
            url=router.url_path_for("main-page"),
            status_code=303
        )
    except ValueError:
        return RedirectResponse(
            url=router.url_path_for("main-page"), 
            status_code=303
        )


@router.post("/habit/{habit_id}/edit", name="edit_habit_from_form")
def edit_habit_form(habit_id: int, name: str = Form(...)):
    """Редактирование привычки из формы."""
    try:
        habit_data = HabitUpdate(name=name)
        update_habit(habit_id, habit_data)
        return RedirectResponse(
            url=router.url_path_for("habit-detail", habit_id=habit_id),
            status_code=303
        )
    except ValueError:
        return RedirectResponse(
            url=router.url_path_for("habit-detail", habit_id=habit_id),
            status_code=303
        )


@router.post("/habit/{habit_id}/delete", name="delete_habit_from_form")
def delete_habit_form(habit_id: int):
    """Удаление привычки из формы."""
    delete_habit(habit_id)
    return RedirectResponse(
        url=router.url_path_for("main-page"),
        status_code=303
    )
