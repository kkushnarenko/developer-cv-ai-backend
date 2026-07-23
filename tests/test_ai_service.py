import pytest

from src.app.services.ai_services import ai_service
from src.app.core.config import config


@pytest.mark.asyncio
async def test_ai_service():
    if not config.GIGACHAT_CREDENTIALS:
        pytest.skip("Пропуск теста: GIGACHAT_CREDENTIALS не зафиксирован в .env")

    service = ai_service
    result = await service.analyze_and_respond(
        name="Тест",
        comments="Нам понравился ваш стек, хотим предложить проект"
    )

    assert "sentiment" in result
    assert "category" in result
    assert "auto_reply" in result
    assert "is_fallback" in result

    assert result["is_fallback"] is False
    assert result["sentiment"] in ["positive", "negative", "neutral"]
    assert len(result["auto_reply"]) > 0


