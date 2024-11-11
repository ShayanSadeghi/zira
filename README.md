# OLLO

OLLO will help you during the logging process. 

Currently this package try to log on a mongo db using mongo URI.

## Use Case Example

```bash
pip install ollo
```

### logging

```python
import asyncio

from OllO.logger import Logger 

async def main():
   ollo = Logger(service_name="TestService", db_name="test_omni_log")

   log_tasks = []
   log_tasks.append(ollo.started(message="Test log message"))
   log_tasks.append(ollo.warning(message="Warning message"))
   log_tasks.append(ollo.error(message="Error message"))
   log_tasks.append(ollo.finished(message="Error message"))

   await asyncio.gather(*log_tasks)

if __name__ == "__main__":
    asyncio.run(main())
```