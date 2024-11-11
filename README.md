# Zira

Zira will help you during the logging process. 

Currently this package try to log on a mongo db using mongo URI.

## Use Case Example

```bash
pip install zira
```

### Logging

```python
import asyncio

from Zira.logger import ZiraLog 

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

To sync logs, that stored on local storage due to any interrupt of database connection, use the Sync class:

```python
from src.sync import Sync

zira_sync = Sync(db_name="test_zira_log", sync_interval=3600) #run every hour
await zira_sync.start_sync()
```