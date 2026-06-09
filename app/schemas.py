from email_validator import EmailNotValidError, validate_email
from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError

from app.messages import VALIDATION


def _invalid(code: str, message: str) -> None:
    raise PydanticCustomError(code, message)


class ContactForm(BaseModel):
    name: str
    email: str
    subject: str
    message: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            _invalid("name_too_short", VALIDATION["name"])
        return v

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, v: object) -> str:
        if not isinstance(v, str):
            _invalid("email_invalid", VALIDATION["email"])
        v = v.strip().lower()
        try:
            result = validate_email(v, check_deliverability=False)
        except EmailNotValidError:
            _invalid("email_invalid", VALIDATION["email"])
        return result.normalized

    @field_validator("subject")
    @classmethod
    def validate_subject(cls, v: str) -> str:
        v = v.strip()
        if not v:
            _invalid("subject_required", VALIDATION["subject"])
        return v

    @field_validator("message")
    @classmethod
    def validate_message(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 10:
            _invalid("message_too_short", VALIDATION["message"])
        return v
