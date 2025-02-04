import asyncio
from datetime import datetime

from judobase.base import CompetitionAPI, ContestAPI, JudokaAPI, CountryAPI
from judobase.schemas import Competition, Contest, Judoka, Country


class JudoBase(CompetitionAPI, ContestAPI, JudokaAPI, CountryAPI):
    """
    Class for interacting with the JudoBase API.
    Provides methods to retrieve information about competitions, contests, judokas, and countries.
    """

    async def all_competition(self) -> list[Competition]:
        """
        Retrieves data for all competitions.
        """

        return await self.get_competition_list()

    async def competitions_in_range(
        self, start_date: datetime, end_date: datetime
    ) -> list[Competition]:
        """
        Retrieves data for competitions within a specified date range.
        """

        all_comps = await self.all_competition()
        return [comp for comp in all_comps if start_date <= comp.date_from <= end_date]

    async def competition_by_id(self, competition_id: int | str) -> Competition:
        """
        Retrieves data for a specific competition by its ID.
        """

        return await self.get_competition_info(competition_id)

    async def all_contests(self) -> list[Contest]:
        """
        Retrieves data for all contests using concurrent API calls.
        """

        comps = await self.all_competition()
        tasks = [self.find_contests(comp.id_competition) for comp in comps]
        tasks_results = await asyncio.gather(*tasks)

        return [contest for sublist in tasks_results for contest in sublist]

    async def judoka_by_id(self, judoka_id: int | str) -> Judoka:
        """
        Retrieves data for a specific judoka by their ID.
        """

        return await self.get_judoka_info(str(judoka_id))

    async def country_by_id(self, country_id: int | str) -> Country:
        """
        Retrieves data for a specific country by its ID.
        """

        return await self.get_country_info(country_id)
