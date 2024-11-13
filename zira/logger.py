import inspect
import json
import os
import uuid
from datetime import datetime, timezone

from bson import ObjectId
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)


class ZiraLog:
    # TODO: Different DBs
    def __init__(
        self,
        service_name,
        mongoURI=None,
        db_name="zira_logs",
        collection="logs",
        fallback_dir="cache_logs",
    ):
        load_dotenv()
        self.service_name = service_name
        mongoURI = mongoURI or os.getenv("ZIRALOG_MONGO")
        client = AsyncIOMotorClient(mongoURI)
        db = client[db_name]
        self.collection = db[collection]
        self.fallback_dir = fallback_dir

        if not os.path.exists(self.fallback_dir):
            os.makedirs(self.fallback_dir)

    async def started(self, message="", context=None):
        await self._log(message=f"{message} Started", context=context)

    async def finished(self, message="", context=None):
        await self._log(message=f"{message} Finished", context=context)

    async def error(self, message="", context=None):
        caller_info = self._get_caller_info()
        detailed_context = context or {}
        detailed_context = {**detailed_context, "caller_info": caller_info}
        await self._log(
            log_level="CRITICAL",
            message=message,
            context=detailed_context,
        )

    async def warning(self, message="", context=None):
        await self._log(log_level="WARNING", message=message, context=context)

    async def _log(self, log_level="INFO", message="", context=None):
        utc_time = datetime.now(timezone.utc)
        data = {
            "log_level": log_level,
            "message": message,
            "datetime": utc_time.isoformat(),
            "timestamp": utc_time.timestamp(),
            "service_name": self.service_name,
            "context": context or {},
        }

        try:
            await self.collection.insert_one(data)
        except PyMongoError:
            if self.fallback_dir:
                self._log_to_local_fallback(data)
            else:
                print("Failed to log on MongoDB")

    def _log_to_local_fallback(self, log_data):
        file_name = os.path.join(self.fallback_dir, f"log_{uuid.uuid4()}.json")
        try:
            with open(file_name, "w") as f:
                json.dump(log_data, f, cls=CustomJSONEncoder)
            print(f"Saved log to local fallback: {file_name}")
        except IOError as e:
            print(f"Failed to write to local fallback file: {e}")

    def _get_caller_info(self):
        stack = inspect.stack()

        caller_info = [
            {
                "function_name": caller_frame.function,
                "file_name": caller_frame.filename,
                "line_number": caller_frame.lineno,
            }
            for caller_frame in stack
        ]
        return caller_info
