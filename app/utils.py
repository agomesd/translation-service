import anthropic
from sqlalchemy.orm import Session
from crud import update_translation_task
from dotenv import load_dotenv

import os
load_dotenv()

ANT_API_KEY = os.getenv("ANT_API_KEY")

async def translate_text(task_id: int, text: str, language: str, db: Session) -> str:
   client = anthropic.Anthropic(
       api_key=ANT_API_KEY
   )
   
   message = client.messages.create(
       model="claude-3-5-sonnet-20241022",
       max_tokens=1024,
       messages=[
           {"role": "assistant", "content": f"You are a helpful assistand to translate to {language}"},
           {"role": "user", "content": text}
       ]
   )
   translation = message.content[0].text
   update_translation_task(db, task_id, translation)
