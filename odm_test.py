from odmmanager import OdmManager
import asyncio
import concurrent.futures
from auth import (hostname, port, token)

async def wrapped_process_image():
    executor = concurrent.futures.ThreadPoolExecutor()
    await loop.run_in_executor(executor, om.processImages())

async def run():
    await wrapped_process_image()

if __name__== "__main__":
    om = OdmManager()
    om.config("images/*", token, hostname, port)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())