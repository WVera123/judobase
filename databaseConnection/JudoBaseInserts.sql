USE JudoBase;
SELECT * FROM Weight;
SELECT * FROM Judoka;
SELECT * FROM Competition;
SELECT * FROM Contest WHERE id_weight NOT between 1 and 14;
UPDATE Contest SET id_weight = 11 WHERE id_weight = 262;

CREATE TABLE Judoka (
id INT NOT NULL,
id_country INT,
age INT,
archived INT,
belt VARCHAR(255),
best_result VARCHAR(255),
birth_date VARCHAR(255) NOT NULL, -- VARCHAR van gemaakt omdat API vreemde en niet juiste data teruggeeft.
categories VARCHAR(255) NOT NULL,
club VARCHAR(255),
coach VARCHAR(255),
death_age INT,
dob_year INT,
family_name VARCHAR(255) NOT NULL,
family_name_local VARCHAR(255),
file_flag VARCHAR(255),
folder VARCHAR(255) NOT NULL,
ftechique VARCHAR(255),
gender VARCHAR(255) NOT NULL,
given_name VARCHAR(255) NOT NULL,
given_name_local VARCHAR(255),
height INT,
middle_name VARCHAR(255),
middle_name_local VARCHAR(255),
personal_picture VARCHAR(255) NOT NULL,
picture_filename  VARCHAR(255),
short_name VARCHAR(255),
side VARCHAR(255),
status INT,
youtube_links VARCHAR (255),

CONSTRAINT PK_Judoka PRIMARY KEY (id)
);

CREATE TABLE Competition (
id_competition INT NOT NULL,
id_country INT NOT NULL,
ages VARCHAR(255),
city VARCHAR(255) NOT NULL,
code_live_theme VARCHAR(255) NOT NULL,
comp_year YEAR,
continent_short VARCHAR(4),
country VARCHAR(255) NOT NULL,
date_from DATETIME NOT NULL,
date_to DATETIME NOT NULL,
external_id VARCHAR(255),
has_logo BOOLEAN,
has_results INT,
id_draw_type INT,
id_live_theme INT NOT NULL,
is_teams BOOLEAN NOT NULL,
name VARCHAR(255) NOT NULL,
prime_event BOOLEAN,
rank_name VARCHAR(255),
status INT,
street VARCHAR(255),
street_no VARCHAR(255),
timezone VARCHAR(255),
updated_at DATETIME,
updated_at_ts DATETIME NOT NULL,

CONSTRAINT PK_Competition PRIMARY KEY (id_competition)
);

CREATE TABLE Contest (
id_fight INT NOT NULL,
id_competition INT NOT NULL,
id_person_blue INT NOT NULL,
id_person_white INT NOT NULL,
id_weight INT,
age VARCHAR(255),
bye INT NOT NULL,
contest_code_long VARCHAR(255) NOT NULL,
date_start_ts DATETIME NOT NULL,
duration TIME,
events VARCHAR(255),
fight_duration INT,
fight_no INT NOT NULL,
first_hajime_at_ts DATETIME NOT NULL,
gs BOOLEAN NOT NULL,
hsk_b INT,
hsk_w INT,
id_competition_teams VARCHAR(255),
id_fight_team VARCHAR(255),
id_ijf_blue VARCHAR(255),
id_ijf_white VARCHAR(255),
id_winner INT,
ippon_b INT,
ippon_w INT,
is_finished BOOLEAN NOT NULL,
kodokan_tagged INT NOT NULL,
mat INT NOT NULL,
media VARCHAR(255),
penalty_b INT,
penalty_w INT,
published INT NOT NULL,
rank_name VARCHAR(255),
round INT,
round_code VARCHAR(255),
round_name VARCHAR(255),
sc_countdown_offset INT NOT NULL,
tagged INT,
timestamp_version_blue VARCHAR(255) NOT NULL,
timestamp_version_white VARCHAR(255) NOT NULL,
type INT NOT NULL,
updated_at DATETIME NOT NULL,
waza_b INT,
waza_w INT,
yuko_b INT,
yuko_w INT,

CONSTRAINT PK_Contest PRIMARY KEY (id_fight)
);

CREATE TABLE Weight (
id INT NOT NULL,
weight VARCHAR(255),

CONSTRAINT PK_Weight PRIMARY KEY (id)
);

INSERT INTO Weight
VALUES
(76, '-55'),
(1, '-60'),
(2, '-66'),
(3, '-73'),
(4, '-81'),
(5, '-90'),
(6, '-100'),
(7, '100'),
(77, '-44'),
(8, '-48'),
(9, '-52'),
(10, '-57'),
(11, '-63'),
(12, '-70'),
(13, '-78'),
(14, '78'),
(227, 'Open male'),
(228, 'Open female');

CREATE TABLE CountryShort(
id INT NOT  NULL,
name VARCHAR(255),
ioc VARCHAR(255),
CONSTRAINT PK_CountryShort PRIMARY KEY (id)
);

CREATE TABLE Country(
id_country INT NOT NULL,
org_name VARCHAR(255),
org_www VARCHAR(255),
head_address VARCHAR(255),
head_city VARCHAR(255),
contact_phone VARCHAR(255),
contact_email VARCHAR(255),
exclude_from_medals INT,
president_name VARCHAR(255),
male_competitors INT,
female_competitors INT,
total_competitors INT,
number_of_competitions INT,
number_of_total_wins INT,
number_of_total_fights INT,
best_male_competitors_id INT,
best_female_competitor_id INT,
total_ranking_points INT,
ranking_place INT,
ranking_place_male INT,
ranking_place_female INT

)

ALTER TABLE Contest
ADD CONSTRAINT FK_ContestCompetition 
FOREIGN KEY (id_competition) REFERENCES Competition(id_competition)
ON UPDATE CASCADE;

ALTER TABLE Contest
ADD CONSTRAINT FK_ContestPersonBlue
FOREIGN KEY (id_person_blue) REFERENCES Judoka(id)
ON UPDATE CASCADE;

ALTER TABLE Contest
ADD CONSTRAINT FK_ContestPersonWhite
FOREIGN KEY (id_person_white) REFERENCES Judoka(id)
ON UPDATE CASCADE;

-- ALTER TABLE Contest DROP CONSTRAINT FK_ContestWeight;

ALTER TABLE Contest
ADD CONSTRAINT FK_ContestWeight
FOREIGN KEY (id_weight) REFERENCES Weight(id)
ON UPDATE CASCADE;

ALTER TABLE Judoka
ADD CONSTRAINT FK_JudokaCountryShort
FOREIGN KEY (id_country) REFERENCES CountryShort(id)
ON UPDATE CASCADE;

ALTER TABLE Competition
ADD CONSTRAINT FK_CompetitionCountryShort
FOREIGN KEY (id_country) REFERENCES CountryShort(id)
ON UPDATE CASCADE;
