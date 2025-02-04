# flake8: noqa: WPS110, WPS114

from datetime import datetime, timezone
from typing import Optional, List, Any

from pydantic import BaseModel, field_validator, Field


class Competition(BaseModel):
    """
    Represents the data about competition which provide the judobase api
    """

    id_competition: str = Field(
        ..., title="Competition ID", description="The unique identifier for the competition."
    )
    date_from: str = Field(
        ...,
        title="Start Date",
        description="The start date of the competition in YYYY/MM/DD format.",
    )
    date_to: str = Field(
        ..., title="End Date", description="The end date of the competition in YYYY/MM/DD format."
    )
    name: str = Field(..., title="Competition Name", description="The name of the competition.")
    has_results: int = Field(
        ..., title="Results Available", description="Indicates if results are available."
    )
    city: str = Field(..., title="City", description="The city where the competition is held.")
    street: str = Field(
        ..., title="Street", description="The street where the competition venue is located."
    )
    street_no: str = Field(
        ..., title="Street Number", description="The street number of the competition venue."
    )
    comp_year: int = Field(
        ..., title="Competition Year", description="The year in which the competition takes place."
    )
    prime_event: bool = Field(
        ..., title="Prime Event", description="Indicates if this is a prime event."
    )
    continent_short: str = Field(
        ..., title="Continent Code", description="The short code for the continent."
    )
    has_logo: bool = Field(
        ..., title="Has Logo", description="Indicates if the competition has a logo."
    )
    competition_code: Optional[str] = Field(
        None, title="Competition Code", description="The unique code for the competition."
    )
    updated_at_ts: datetime = Field(
        ..., title="Last Updated Timestamp", description="The timestamp of the last update."
    )
    updated_at: datetime = Field(
        ..., title="Last Updated", description="The last update date and time."
    )
    timezone: Optional[str] = Field(
        None, title="Timezone", description="The timezone of the competition."
    )
    id_live_theme: int = Field(
        ..., title="Live Theme ID", description="The ID of the live theme used for the competition."
    )
    code_live_theme: str = Field(
        ..., title="Live Theme Code", description="The code of the live theme used."
    )
    country_short: str = Field(
        ..., title="Country Short Code", description="The short code for the country."
    )
    country: str = Field(
        ..., title="Country", description="The country where the competition is held."
    )
    id_country: int = Field(
        ..., title="Country ID", description="The unique identifier for the country."
    )
    is_teams: int = Field(
        ..., title="Team Competition", description="Indicates if the competition is a team event."
    )
    status: Optional[str] = Field(
        None, title="Status", description="The status of the competition."
    )
    external_id: Optional[str] = Field(
        None, title="External ID", description="The external identifier for the competition."
    )
    id_draw_type: int = Field(..., title="Draw Type ID", description="The ID of the draw type.")
    ages: List[str] = Field(
        ..., title="Age Categories", description="List of age categories for the competition."
    )
    rank_name: Optional[str] = Field(
        None, title="Ranking Name", description="The ranking name associated with the competition."
    )

    @field_validator("updated_at", mode="after")
    @classmethod
    def parse_updated_at(cls, value):
        """Converts the `updated_at` field to a datetime object with UTC timezone."""
        return value.replace(tzinfo=timezone.utc)

    @field_validator("date_from", mode="after")
    @classmethod
    def parse_date_from(cls, value):
        """Converts the `date_from` field to a datetime object with UTC timezone."""
        return datetime.strptime(value, "%Y/%m/%d")

    @field_validator("date_to", mode="after")
    @classmethod
    def parse_date_to(cls, value):
        """Converts the `date_to` field to a datetime object with UTC timezone."""
        if isinstance(value, str):
            return datetime.strptime(value, "%Y/%m/%d")


class Contest(BaseModel):
    """
    Represents the data about contest which provide the judobase api
    """

    # general contest data
    id_competition: str
    id_fight: str
    id_person_blue: str
    id_person_white: str
    id_winner: Optional[str]
    is_finished: bool
    round: int
    duration: Optional[str]
    gs: bool
    bye: str
    fight_duration: Optional[str]
    weight: Optional[str]
    id_weight: Optional[str]
    type: int
    round_code: Optional[str]
    round_name: str
    mat: int
    date_start_ts: datetime
    updated_at: datetime
    first_hajime_at_ts: datetime

    # white person details
    ippon_w: Optional[int]
    waza_w: Optional[int]
    yuko_w: Optional[int]
    penalty_w: Optional[int]
    hsk_w: Optional[int]
    person_white: str
    id_ijf_white: str
    family_name_white: str
    given_name_white: str
    timestamp_version_white: str
    country_white: Optional[str]
    country_short_white: Optional[str]
    id_country_white: Optional[str]
    picture_folder_1: Optional[str]
    picture_filename_1: Optional[str]
    personal_picture_white: Optional[str]

    # blue person details
    ippon_b: Optional[int]
    waza_b: Optional[int]
    yuko_b: Optional[int]
    penalty_b: Optional[int]
    hsk_b: Optional[int]
    person_blue: str
    id_ijf_blue: str
    family_name_blue: str
    given_name_blue: str
    timestamp_version_blue: str
    country_blue: Optional[str]
    country_short_blue: Optional[str]
    id_country_blue: Optional[str]
    picture_folder_2: Optional[str]
    picture_filename_2: Optional[str]
    personal_picture_blue: Optional[str]

    # competitions details
    competition_name: str
    external_id: str
    city: str
    age: Optional[str]
    rank_name: Optional[str]
    competition_date: str
    date_raw: str
    comp_year: str

    # other details
    tagged: int
    kodokan_tagged: int
    published: str
    sc_countdown_offset: int
    fight_no: int
    contest_code_long: str
    media: Optional[str]
    id_competition_teams: Optional[str]
    id_fight_team: Optional[str]

    @field_validator("updated_at", mode="after")
    @classmethod
    def parse_updated_at(cls, value):
        return value.replace(tzinfo=timezone.utc)

    @field_validator("date_start_ts", mode="after")
    @classmethod
    def parse_date_start_ts(cls, value):
        return value.replace(tzinfo=timezone.utc)

    @field_validator("first_hajime_at_ts", mode="after")
    @classmethod
    def parse_first_hajime_at_ts(cls, value):
        return value.replace(tzinfo=timezone.utc)


class Judoka(BaseModel):
    """
    Represents the data about judoka which provide the judobase api
    """

    family_name: str
    middle_name: Optional[str]
    given_name: str
    family_name_local: str
    middle_name_local: Optional[str]
    given_name_local: str
    short_name: Optional[str]
    gender: str
    folder: str
    picture_filename: str
    ftechique: Optional[str]
    side: str
    coach: str
    best_result: str
    height: str
    birth_date: datetime
    country: str
    id_country: str
    country_short: str
    file_flag: Optional[str]
    club: Optional[str]
    belt: Optional[str]
    youtube_links: Optional[str]
    status: Optional[str]
    archived: Optional[str]
    categories: List[str]
    dob_year: Optional[str]
    age: Optional[str]
    death_age: Optional[str]
    personal_picture: str


class Country(BaseModel):
    """
    Represents the data about country which provide the judobase api
    """

    name: str
    id_country: str
    country_short: str
    org_name: str
    org_www: str
    head_address: str
    head_city: str
    contact_phone: str
    contact_email: str
    exclude_from_medals: str
    president_name: str
    male_competitiors: str
    female_competitiors: str
    total_competitors: int
    number_of_competitions: str
    number_of_total_competitions: str
    number_of_total_wins: int
    number_of_total_fights: int
    best_male_competitor: Optional[dict[str, Any]] = None
    best_female_competitor: Optional[dict[str, Any]] = None
    total_ranking_points: Optional[str] = None
    ranking: Optional[dict[str, Any]] = None
    ranking_male: Optional[dict[str, Any]] = None
    ranking_female: Optional[dict[str, Any]] = None
