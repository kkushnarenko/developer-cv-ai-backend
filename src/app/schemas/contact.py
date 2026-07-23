import re
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

class ContactFormRequest(BaseModel):
    name : str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Имя отправителя",
        examples=["Алексей"]
    )
    email : EmailStr = Field(
        description="Email для обратной связи",
        examples=["example@gmail.cpm"]
    )
    phone : Optional[str] = Field(
        None,
        description="Номер телефона (необязательное поле)",
        examples=["+79991234567"]
    )
    comments : str = Field(
        min_length=5,
        max_length=2000,
        description="Текст обращения/комментария",
        examples=["Здравствуйте! Хотим предложить вам участие в проекте."]
    )

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: Optional[str]) -> Optional[str]:
        if value is None or value.strip() == "":
            return None

        cleaned_value = re.sub(r"[\s\-\(\)]", "", value)

        if not re.match(r"^\+?[0-9]{10,15}$", cleaned_value):
            raise ValueError("Некорректный формат номера телефона. Ожидается от 10 до 15 цифр.")
        return cleaned_value
    