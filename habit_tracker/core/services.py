from datetime import date
from typing import Dict, List
from fastapi import HTTPException
from habit_tracker.core.models import Habit, HabitCreate, HabitUpdate

# In-memory хранилище
habits_db: dict[int, Habit] = {
    1: Habit(id=1, name="Бег", marks=[date(2025, 7, 10), date(2025, 7, 11)]),
    2: Habit(id=2, name="Чтение", marks=[date(2025, 7, 11)]),
    3: Habit(id=3, name="Медитация", marks=[])
}
next_habit_id = 4
TODAY = date(2025, 7, 12)


def create_habit(name: str) -> Habit:
    """Создать новую привычку."""
    global next_habit_id

    if name.strip() == '':
        raise HTTPException(status_code=400, detail="Habit name cannot be empty.")
    for i in habits_db.values():
        if name.lower() == i.name.lower():
            raise HTTPException(status_code=400, detail="Habit with this name already exists.")
    habit = Habit(id=next_habit_id, name=name)
    habits_db[habit.id] = habit
    next_habit_id += 1
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


def calculate_streak(marks: list[date]) -> int:
    """
    Рассчитывает *текущий* streak по датам в `marks` относительно `TODAY`.  
    Алгоритм в общих чертах:
    - пустой список -> streak = 0;
    - работай с отсортированным по убыванию набором уникальных дат;
    - если среди последних дат нет ни `TODAY`, ни вчерашнего дня -> streak = 0;
    - иначе отсчитывай подряд идущие дни назад (без пропусков) от `TODAY` или вчерашнего дня.
    """
    pass


def get_all_habits_with_details() -> list[dict]:
    """
    Возвращает список привычек, где для каждой привычки в словаре есть все её поля 
    (`id`, `name`, `marks` как список дат) **и** рассчитанный `streak`.  
    Список должен быть отсортирован по `id` (по возрастанию).  
    **Важно:** `marks` должен быть списком объектов `date`, так как в шаблонах 
    может использоваться форматирование дат.
    """
    pass

def get_habit_by_id_with_details(habit_id: int) -> dict | None:
    """
    Возвращает одну привычку по `id` в виде словаря с полями привычки 
    (включая `id`, `name`, `marks` как список дат) и рассчитанным `streak`, 
    либо `None`, если привычки нет.  
    **Важно:** `marks` должен быть списком объектов `date`, а не строк, 
    так как в шаблонах используется `mark.strftime()
    """
    pass

def create_habit(habit_data: HabitCreate) -> Habit:
    """
    Создаёт новую привычку:
    - имя не должно быть пустым (валидация на уровне сервиса; при ошибке выбрасывается `ValueError`);
    - имя должно быть уникальным среди существующих привычек;
    - используется и увеличивается глобальная переменная `next_habit_id` (используй `global next_habit_id`).
    """
    pass

def update_habit(habit_id: int, habit_data: HabitUpdate) -> Habit | None:
    """
    Обновляет существующую привычку:
    - возвращает обновлённую привычку или `None`, если она не найдена;
    - проверяет непустое имя и уникальность нового имени (ошибки — через `ValueError`).
    """
    pass

def delete_habit(habit_id: int) -> bool:
    """
    Удаляет привычку из `habits_db` и возвращает `True` при успехе, `False`, если такой привычки нет.   
    """

def mark_habit(habit_id: int) -> dict | None:
    """
    Отмечает привычку за `TODAY`:
    - при отсутствии привычки возвращает `None`;
    - при повторной отметке за `TODAY` выбрасывает `ValueError`;
    - добавляет дату в `marks` и возвращает словарь с `id`, `name`, `last_marked_at` и актуальным `streak`.
    """

def is_habit_marked_today(habit_id: int) -> bool:
    """
    Отвечает, отмечена ли привычка за `TODAY` (используется во вьюхах для отображения кнопки/чекбокса).
    """
