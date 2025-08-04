import asyncio
from judobase import JudoBase
from databaseConnection.connection import execute_query


async def insert_countryshort_into_db():
    async with JudoBase() as api:
        countries_short = await api.all_countries()

        # Prepare data for insertion
        data = []
        for country in countries_short:
            data.append((
                country.id_country,
                country.name,
                country.ioc))

        # SQL query for insertion
        insert_query = """
        INSERT INTO CountryShort (
        id, name, ioc
        )
        VALUES (
        %s, %s, %s
        ) AS new
        ON DUPLICATE KEY UPDATE
            id = new.id,
            name = new.name,
            ioc = new.ioc
        """

        # Execute the query
        await execute_query(insert_query, data, many=True)

async def insert_country_into_db():
    async with JudoBase() as api:
        countries = await api.all_countries()

        # Prepare data for insertion
        data = []
        for country in countries:
            data.append((
                country.id_country,
                country.name,
                country.ioc,
                country.flag_url))

        # SQL query for insertion
        insert_query = """
        INSERT INTO Country (
        
        )VALUES (
        ) AS new
        ON DUPLICATE KEY UPDATE
        
        """

        # Execute the query
        await execute_query(insert_query, data, many=True)

async def main():
    await insert_countryshort_into_db()


asyncio.run(main())
