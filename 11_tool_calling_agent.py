import requests
import urllib3
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage, SystemMessage

# Desabilitar avisos de SSL para desenvolvimento
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

@tool('get_weather', description='Return weather information for a given city', return_direct=False)
def get_weather(city: str):
    response = requests.get(f'https://wttr.in/{city}?format=j1', verify=False)
    return response.json()

@tool('get_cnpj', description='Return CNPJ information for a given CNPJ number', return_direct=False)
def get_cnpj(cnpj: str):
    response = requests.get(f'https://api.opencnpj.org/{cnpj}', verify=False)
    return response.json()

agent = create_agent(
    model = 'gpt-4.1-mini',
    tools = [get_weather, get_cnpj],
    system_prompt = "Você é um asssistente que responde vários tipos de perguntas"
)

result = agent.invoke({
    "messages": [
        HumanMessage(content="Qual o clima na cidade do CNPJ 06.990.590/0001-23")
    ]
})

# for message in result["messages"]:
#     print(message)
#     print(message.type)
#     print("-" * 100)

print(result["messages"][-1].content)
