import asyncio
from judobase import JudoBase

# Example usage of JudoBase to get a list of competitors
async def test_get_list():
    async with JudoBase() as api:
        try:
            data = await api._get_json({
                "params[action]": "competitor.get_list",
                "params[limit]": 5,
            })
            print("Success:", data)
        except Exception as e:
            print("Error:", e)


asyncio.run(test_get_list())

# Test fetching info for a single judoka using their ID
async def test_get_judoka_info():
    async with JudoBase() as api:
        try:
            data = await api.get_judoka_info("2")
            print("Judoka Info:")
            print(data)
        except Exception as e:
            print("Error fetching judoka info:", e)

asyncio.run(test_get_judoka_info())
