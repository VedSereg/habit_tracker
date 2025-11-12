from fastapi import FastAPI
from habit_tracker.api import habits

# TODO: Создать экземпляр FastAPI
# TODO: Подключить роутер
app = FastAPI(title="Habit Tracker API")

app.include_router(habits.router)

