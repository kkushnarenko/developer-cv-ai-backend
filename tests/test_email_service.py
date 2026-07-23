from unittest.mock import AsyncMock, patch
import pytest

from src.app.services.email_service import email_service

@pytest.mark.asyncio
async def test_send_notifications_mocked():
    ai_result = {
        "sentiment": "positive",
        "category": "job_offer",
        "auto_reply": "Спасибо за предложение!",
        "is_fallback": False
    }

    mock_send = AsyncMock(return_value=None)

    with patch.object(email_service.fastmail, "send_message", mock_send):
        owner_res = await email_service.send_owner_notification(
            name="Алексей",
            email="test@example.com",
            phone="+79991234567",
            comments="Тестовое сообщение",
            ai_result=ai_result
        )

        user_res = await email_service.send_user_autoreply(
            user_email="test@example.com",
            user_name="Алексей",
            auto_reply_text=ai_result["auto_reply"]
        )

        assert owner_res is True
        assert user_res is True
        assert mock_send.call_count == 2

