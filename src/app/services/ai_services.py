import json
from typing import Any, Dict
from gigachat import GigaChat

from loguru import logger


from src.app.core.config import config


class AIService:
    def __init__(self):
        self._init_client()

    def _init_client(self):
        if config.GIGACHAT_CREDENTIALS and config.GIGACHAT_CREDENTIALS.strip():
            try:
                self.client = GigaChat(
                    credentials=config.GIGACHAT_CREDENTIALS,
                    scope=config.GIGACHAT_SCOPE,
                    verify_ssl_certs=False
                )
            except Exception as e:
                logger.error(f"Ошибка инициализации GigaChat: {e}")
                self.client = None
        else:
            self.client = None

    async def analyze_and_respond(self, name: str, comments: str,) -> Dict[str, Any]:
        if not self.client:
            logger.warning("Клиент ИИ не настроен. Возвращается fallback ответ.")
            return self.get_feelback_responce(name)

        system_prompt = (
            "Ты — AI-ассистент на личном сайте разработчика. "
            "Проанализируй сообщение от посетителя и сформируй ответ.\n"
            "Верни ответ СТРОГО в формате JSON со следующими полями:\n"
            "1. 'sentiment': тональность ('positive', 'neutral', 'negative')\n"
            "2. 'category': тип запроса ('job_offer', 'question', 'collaboration', 'other')\n"
            "3. 'auto_reply': вежливый и короткий авто-ответ на русском языке (2-3 предложения).\n")

        user_prompt = f"Имя отправителя {name}\n Сообщение: {comments}"

        try:
            response = await self.client.achat(system_prompt)
            raw_content = response.choices[0].message.content
            clean_json = raw_content.replace("```json", "").replace("```", "").strip()
            parsed_content = json.loads(clean_json)
            logger.info(f"Анализ с помощью ИИ успешно выполнен для пользователя «{name}»")
            return {
                "sentiment": parsed_content.get("sentiment", "neutral"),
                "category": parsed_content.get("category", "other"),
                "auto_reply": parsed_content.get("auto_reply", f"Здравствуйте, {name}! Спасибо за обращение."),
                "is_fallback": False
            }
        except Exception as e:
            logger.error(e)
            return self.get_feelback_responce(name)



    def get_feelback_responce(self, name : str) -> Dict[str, Any]:
        return {
            "sentiment": "unknown",
            "category": "general",
            "auto_reply": f"Здравствуйте, {name}! Ваше обращение получено. Я отвечу вам в ближайшее время.",
            "is_fallback": True
        }

ai_service = AIService()