import asyncio
import datetime
from judobase import JudoBase
from databaseConnection.connection import execute_query


async def insert_competitions():
    async with JudoBase() as api:
        competitions = await api.get_competition_list()

        data = []
        for comp in competitions:
            comp_details = await api.get_competition_info(comp.id_competition)

            ages = ','.join(comp.ages) if isinstance(comp.ages, list) else comp.ages or ""
            updated_at = comp_details.updated_at if comp_details.updated_at else datetime.datetime.now()
            data.append((
                comp_details.id_competition,
                ages,
                comp_details.city or "",
                getattr(comp_details, 'code_live_theme'),
                getattr(comp, 'comp_year'),
                getattr(comp, 'continent_short', ),
                comp_details.country or "",
                getattr(comp_details, 'country_short', ""),
                comp_details.date_from.strftime('%Y-%m-%d %H:%M:%S') if comp_details.date_from else None,
                comp_details.date_to.strftime('%Y-%m-%d %H:%M:%S') if comp_details.date_to else None,
                getattr(comp_details, 'external_id', ""),
                int(getattr(comp_details, 'has_logo', 0)),
                int(comp_details.has_results) if comp_details.has_results is not None else 0,
                int(getattr(comp_details, 'id_country', 0)),
                int(comp_details.id_draw_type) if comp_details.id_draw_type is not None else 0,  # Handle None
                int(getattr(comp_details, 'id_live_theme', 0)),
                int(getattr(comp_details, 'is_teams', 0)),
                comp_details.name or "",
                int(comp.prime_event) if comp.prime_event is not None else 0,
                getattr(comp, 'rank_name'),
                getattr(comp, 'status'),
                getattr(comp, 'street'),
                getattr(comp, 'street_no'),
                getattr(comp_details, 'timezone',),
                updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                comp_details.date_to.strftime('%Y-%m-%d %H:%M:%S') if comp_details.date_to else None
            ))

        insert_query = """
        INSERT INTO Competition (
            id_competition, ages, city, code_live_theme, comp_year, continent_short, country, country_short,
            date_from, date_to, external_id, has_logo, has_results, id_country, id_draw_type, id_live_theme,
            is_teams, name, prime_event, rank_name, status, street, street_no, timezone, updated_at, updated_at_ts
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        ) AS new
        ON DUPLICATE KEY UPDATE
            ages = new.ages,
            city = new.city,
            code_live_theme = new.code_live_theme,
            comp_year = new.comp_year,
            continent_short = new.continent_short,
            country = new.country,
            country_short = new.country_short,
            date_from = new.date_from,
            date_to = new.date_to,
            external_id = new.external_id,
            has_logo = new.has_logo,
            has_results = new.has_results,
            id_country = new.id_country,
            id_draw_type = new.id_draw_type,
            id_live_theme = new.id_live_theme,
            is_teams = new.is_teams,
            name = new.name,
            prime_event = new.prime_event,
            rank_name = new.rank_name,
            status = new.status,
            street = new.street,
            street_no = new.street_no,
            timezone = new.timezone,
            updated_at = new.updated_at,
            updated_at_ts = new.updated_at_ts
        """

        await execute_query(insert_query, data, many=True)

async def insert_judokas():
    async with JudoBase() as api:
        # Step 1: Fetch all Judokas
        judokas = await api.get_judoka_list()

        data = []
        for judoka in judokas:
            # Step 2: Fetch detailed info for each Judoka
            judoka_details = await api.get_judoka_info(judoka.id_person)

            # Step 3: Prepare data for insertion
            data.append((
                judoka_details.family_name,
                judoka_details.middle_name,
                judoka_details.given_name,
                judoka_details.family_name_local,
                judoka_details.middle_name_local,
                judoka_details.given_name_local,
                judoka_details.short_name,
                judoka_details.gender,
                judoka_details.folder,
                judoka_details.picture_filename,
                judoka_details.ftechique,
                judoka_details.side,
                judoka_details.coach,
                judoka_details.best_result,
                judoka_details.height,
                judoka_details.birth_date.strftime('%Y-%m-%d') if judoka_details.birth_date else None,
                judoka_details.country,
                judoka_details.id_country,
                judoka_details.country_short,
                judoka_details.file_flag,
                judoka_details.club,
                judoka_details.belt,
                judoka_details.youtube_links,
                judoka_details.status,
                judoka_details.archived,
                ','.join(judoka_details.categories) if judoka_details.categories else None,
                judoka_details.dob_year,
                judoka_details.age,
                judoka_details.death_age,
                judoka_details.personal_picture,
            ))

        # Step 4: Insert into the database
        insert_query = """
        INSERT INTO Judoka (
            family_name, middle_name, given_name, family_name_local, middle_name_local, given_name_local,
            short_name, gender, folder, picture_filename, ftechique, side, coach, best_result, height,
            birth_date, country, id_country, country_short, file_flag, club, belt, youtube_links, status,
            archived, categories, dob_year, age, death_age, personal_picture
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s
        ) AS new
        ON DUPLICATE KEY UPDATE
            family_name = new.family_name,
            middle_name = new.middle_name,
            given_name = new.given_name,
            family_name_local = new.family_name_local,
            middle_name_local = new.middle_name_local,
            given_name_local = new.given_name_local,
            short_name = new.short_name,
            gender = new.gender,
            folder = new.folder,
            picture_filename = new.picture_filename,
            ftechique = new.ftechique,
            side = new.side,
            coach = new.coach,
            best_result = new.best_result,
            height = new.height,
            birth_date = new.birth_date,
            country = new.country,
            id_country = new.id_country,
            country_short = new.country_short,
            file_flag = new.file_flag,
            club = new.club,
            belt = new.belt,
            youtube_links = new.youtube_links,
            status = new.status,
            archived = new.archived,
            categories = new.categories,
            dob_year = new.dob_year,
            age = new.age,
            death_age = new.death_age,
            personal_picture = new.personal_picture
        """

        await execute_query(insert_query, data, many=True)

async def main():
    await insert_competitions()
    await insert_judokas()

asyncio.run(main())
