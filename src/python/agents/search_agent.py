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


from python.tools.craw4ai import crawl
from python.tools.webscraper import web_grounding


from datetime import datetime, timedelta
today = datetime.now().strftime("%Y-%m-%d")

search_agent = Agent(
    name="search_agent",
    model="gemini-2.0-flash",
    instruction=(
        "ค้นหาข้อมูลที่เกี่ยวข้องมากที่สุดจากเว็บไซต์ และสรุปผลในบริบทที่เป็นประโยชน์ต่อผู้ใช้ "
        f"โดยข้อมูลต้องเป็นข้อมูลล่าสุดภายในสัปดาห์นี้เท่านั้น (อัปเดต ณ วันที่ {today}) และต้องระบุช่วงเวลาให้ชัดเจนใน query\n\n"
        "คำค้น (query) ต้องมีลักษณะดังนี้:\n"
        "- เป็นคำถามที่ชัดเจน เข้าใจง่าย ไม่กำกวม\n"
        "ให้ใช้เครื่องมือต่อไปนี้อย่างเต็มประสิทธิภาพ:\n"
        "- เรียกใช้ `web_grounding(query: str)` อย่างน้อย 2 ครั้ง โดยเปลี่ยนคำค้นหรือขยายประเด็นเพื่อให้ได้ข้อมูลที่หลากหลาย\n"
        "- หลังจาก web_grounding เลือก URL ที่เกี่ยวข้องมากที่สุด 2-3 URL\n"
        "- ใช้ `crawl(url: str)` เพื่อดึงข้อมูลจาก URL ที่เลือก\n"
        "เมื่อรวบรวมข้อมูลจากหลายแหล่งแล้ว ให้:\n"
        "- วิเคราะห์เนื้อหาจากแต่ละแหล่งเพื่อกรองข้อมูลที่ถูกต้อง ทันสมัย และมีคุณค่า\n"
        "- สรุปผลเป็นภาษาไทยอย่างกระชับ พร้อมเน้นประเด็นที่สามารถนำไปใช้ได้จริง และเหมาะสมกับบริบทของคำถาม"
    ),
    description="ตัวช่วยค้นหาข้อมูลเชิงลึกจากเว็บไซต์โดยใช้การค้นหาและดึงข้อมูลแบบเข้มข้น",
    tools=[web_grounding, crawl],
)

