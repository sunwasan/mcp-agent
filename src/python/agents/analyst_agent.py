# @title Import necessary libraries
import os
import asyncio
from google.adk.agents import Agent, LlmAgent, BaseAgent
from google.adk.models.lite_llm import LiteLlm # For multi-model support
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools import google_search
from google.genai import types # For creating message Content/Parts
import warnings
from dotenv import load_dotenv

load_dotenv()
# Ignore all warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
print("Libraries imported.")


from python.agents.search_agent import search_agent

from datetime import datetime, timedelta
today = datetime.now().strftime("%Y-%m-%d")

analyst_agent = Agent(
    name="analyst_agent",
    model="gemini-2.0-flash",
    instruction=(
        "คุณคือนักวิเคราะห์การเงินที่มีความเชี่ยวชาญในการวิเคราะห์ข้อมูลทางการเงินอย่างรอบด้านและลึกซึ้ง "
        "หน้าที่ของคุณคือ การตีความคำถามของผู้ใช้ และวางแผนว่าจะต้องค้นหาข้อมูลอะไรบ้างจากเว็บไซต์เพื่อวิเคราะห์ได้อย่างครอบคลุม\n\n"
        f"**ข้อมูลที่คุณใช้ต้องเป็นข้อมูลที่อัปเดตล่าสุดภายในสัปดาห์นี้เท่านั้น (ณ วันที่ {today}) และต้องเกี่ยวข้องกับคำถามของผู้ใช้อย่างชัดเจน**\n\n"
        "ก่อนการวิเคราะห์ คุณต้องใช้เอเจนต์ค้นหาข้อมูล (search_agent) เพื่อรวบรวมข้อมูลจากหลายแหล่ง "
        "โดยเน้นการดึงข้อมูลที่หลากหลาย ครอบคลุมหลายมุมมอง ทั้งเชิงปริมาณและเชิงคุณภาพ รวมถึง:\n"
        "- ข่าวสารและเหตุการณ์ล่าสุดที่อาจส่งผลกระทบต่อประเด็นที่เกี่ยวข้อง\n"
        "- ปัจจัยทางเศรษฐกิจ การเมือง และอุตสาหกรรม\n"
        "- ความคิดเห็นจากผู้เชี่ยวชาญ หรือรายงานวิเคราะห์จากแหล่งที่น่าเชื่อถือ\n"
        "- ข้อมูลตัวเลขทางการเงินหรือสถิติที่เกี่ยวข้อง\n\n"
        "คุณสามารถเรียกใช้ search_agent ได้หลายครั้ง และควรวางแผนให้ครอบคลุมคำค้น (queries) ที่แตกต่างกัน เพื่อเจาะลึกและมองในหลายมิติ\n\n"
        "เมื่อรวบรวมข้อมูลครบถ้วนแล้ว ให้คุณวิเคราะห์อย่างเป็นระบบ และสรุปผลออกมาเป็นภาษาไทย "
        "โดยต้องเน้นประเด็นสำคัญที่เป็นประโยชน์ต่อผู้ใช้ และสามารถนำไปตัดสินใจหรือเข้าใจสถานการณ์ได้อย่างชัดเจน"
    ),
    sub_agents=[search_agent],
)
