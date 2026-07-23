from email.message import EmailMessage
from typing import Any, Dict
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from loguru import logger

from src.app.core.config import config


class EmailService:
    def __init__(self):
        self.config = ConnectionConfig(
            MAIL_USERNAME=config.MAIL_USERNAME,
            MAIL_PASSWORD=config.MAIL_PASSWORD,
            MAIL_FROM=config.MAIL_FROM,
            MAIL_PORT=config.MAIL_PORT,
            MAIL_SERVER=config.MAIL_SERVER,
            MAIL_FROM_NAME=config.MAIL_FROM_NAME,
            MAIL_STARTTLS=False,
            MAIL_SSL_TLS=True,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )
        self.fastmail = FastMail(self.config)

    async def send_owner_notification(self, name: str,
        email: str,
        phone: str | None,
        comments: str,
        ai_result: Dict[str, Any]
    ) -> bool:
        subject = f"Новое обращение с сайта от {name} "

        body_text = (
            f"Новая заявка на сайте!\n\n"
            f"Имя: {name}\n"
            f"Email: {email}\n"
            f"Телефон: {phone or 'Не указан'}\n"
            f"Комментарий: {comments}\n\n"
            f"--- Анализ ИИ (GigaChat) ---\n"
            f"Тональность: {ai_result.get('sentiment')}\n"
            f"Категория: {ai_result.get('category')}\n"
            f"Сгенерированный авто-ответ: {ai_result.get('auto_reply')}\n"
            f"Fallback режим: {ai_result.get('is_fallback')}"
        )

        message = MessageSchema(
            subject=subject,
            recipients=[config.ADMIN_EMAIL or config.MAIL_FROM],
            body=body_text,
            subtype=MessageType.plain
        )
        try:
            await self.fastmail.send_message(message)
            logger.info(f"Уведомление отправлено на этот адреc {config.ADMIN_EMAIL}")
            return True
        except Exception as e:
            logger.error(e)
            return False

    async def send_user_autoreply(self,
        user_email: str,
        user_name: str,
        auto_reply_text: str
    ) -> bool:
        subject = f"Спасибо за ваше обраще {user_name} "

        body_text = (f"Здравствуйте, {user_name}!\n\n"
            f"{auto_reply_text}\n\n"
            f"С уважением,\n"
            f"Команда разработки"
        )

        message = MessageSchema(
            subject=subject,
            recipients=[user_email],
            body=body_text,
            subtype=MessageType.plain
        )
        try:
            await self.fastmail.send_message(message)
            logger.info(f"Авто-ответ пользователю отправлен на {user_email}")
            return True
        except Exception as e:
            logger.error(e)
            return False

email_service = EmailService()

