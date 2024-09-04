from agency_swarm import Agency
from HealthAnalyst import HealthAnalyst
from HealthDev import HealthDev
from HealthCEO import HealthCEO

health_ceo = HealthCEO()
health_dev = HealthDev()
health_analyst = HealthAnalyst()

agency = Agency([health_ceo, health_dev, [health_ceo, health_dev],
                 [health_ceo, health_analyst],
                 [health_dev, health_analyst]],
                shared_instructions='./agency_manifesto.md',  # shared instructions for all agents
                max_prompt_tokens=25000,  # default tokens in conversation for all agents
                temperature=0.3,  # default temperature for all agents
                )

if __name__ == '__main__':
    agency.demo_gradio()