import json
from pathlib import Path
from loguru import logger

STATS_FILE = Path("data/stats.json")

class StatsService:
    def __init__(self):
        STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not STATS_FILE.is_file():
            self.write_stats({"total_requests": 0, "categories": {}, "sentiments": {}})

    def get_stats(self) -> dict:
        try:
            with open(STATS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Ошибка чтения статистики: {e}")
            return {}

    def write_stats(self, data : dict):
        with open(STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def update_stats(self, category: str, sentiment: str):
        try:
            stats = self.get_stats()

            stats["total_requests"] = stats.get("total_requests", 0) + 1

            cat_count = stats.get("categories", {}).get(category, 0)
            stats.setdefault("categories", {})[category] = cat_count + 1

            sent_count = stats.get("sentiments", {}).get(sentiment, 0)
            stats.setdefault("sentiments", {})[sentiment] = sent_count + 1

            self.write_stats(stats)

        except Exception as e:
            logger.error(f"Ошибка обновления статистики: {e}")


stats_service = StatsService()