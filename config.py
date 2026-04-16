import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN   = os.getenv("BOT_TOKEN", "")
POLZA_KEY   = os.getenv("POLZA_KEY", "")
ADMIN_IDS   = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
STARS_PRICE = int(os.getenv("STARS_PRICE", "25"))
API_PORT    = int(os.getenv("API_PORT", "3000"))

WEBAPP_URL_FILE = os.getenv("WEBAPP_URL_FILE", ".tunnel_url")

def get_webapp_url():
    try:
        with open(WEBAPP_URL_FILE) as f:
            line = f.read().strip()
            return line.replace("TUNNEL_URL=", "")
    except:
        return os.getenv("WEBAPP_URL", "")

MODELS = {
    "x-ai/grok-4.1-fast":       {"icon": "⚡", "name": "Grok 4.1 Fast",     "desc": "Быстрый, прямолинейный"},
    "anthropic/claude-3-haiku": {"icon": "🔵", "name": "Claude 3 Haiku",    "desc": "Точный, понимает контекст"},
    "qwen/qwen3-32b":            {"icon": "🟠", "name": "Qwen3 32B",         "desc": "Логика и рассуждения"},
    "qwen/qwen3-30b-a3b":       {"icon": "🟡", "name": "Qwen3 30B A3B",     "desc": "MoE — быстрая и эффективная"},
    "qwen/qwen3-coder-flash":   {"icon": "🟢", "name": "Qwen3 Coder Flash", "desc": "Код и дебаггинг"},
}
