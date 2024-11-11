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


class Logger:
    # TODO: Different DBs
    def __init__(
        self,
        service_name,
        mongoURI=None,
        task_id=None,
        db_name="omni_logs",
        collection="logs",
        fallback_dir="cache_logs",
    ):
        load_dotenv()
        self.service_name = service_name
        self.task_id = task_id if task_id else str(uuid.uuid4())
        mongoURI = mongoURI or os.getenv("OMNILOG_MONGO")
        client = AsyncIOMotorClient(mongoURI)
        db = client[db_name]
        self.collection = db[collection]
        self.fallback_dir = fallback_dir

        if not os.path.exists(self.fallback_dir):
            os.makedirs(self.fallback_dir)

    async def started(self, message="", context=None):
        await self._log_with_status("Started", message, context)

    async def finished(self, message="", context=None):
        await self._log_with_status("Finished", message, context)

    async def error(self, message="", context=None):
        await self.log(log_level="CRITICAL", message=message, context=context)

    async def warning(self, message="", context=None):
        await self.log(log_level="WARNING", message=message, context=context)

    async def log(self, log_level="INFO", message="", context=None):
        frame = inspect.currentframe().f_back

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

    async def _log_with_status(self, status, message, context):
        await self.log(message=f"{message} {status}", context=context)
