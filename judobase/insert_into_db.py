import asyncio
import datetime
from judobase import JudoBase
from databaseConnection.connection import execute_query
from databaseConnection.connection import fetch_all


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
                int(getattr(comp, 'has_logo', 0)),
                int(comp.has_results) if comp.has_results is not None else 0,
                int(getattr(comp_details, 'id_country', 0)),
                int(comp.id_draw_type) if comp.id_draw_type is not None else 0,
                int(getattr(comp_details, 'id_live_theme', 0)),
                int(getattr(comp, 'is_teams', 0)),
                comp_details.name or "",
                int(comp.prime_event) if comp.prime_event is not None else 0,
                getattr(comp, 'rank_name'),
                getattr(comp, 'status'),
                getattr(comp, 'street'),
                getattr(comp, 'street_no'),
                getattr(comp_details, 'timezone', ),
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


async def fetch_all_contests_from_db():
    query = """
    SELECT id_person_blue, id_person_white
    FROM Contest
    """
    return await fetch_all(query)


async def insert_judokas():
    # Step 1: Fetch all contests from the database
    contests = await fetch_all_contests_from_db()

    # Step 2: Extract unique judoka IDs
    judoka_ids = set()
    for contest in contests:
        judoka_ids.add(contest[0])
        judoka_ids.add(contest[1])

    # Step 3: Fetch detailed info for each Judoka
    async with JudoBase() as api:
        data = []
        for judoka_id in judoka_ids:
            judoka_details = await api.get_judoka_info(judoka_id)
            data.append((
                judoka_id,  # Use judoka_id as the id in the database
                judoka_details.age,
                judoka_details.archived or 0,
                judoka_details.belt or '',
                judoka_details.best_result or '',
                judoka_details.birth_date.strftime('%Y-%m-%d') if judoka_details.birth_date else None,
                ','.join(judoka_details.categories) if judoka_details.categories else None,
                judoka_details.club or '',
                judoka_details.coach or None,
                judoka_details.country or '',
                judoka_details.country_short or '',
                judoka_details.death_age or None,
                judoka_details.dob_year or None,
                judoka_details.family_name or '',
                judoka_details.family_name_local or '',
                judoka_details.file_flag,
                judoka_details.folder or '',
                judoka_details.ftechique or '',
                judoka_details.gender or '',
                judoka_details.given_name or '',
                judoka_details.given_name_local or '',
                judoka_details.height or None,
                judoka_details.id_country or None,
                judoka_details.middle_name or '',
                judoka_details.middle_name_local or '',
                judoka_details.personal_picture or '',
                judoka_details.picture_filename or '',
                judoka_details.short_name or '',
                judoka_details.side or None,
                judoka_details.status or 0,
                judoka_details.youtube_links or '',
            ))

        # Step 4: Insert into the database
        insert_query = """
        INSERT INTO Judoka (
            id, age, archived, belt, best_result, birth_date, categories, club, coach, country,
            country_short, death_age, dob_year, family_name, family_name_local, file_flag, folder,
            ftechique, gender, given_name, given_name_local, height, id_country, middle_name,
            middle_name_local, personal_picture, picture_filename, short_name, side, status, youtube_links
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s
        ) AS new
        ON DUPLICATE KEY UPDATE
            age = new.age,
            archived = new.archived,
            belt = new.belt,
            best_result = new.best_result,
            birth_date = new.birth_date,
            categories = new.categories,
            club = new.club,
            coach = new.coach,
            country = new.country,
            country_short = new.country_short,
            death_age = new.death_age,
            dob_year = new.dob_year,
            family_name = new.family_name,
            family_name_local = new.family_name_local,
            file_flag = new.file_flag,
            folder = new.folder,
            ftechique = new.ftechique,
            gender = new.gender,
            given_name = new.given_name,
            given_name_local = new.given_name_local,
            height = new.height,
            id_country = new.id_country,
            middle_name = new.middle_name,
            middle_name_local = new.middle_name_local,
            personal_picture = new.personal_picture,
            picture_filename = new.picture_filename,
            short_name = new.short_name,
            side = new.side,
            status = new.status,
            youtube_links = new.youtube_links
        """

        await execute_query(insert_query, data, many=True)


async def insert_contests_into_db():
    async with JudoBase() as api:
        # Step 1: Fetch all contests
        contests = await api.all_contests()

        # Step 2: Prepare data for insertion
        data = []
        for contest in contests:
            data.append((
                contest.id_fight,
                contest.id_competition,
                contest.id_person_blue,
                contest.id_person_white,
                contest.id_weight,
                contest.age,
                contest.bye,
                contest.contest_code_long,
                contest.date_start_ts.strftime('%Y-%m-%d %H:%M:%S'),
                contest.duration,
                ','.join([event.dict() for event in contest.events]) if contest.events else None,
                contest.fight_duration,
                contest.fight_no,
                contest.first_hajime_at_ts.strftime('%Y-%m-%d %H:%M:%S'),
                contest.gs,
                contest.hsk_b,
                contest.hsk_w,
                contest.id_competition_teams,
                contest.id_fight_team,
                contest.id_ijf_blue,
                contest.id_ijf_white,
                contest.id_winner,
                contest.ippon_b,
                contest.ippon_w,
                contest.is_finished,
                contest.kodokan_tagged,
                contest.mat,
                contest.media or None,
                contest.penalty_b,
                contest.penalty_w,
                contest.published,
                contest.rank_name,
                contest.round,
                contest.round_code or None,
                contest.round_name,
                contest.sc_countdown_offset,
                contest.tagged,
                contest.timestamp_version_blue,
                contest.timestamp_version_white,
                contest.type,
                contest.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                contest.waza_b,
                contest.waza_w,
                contest.yuko_b,
                contest.yuko_w,
            ))
        # Step 3: Insert data into the database
        insert_query = """
        INSERT INTO Contest (
            id_fight, id_competition, id_person_blue, id_person_white, id_weight, age, bye,
            contest_code_long, date_start_ts, duration, events, fight_duration, fight_no,
            first_hajime_at_ts, gs, hsk_b, hsk_w, id_competition_teams, id_fight_team, id_ijf_blue,
            id_ijf_white, id_winner, ippon_b, ippon_w, is_finished, kodokan_tagged, mat, media,
            penalty_b, penalty_w, published, rank_name, round, round_code, round_name,
            sc_countdown_offset, tagged, timestamp_version_blue, timestamp_version_white, type,
            updated_at, waza_b, waza_w, yuko_b, yuko_w
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        ) AS new
        ON DUPLICATE KEY UPDATE
            id_competition = new.id_competition,
            id_person_blue = new.id_person_blue,
            id_person_white = new.id_person_white,
            id_weight = new.id_weight,
            age = new.age,
            bye = new.bye,
            contest_code_long = new.contest_code_long,
            date_start_ts = new.date_start_ts,
            duration = new.duration,
            events = new.events,
            fight_duration = new.fight_duration,
            fight_no = new.fight_no,
            first_hajime_at_ts = new.first_hajime_at_ts,
            gs = new.gs,
            hsk_b = new.hsk_b,
            hsk_w = new.hsk_w,
            id_competition_teams = new.id_competition_teams,
            id_fight_team = new.id_fight_team,
            id_ijf_blue = new.id_ijf_blue,
            id_ijf_white = new.id_ijf_white,
            id_winner = new.id_winner,
            ippon_b = new.ippon_b,
            ippon_w = new.ippon_w,
            is_finished = new.is_finished,
            kodokan_tagged = new.kodokan_tagged,
            mat = new.mat,
            media = new.media,
            penalty_b = new.penalty_b,
            penalty_w = new.penalty_w,
            published = new.published,
            rank_name = new.rank_name,
            round = new.round,
            round_code = new.round_code,
            round_name = new.round_name,
            sc_countdown_offset = new.sc_countdown_offset,
            tagged = new.tagged,
            timestamp_version_blue = new.timestamp_version_blue,
            timestamp_version_white = new.timestamp_version_white,
            type = new.type,
            updated_at = new.updated_at,
            waza_b = new.waza_b,
            waza_w = new.waza_w,
            yuko_b = new.yuko_b,
            yuko_w = new.yuko_w
        """

        await execute_query(insert_query, data, many=True)


async def main():
    await insert_competitions()
    await insert_judokas()
    await insert_contests_into_db()


asyncio.run(main())
