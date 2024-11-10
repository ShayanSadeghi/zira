import inspect
import os
import uuid
from datetime import datetime, timezone

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


class OmniLog:
    def __init__(
        self,
        service_name,
        mongoURI=None,
        task_id=None,
        db_name="omni_logs",
        collection="logs",
    ):
        load_dotenv()
        self.service_name = service_name
        self.task_id = task_id if task_id else str(uuid.uuid4())
        mongoURI = mongoURI or os.getenv("OMNILOG_MONGO")
        client = AsyncIOMotorClient(mongoURI)
        db = client[db_name]
        self.collection = db[collection]

    async def started(self, message="", context=None):
        await self._log_with_status("Started", message, context)

    async def finished(self, message="", context=None):
        await self._log_with_status("Finished", message, context)

    async def error(self, message="", context=None):
        await self.log(log_level="CRITICAL", message=message, context=context)

    async def warning(self, message="", context=None):
        await self.log(log_level="WARNING", message=message, context=context)

    async def log(self, log_level="INFO", message="", context=None):
        frame = inspect.currentframe().f_back()
        caller_info = {
            "function_name": frame.f_code.co_name,
            "file_name": frame.f_code.co_filename,
            "line_number": frame.f_lineno,
        }

        data = {
            "log_level": log_level,
            "message": message,
            "task_id": self.task_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service_name": self.service_name,
            **caller_info,
            "context": context or {},
        }

        try:
            await self.collection.insert_one(data)
        except Exception as e:
            print(f"Failed to log on MongoDB: {e}")

    async def _log_with_status(self, status, message, context):
        await self.log(message=f"{message} {status}", context=context)
