from agency_swarm.agents import Agent


class HealthAnalyst(Agent):
    def __init__(self):
        super().__init__(
            name="HealthAnalyst",
            description="Führt spezifische Datenanalysen durch und bereitet die Ergebnisse für die UI-Integration vor.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
        )
        
    def response_validator(self, message):
        return message
