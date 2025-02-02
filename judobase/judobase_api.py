import asyncio
from datetime import datetime

from .base import _Base
from .schemas import Competition, Contest, Judoka, Country


class JudoBase(_Base):
    """
    Class for interacting with the JudoBase API.
    Provides methods to retrieve information about competitions, contests, judokas, and countries.
    """

    async def all_competition(self) -> list[Competition]:
        """
        Retrieves data for all competitions.
        """

        return await self._competition_list()

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

        return await self._competition_info(competition_id)

    async def all_contests(self) -> list[Contest]:
        """
        Retrieves data for all contests using concurrent API calls.
        """

        comps = await self.all_competition()
        tasks = [self._find_contests(comp.id_competition) for comp in comps]

        results = await asyncio.gather(*tasks)

        contests = [contest for sublist in results for contest in sublist]
        return contests

    async def judoka_by_id(self, judoka_id: int | str) -> Judoka:
        """
        Retrieves data for a specific judoka by their ID.
        """

        return await self._competitor_info(str(judoka_id))

    async def country_by_id(self, country_id: int | str) -> Country:
        """
        Retrieves data for a specific country by its ID.
        """

        return await self._country_info(country_id)
