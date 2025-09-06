from agents import (
    Agent,
    Runner,
    AgentOutputSchema,
)
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class CustomAgentOutputSchema(BaseModel):
    sport: str
    team_leader: str
    championships_won: int
    famous_players: list[str]
    coach: str

agent = Agent(
    name="SportsInfoAgent",
    instructions="Provides detailed information about various sports teams.",
    output_type=AgentOutputSchema(output_type = CustomAgentOutputSchema, strict_json_schema=True),
    model = 'gpt-4o-mini',
)

result = Runner.run_sync(
    agent,
    "Provide detailed information about the Los Angeles Lakers basketball team.",
)

print(result.final_output)


# OUTPUT 👇🏻
# sport='Basketball' team_leader='Jeanie Buss' championships_won=17 
# famous_players=['Magic Johnson', 'Kobe Bryant', "Shaquille O'Neal", 'Kareem Abdul-Jabbar', 'LeBron James'] coach='Darvin Ham'