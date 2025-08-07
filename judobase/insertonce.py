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


async def insert_countries_into_db():
    async with JudoBase() as api:
        countries_short = await api.get_country_list()
        country_data = []

        for country_short in countries_short:
            try:
                country_info = await api.get_country_info(country_short.id_country)

                if isinstance(country_info.president_name, dict):
                    president_str = country_info.president_name.get("president_name")
                elif isinstance(country_info.president_name, str):
                    president_str = country_info.president_name
                else:
                    president_str = None

                # Prepare data for insertion
                country_data.append((
                    country_info.id_country,
                    country_info.org_name,
                    country_info.org_www,
                    country_info.head_address or None,
                    country_info.head_city or None,
                    country_info.contact_phone or None,
                    country_info.contact_email or None,
                    country_info.exclude_from_medals,
                    president_str,
                    country_info.male_competitiors if country_info.male_competitiors != 0 else None,
                    country_info.female_competitiors if country_info.female_competitiors != 0 else None,
                    country_info.total_competitors,
                    country_info.number_of_competitions,
                    country_info.number_of_total_competitions,
                    country_info.number_of_total_wins,
                    country_info.number_of_total_fights,
                    country_info.best_male_competitor.get("id_person") if country_info.best_male_competitor else None,
                    country_info.best_female_competitor.get(
                        "id_person") if country_info.best_female_competitor else None,
                    country_info.total_ranking_points,
                    country_info.ranking_male.get("points") if country_info.ranking_male else None,
                    country_info.ranking_female.get("points") if country_info.ranking_female else None,
                    country_info.ranking.get("place") if country_info.ranking else None,
                    country_info.ranking_male.get("place") if country_info.ranking_male else None,
                    country_info.ranking_female.get("place") if country_info.ranking_female else None,
                ))
            except Exception as e:
                print(f"Error processing country ID {country_short.id_country}: {e} ")

        # Insert into DB
        country_query = """
        INSERT INTO Country (
            id_country, org_name, org_www, head_address, head_city, contact_phone, contact_email,
            exclude_from_medals, president_name, male_competitors, female_competitors, total_competitors,
            number_of_competitions, number_of_total_competitions, number_of_total_wins, number_of_total_fights,
            best_male_competitor_id, best_female_competitor_id, total_ranking_points, ranking_points_male,
            ranking_points_female, total_ranking_place, ranking_place_male, ranking_place_female
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        ) AS new
        ON DUPLICATE KEY UPDATE
            org_name = new.org_name,
            org_www = new.org_www,
            head_address = new.head_address,
            head_city = new.head_city,
            contact_phone = new.contact_phone,
            contact_email = new.contact_email,
            exclude_from_medals = new.exclude_from_medals,
            president_name = new.president_name,
            male_competitors = new.male_competitors,
            female_competitors = new.female_competitors,
            total_competitors = new.total_competitors,
            number_of_competitions = new.number_of_competitions,
            number_of_total_competitions = new.number_of_total_competitions,
            number_of_total_wins = new.number_of_total_wins,
            number_of_total_fights = new.number_of_total_fights,
            best_male_competitor_id = new.best_male_competitor_id,
            best_female_competitor_id = new.best_female_competitor_id,
            total_ranking_points = new.total_ranking_points,
            ranking_points_male = new.ranking_points_male,
            ranking_points_female = new.ranking_points_female,
            total_ranking_place = new.total_ranking_place,
            ranking_place_male = new.ranking_place_male,
            ranking_place_female = new.ranking_place_female
        """
        await execute_query(country_query, country_data, many=True)


async def main():
    await insert_countryshort_into_db()
    await insert_countries_into_db()


asyncio.run(main())
