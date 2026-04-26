# data/supabase_client.py
"""
ملف إدارة اتصال Supabase
مسؤول عن إنشاء وإدارة الاتصال بقاعدة البيانات
"""

import logging
from typing import Optional
from supabase import create_client, Client
from core.config import settings

print(settings.APP_NAME)
print(settings.SUPABASE_URL)# Logger
logger = logging.getLogger(__name__)

# متغير عام على مستوى الملف
_supabase_client: Optional[Client] = None


def init_supabase() -> Client:
    """
    تهيئة اتصال Supabase (تُنادى مرة واحدة في main.py)
    """
    global _supabase_client

    if _supabase_client is None:
        try:
            _supabase_client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_KEY
            )
            logger.info("✅ Supabase connected successfully")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Supabase: {e}")
            raise RuntimeError(f"Supabase initialization failed: {e}")

    return _supabase_client


def get_supabase() -> Client:
    """
    جلب اتصال Supabase من أي مكان في المشروع
    """
    if _supabase_client is None:
        raise RuntimeError(
            "Supabase not initialized. Call init_supabase() first in main.py"
        )
    return _supabase_client