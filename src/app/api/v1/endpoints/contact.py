from fastapi import APIRouter, Request, status
from loguru import logger

from src.app.schemas.contact import ContactFormRequest
from src.app.services.ai_services import ai_service
from src.app.services.email_service import email_service
from src.app.services.stats_service import stats_service
from src.app.core.limiter import limiter


router = APIRouter(tags=["Contact"])

@router.post("/api/contact", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")  # Защита от спама (5 запросов в минуту с 1 IP)
async def handle_contact_form(request: Request, form_data: ContactFormRequest):
    logger.info(f"Получено новое обращение от {form_data.name} ({form_data.email})")


    ai_result = await ai_service.analyze_and_respond(
        name=form_data.name,
        comments=form_data.comments
    )


    stats_service.update_stats(
        category=ai_result.get("category", "unknown"),
        sentiment=ai_result.get("sentiment", "unknown")
    )


    await email_service.send_owner_notification(
        name=form_data.name,
        email=form_data.email,
        phone=form_data.phone,
        comments=form_data.comments,
        ai_result=ai_result
    )

    await email_service.send_user_autoreply(
        user_email=form_data.email,
        user_name=form_data.name,
        auto_reply_text=ai_result["auto_reply"]
    )

    return {
        "status": "success",
        "message": "Ваше обращение успешно обработано!"
    }