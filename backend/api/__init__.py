"""HTTP-lagret: FastAPI-routers.

Routrarna validerar input med scheman från ``backend.schemas``, anropar rena
funktioner i ``backend.ml`` och läser/skriver via ``backend.db``. Ingen
ML-logik ligger här.
"""
