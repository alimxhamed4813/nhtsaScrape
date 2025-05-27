import asyncio

from scraper import execute


async def main():
  print("Executing NHTSA scraper...")
  await execute()


if __name__ == "__main__":
  asyncio.run(main())
