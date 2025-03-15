
"""
Weather AI Assistant: A simple AI agent that helps users get weather information
and provides clothing recommendations based on weather conditions.

Requirements:
- Python 3.8+
- OpenAI API key or equivalent
- Weather API key (OpenWeatherMap used in this example)
"""

import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.tools import BaseTool
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Initialize the LLM
llm = ChatOpenAI(
    temperature=0.2,
    model="gpt-3.5-turbo",
    openai_api_key=OPENAI_API_KEY
)

# Create a Weather Tool
class WeatherTool(BaseTool):
    name: str = "weather_tool"
    description: str = "Use this tool to get current weather information for a specific location"

    
    def _run(self, location: str) -> str:
        """Get weather information for a location."""
        try:
            base_url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": location,
                "appid": WEATHER_API_KEY,
                "units": "metric"  # Use metric units (Celsius)
            }
            
            response = requests.get(base_url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                weather_info = {
                    "location": data["name"],
                    "country": data["sys"]["country"],
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"],
                    "wind_speed": data["wind"]["speed"],
                }
                return json.dumps(weather_info)
            else:
                return f"Error: Unable to fetch weather data. Status code: {response.status_code}"
        except Exception as e:
            return f"Error fetching weather data: {str(e)}"
    
    def _arun(self, location: str):
        # Async implementation would go here
        pass

# Create a Clothing Recommendation Tool
class ClothingRecommendationTool(BaseTool):
    name: str = "clothing_recommendation_tool"
    description: str = "Use this tool to get clothing recommendations based on weather conditions"

    
    def _run(self, weather_data: str) -> str:
        """Generate clothing recommendations based on weather data."""
        try:
            # Parse the weather data
            weather_info = json.loads(weather_data)
            
            # Create a prompt for the LLM to generate clothing recommendations
            prompt = ChatPromptTemplate.from_template(
                """
                Based on the following weather conditions, provide clothing recommendations:
                
                Location: {location}, {country}
                Temperature: {temperature}°C (feels like {feels_like}°C)
                Humidity: {humidity}%
                Weather: {description}
                Wind Speed: {wind_speed} m/s
                
                Provide specific clothing recommendations for these conditions. 
                Include suggestions for top, bottom, footwear, and accessories if needed.
                Format your response in a friendly, helpful manner.
                """
            )
            
            # Format the prompt with weather information
            formatted_prompt = prompt.format(
                location=weather_info["location"],
                country=weather_info["country"],
                temperature=weather_info["temperature"],
                feels_like=weather_info["feels_like"],
                humidity=weather_info["humidity"],
                description=weather_info["description"],
                wind_speed=weather_info["wind_speed"]
            )
            
            # Get recommendations from the LLM
            response = llm.predict(formatted_prompt)
            return response
        except Exception as e:
            return f"Error generating clothing recommendations: {str(e)}"
    
    def _arun(self, weather_data: str):
        # Async implementation would go here
        pass

# Setup the agent
def create_weather_assistant():
    # Define tools
    tools = [
        WeatherTool(),
        ClothingRecommendationTool()
    ]
    
    # Setup memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    # Initialize agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True
    )
    
    return agent

# Main application function
def run_weather_assistant():
    agent = create_weather_assistant()
    
    print("🌤️ Weather AI Assistant 🌤️")
    print("Ask for weather information and clothing recommendations for any location.")
    print("Type 'exit' to quit.")
    print("-" * 50)
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == "exit":
            print("Thank you for using Weather AI Assistant. Goodbye!")
            break
        
        try:
            response = agent.invoke(user_input)
            print(f"\nAssistant: {response}")
        except Exception as e:
            print(f"\nAssistant: I encountered an error: {str(e)}")
            print("Please try again with a different query.")

if __name__ == "__main__":
    run_weather_assistant()