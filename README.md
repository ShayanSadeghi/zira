# Zira: Enhanced Event Tracking for Logging in Python

Zira designed to help developers efficiently track and understand the root cause of various events. It supports logging directly to MongoDB and offers local storage fallback if database connectivity is interrupted. Zira then syncs logs automatically once the database connection is restored, ensuring no data is lost.

## Installation

```bash
pip install zira
```

## Important Note:
To streamline your code, you can specify the `Mongo URI` in a `.env` file as the variable `ZIRALOG_MONGO`:

```python
# .env
ZIRALOG_MONGO='mongodb://user:pass@host:port/'

```

Alternatively, you can provide the Mongo URI directly when creating a `ZiraLog` or `Sync` instance:


```python

log_db_uri='mongodb://user:pass@host:port/'

zira = ZiraLog(mongoURI=log_db_uri, service_name="TestService", db_name="test_zira_log")

```


## Use Case Example


### Logging

```python
import asyncio

from zira.logger import ZiraLog 

async def main():
   zira = ZiraLog(service_name="TestService", db_name="test_zira_log")

   log_tasks = []
   log_tasks.append(zira.started(message="Test 1"))
   log_tasks.append(zira.warning(message="Test 2"))
   log_tasks.append(zira.error(message="Test 3"))
   log_tasks.append(zira.finished(message="Test 4"))

   await asyncio.gather(*log_tasks)

if __name__ == "__main__":
    asyncio.run(main())
```


### Syncing

If database connectivity is interrupted, use the `Sync` class to periodically sync stored logs with MongoDB.

```python
from zira.sync import Sync

zira_sync = Sync(db_name="test_zira_log", sync_interval=3600) #run every hour
await zira_sync.start_sync()
```