"""CRUD module"""
from app.crud.crud_user import crud_user
from app.crud.crud_field import crud_field
from app.crud.crud_section import crud_section
from app.crud.crud_schedule import crud_schedule
from app.crud.crud_record import crud_record
from app.crud.crud_photo import crud_photo
from app.crud.crud_share import crud_share
from app.crud.crud_weather import crud_weather

__all__ = [
    "crud_user",
    "crud_field",
    "crud_section",
    "crud_schedule",
    "crud_record",
    "crud_photo",
    "crud_share",
    "crud_weather",
]
