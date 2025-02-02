from aiohttp import ClientSession

from judobase.schemas import Competition, Contest, Judoka, Country


class _Base:
    """
    This class provides core functionality for interacting with the Judobase API.

    All methods are asynchronous and must be called within an async context.
    For ease of use and consistency, the method names mirror those found in the JudobaseAPI.
    """

    def __init__(self):
        self.base_url = "https://data.ijf.org/api/"
        self._session = ClientSession()

    async def __aenter__(self) -> "_Base":
        """Enter the async context and create a session."""

        if self._session.closed:
            self._session = ClientSession()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the async context and close the session."""

        if self._session and not self._session.closed:
            await self._session.close()

    async def close_session(self) -> None:
        """Close the session."""

        if self._session and not self._session.closed:
            await self._session.close()

    async def _get_json(self, params) -> dict:
        """Makes get request to specified API and returns JSON."""

        response = await self._session.get(
            self.base_url + "get_json",
            timeout=10,
            params=params,
        )

        if response.status != 200:
            raise ConnectionError(f"{response.status}")

        return await response.json()

    async def _competition_list(self, years: str = "", months: str = "") -> list[Competition]:
        """Returns competition list by specified filters."""

        params = {
            "params[action]": "competition.get_list",
            "params[year]": years,
            "params[month]": months,
            "params[sort]": -1,
            "params[limit]": 5000,
        }
        return [Competition(**item) for item in await self._get_json(params)]

    async def _competition_info(self, id_competition: str = "") -> Competition:
        """Returns competition list by specified filters."""

        params = {
            "params[action]": "competition.info",
            "params[id_competition]": id_competition
        }
        return Competition(**await self._get_json(params))

    async def _find_contests(
        self, id_competition: str = "", id_weight: str = "", id_person: str = ""
    ) -> list[Contest]:
        """Returns contest list by specified filters."""

        params = {
            "params[action]": "contest.find",
            "params[id_competition]": id_competition,
            "params[id_weight]": id_weight,
            "params[id_person]": id_person,
            "params[order_by]": "cnum",
            "params[limit]": 5000,
        }
        result = await self._get_json(params)
        return [Contest(**item) for item in result["contests"]]

    async def _competitor_info(self, id_competitor: str = "") -> Judoka:
        """Returns info about competitor by id."""

        params = {
            "params[action]": "competitor.info",
            "params[id_person]": id_competitor,
        }
        return Judoka(**await self._get_json(params))

    async def _country_info(self, id_country: str = "") -> Country:
        """Returns info about country by id."""

        params = {
            "params[action]": "country.info",
            "params[id_country]": id_country,
        }
        return Country(**await self._get_json(params))
