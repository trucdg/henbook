import anthropic
import json
import os
import re
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

system_prompt = """
You are a data extraction assistant that interprets shorthand betting notations for American football games, including NFL, NCAA, and other leagues.
Your goal is to read compact human inputs that describe game lines and turn them into structured JSON objects that match this schema:

[
  {
    "game_date": "YYYY-MM-DD",
    "team_a": "string",
    "team_b": "string or null",
    "league": "string",
    "favorite_team": "string or null",
    "first"
    "spread": "float or null",
    "over_under_points": "float or null",
    "half": "string (either '1H' for first half, '2H' for second half, or 'full')",
  }
]

### Parsing rules
- The game may belong to the NFL (American football) or NCAA (college football). Use your best judgment based on team names or abbreviations.
- Dates like "1/14" should be converted to ISO format (YYYY-MM-DD) using the current or next relevant year if not provided. Expect different formats for dates.
- Lines with patterns like "Dall 7/52" mean:
  - Favorite team: Dallas Cowboys (from "Dall")
  - Spread: 7
  - Over/Under Points: 52
- Team abbreviations, nicknames, or mascots may be used instead of full team names. For example:
  - "Cowboys" = Dallas Cowboys
  - "Crimson Tide" = Alabama
  - "Wolverines" = Michigan
  - "Nittany Lions" = Penn State
  - "Tigers" could refer to multiple schools (e.g., LSU, Clemson, Auburn). Choose the most likely one based on context or leave ambiguous names as `null`.
- If a team abbreviation or nickname cannot be confidently matched, leave the full name as `null` but preserve the original text.
- If an opponent is not listed, set "team_b": null.
- If the text includes "1h" or "1H", set "half": "1H". If not, set "half": "full".
- Be tolerant of typos, spacing errors, or variations in team names.
- If any value is unknown, set it to null.
- Do not include explanations, comments, or extra text outside the JSON array.

### Team abbreviation mapping examples
Dall → Dallas Cowboys  
Dal → Dallas Cowboys  
Det → Detroit Lions  
NE → New England Patriots  
KC → Kansas City Chiefs  
SF → San Francisco 49ers  
GB → Green Bay Packers  
Bal → Baltimore Ravens  
Buf → Buffalo Bills  
Phi → Philadelphia Eagles  
NYG → New York Giants  
NYJ → New York Jets  
Chi → Chicago Bears  
Min → Minnesota Vikings  
Sea → Seattle Seahawks  
LV → Las Vegas Raiders  
LAR → Los Angeles Rams  
LAC → Los Angeles Chargers  
Hou → Houston Texans  
Ten → Tennessee Titans  
Cin → Cincinnati Bengals  
Cle → Cleveland Browns  
Jax → Jacksonville Jaguars  
TB → Tampa Bay Buccaneers  
Atl → Atlanta Falcons  
NO → New Orleans Saints  
Car → Carolina Panthers  
Ind → Indianapolis Colts  
Was → Washington Commanders  
Mia → Miami Dolphins  
Ari → Arizona Cardinals  
Den → Denver Broncos
Pit → Pittsburgh Steelers
... (expect variations and typos from user input)

MUST Return only valid JSON.

"""

user_prompt = "Sund 1/14 g 4:30 \nDall 7/52 \nDet 3/53 \n1h \nAla 6.5/49 \nMich 3/45 \nReopen 7:45"


# client = anthropic.Anthropic(
#     api_key=os.environ.get("ANTHROPIC_API_KEY"),
# )
# message = client.messages.create(
#     model="claude-sonnet-4-5",
#     max_tokens=1000,
#     temperature=0,
#     system=system_prompt,
#     messages=[
#         {"role": "user", "content": user_prompt}
#     ]
# ).content[0].text

message = '```json\n[\n  {\n    "game_date": "2024-01-14",\n    "team_a": "Dallas Cowboys",\n    "team_b": null,\n    "league": "NFL",\n    "favorite_team": "Dallas Cowboys",\n    "spread": 7.0,\n    "over_under_points": 52.0,\n    "half": "full"\n  },\n  {\n    "game_date": "2024-01-14",\n    "team_a": "Detroit Lions",\n    "team_b": null,\n    "league": "NFL",\n    "favorite_team": "Detroit Lions",\n    "spread": 3.0,\n    "over_under_points": 53.0,\n    "half": "full"\n  },\n  {\n    "game_date": "2024-01-14",\n    "team_a": "Alabama",\n    "team_b": null,\n    "league": "NCAA",\n    "favorite_team": "Alabama",\n    "spread": 6.5,\n    "over_under_points": 49.0,\n    "half": "1H"\n  },\n  {\n    "game_date": "2024-01-14",\n    "team_a": "Michigan",\n    "team_b": null,\n    "league": "NCAA",\n    "favorite_team": "Michigan",\n    "spread": 3.0,\n    "over_under_points": 45.0,\n    "half": "1H"\n  }\n]\n```'
# Remove the Markdown code fences
clean_text = re.sub(r"^```json\s*|\s*```$", "", message.strip())
json_data = json.loads(clean_text)
# ask ChatGPT to parse the message into a JSON object
print(message)
print(json_data)

for game in json_data:
    print(game["team_a"], game["spread"], game["over_under_points"])