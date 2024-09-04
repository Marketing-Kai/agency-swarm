from agency_swarm.agents import Agent


class HealthDev(Agent):
    def __init__(self):
        super().__init__(
            name="HealthDev",
            description="Verantwortlich für die Implementierung der technischen Lösung (z.B. Streamlit, Django/Flask).",
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
