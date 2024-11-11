import asyncio
import json
import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError


class Sync:
    ## TODO: Using Singleton
    def __init__(
        self,
        mongoURI=None,
        db_name="zira_logs",
        collection="logs",
        fallback_dir="cache_logs",
        sync_interval=10,
    ):
        load_dotenv()

        self.mongoURI = mongoURI or os.getenv("ZIRALOG_MONGO")
        self.client = AsyncIOMotorClient(self.mongoURI)
        self.db = self.client[db_name]
        self.collection = self.db[collection]
        self.fallback_dir = fallback_dir
        self.sync_interval = sync_interval

    async def sync_fallback_logs(self):
        """Sync local fallback logs to MongoDB when available."""
        for file_name in os.listdir(self.fallback_dir):
            if file_name.endswith(".json"):
                filepath = os.path.join(self.fallback_dir, file_name)
                try:
                    with open(filepath, "r") as f:
                        log_data = json.load(f)
                    await self.collection.insert_one(log_data)
                    os.remove(filepath)
                    print(f"Synced and removed local log: {file_name}")
                except PyMongoError as e:
                    print(f"Failed to sync log to MongoDB: {e}")
                    break
                except IOError as e:
                    print(f"Error reading local fallback log file: {e}")

    async def start_sync(self):
        await asyncio.create_task(self._periodic_sync())

    async def _periodic_sync(self):
        while True:
            await self.sync_fallback_logs()
            await asyncio.sleep(self.sync_interval)
