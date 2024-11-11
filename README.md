# Zira

Zira will help you during the logging process. 

Currently this package try to log on a mongo db using mongo URI.

## Use Case Example

```bash
pip install zira
```

### logging

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