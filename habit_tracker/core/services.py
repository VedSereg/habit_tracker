from datetime import date, timedelta
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

def calculate_streak(marks: list[date]) -> int:
    """
    Рассчитывает *текущий* streak по датам в `marks` относительно `TODAY`.  
    Алгоритм в общих чертах:
    - пустой список -> streak = 0;
    - работай с отсортированным по убыванию набором уникальных дат;
    - если среди последних дат нет ни `TODAY`, ни вчерашнего дня -> streak = 0;
    - иначе отсчитывай подряд идущие дни назад (без пропусков) от `TODAY` или вчерашнего дня.
    """
    if not marks:
        return 0

    unique_marks = sorted(set(marks), reverse=True)

    yesterday = TODAY - timedelta(days=1)
    
    has_today = TODAY in unique_marks
    has_yesterday = yesterday in unique_marks
    
    if not has_today and not has_yesterday:
        return 0
    
    current_date = TODAY if has_today else yesterday
    streak = 0
    
    for date in unique_marks:
        if date == current_date:
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break
    return streak

def get_all_habits_with_details() -> list[dict]:
    """
    Возвращает список привычек, где для каждой привычки в словаре есть все её поля 
    (`id`, `name`, `marks` как список дат) **и** рассчитанный `streak`.  
    Список должен быть отсортирован по `id` (по возрастанию).  
    **Важно:** `marks` должен быть списком объектов `date`, так как в шаблонах 
    может использоваться форматирование дат.
    """
    result = []
    for habit_id in sorted(habits_db.keys()):
        habit = habits_db[habit_id]
        habit_dict = {}
        habit_dict["id"] = habit.id
        habit_dict["name"] = habit.name
        habit_dict["marks"] = habit.marks
        habit_dict["streak"] = calculate_streak(habit.marks)
        result.append(habit_dict)
    return result

def get_habit_by_id_with_details(habit_id: int) -> dict | None:
    """
    Возвращает одну привычку по `id` в виде словаря с полями привычки 
    (включая `id`, `name`, `marks` как список дат) и рассчитанным `streak`, 
    либо `None`, если привычки нет.  
    **Важно:** `marks` должен быть списком объектов `date`, а не строк, 
    так как в шаблонах используется `mark.strftime()
    """
    habit = habits_db.get(habit_id)
    if not habit:
        return None
    
    return {
        "id": habit.id,
        "name": habit.name,
        "marks": habit.marks,
        "streak": calculate_streak(habit.marks)
    }


def create_habit(habit_data: HabitCreate) -> Habit:
    """
    Создаёт новую привычку:
    - имя не должно быть пустым (валидация на уровне сервиса; при ошибке выбрасывается `ValueError`);
    - имя должно быть уникальным среди существующих привычек;
    - используется и увеличивается глобальная переменная `next_habit_id` (используй `global next_habit_id`).
    """
    global next_habit_id
    
    if not habit_data.name or not habit_data.name.strip():
        raise ValueError("Habit name cannot be empty.")

    for habit in habits_db.values():
        if habit.name.lower() == habit_data.name.lower():
            raise ValueError("Habit with this name already exists.")

    habit = Habit(id=next_habit_id, name=habit_data.name.strip())
    habits_db[next_habit_id] = habit
    next_habit_id += 1
    
    return habit


def update_habit(habit_id: int, habit_data: HabitUpdate) -> Habit | None:
    """
    Обновляет существующую привычку:
    - возвращает обновлённую привычку или `None`, если она не найдена;
    - проверяет непустое имя и уникальность нового имени (ошибки — через `ValueError`).
    """
    habit = habits_db.get(habit_id)
    if not habit:
        return None
    

    if not habit_data.name or not habit_data.name.strip():
        raise ValueError("Habit name cannot be empty.")
    
    new_name = habit_data.name.strip()
    
    for existing_habit in habits_db.values():
        if existing_habit.id != habit_id and existing_habit.name.lower() == new_name.lower():
            raise ValueError("Habit with this name already exists.")
    
    habit.name = new_name

    return habit

def delete_habit(habit_id: int) -> bool:
    """
    Удаляет привычку из `habits_db` и возвращает `True` при успехе, `False`, если такой привычки нет.   
    """
    if habit_id in habits_db:
        del habits_db[habit_id]
        return True
    else:
        return False

def mark_habit(habit_id: int) -> dict | None:
    """
    Отмечает привычку за `TODAY`:
    - при отсутствии привычки возвращает `None`;
    - при повторной отметке за `TODAY` выбрасывает `ValueError`;
    - добавляет дату в `marks` и возвращает словарь с `id`, `name`, `last_marked_at` и актуальным `streak`.
    """
    habit = habits_db.get(habit_id)
    if not habit:
        return None
    if TODAY in habit.marks:
        raise ValueError("Habit already marked for today.")
    
    habit.marks.append(TODAY)
    streak = calculate_streak(habit.marks)
    habit.streak = streak
    return {
        "id": habit.id,
        "name": habit.name,
        "last_marked_at": TODAY.isoformat(),
        "streak": streak
    }
        

def is_habit_marked_today(habit_id: int) -> bool:
    """
    Отвечает, отмечена ли привычка за `TODAY` (используется во вьюхах для отображения кнопки/чекбокса).
    """
    habit = habits_db.get(habit_id)
    if not habit:
        return False
    return TODAY in habit.marks
