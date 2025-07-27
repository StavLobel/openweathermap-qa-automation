"""OpenWeatherMap API client for testing."""

from typing import Any, Dict, Optional
from playwright.async_api import APIRequestContext
from src.config import get_settings
from src.utils import get_logger


class WeatherAPIClient:
    """Client for OpenWeatherMap API testing using Playwright's APIRequestContext."""
    
    def __init__(self, request_context: APIRequestContext) -> None:
        """Initialize the weather API client.
        
        Args:
            request_context: Playwright APIRequestContext instance.
        """
        self.request_context = request_context
        self.settings = get_settings()
        self.logger = get_logger(self.__class__.__name__)
        self.base_url = self.settings.openweather_base_url
        self.api_key = self.settings.openweather_api_key
        
    async def get_current_weather(self, city: str, **kwargs) -> Dict[str, Any]:
        """Get current weather data for a city.
        
        Args:
            city: City name.
            **kwargs: Additional query parameters.
            
        Returns:
            API response as dictionary.
        """
        params = {
            "q": city,
            "appid": self.api_key,
            "units": kwargs.get("units", "metric"),
            **kwargs
        }
        
        self.logger.info(f"Getting current weather for: {city}")
        
        response = await self.request_context.get(
            f"{self.base_url}/weather",
            params=params
        )
        
        return {
            "status": response.status,
            "headers": dict(response.headers),
            "data": await response.json() if response.ok else await response.text()
        }
        
    async def get_weather_by_coordinates(self, lat: float, lon: float, **kwargs) -> Dict[str, Any]:
        """Get weather data by geographical coordinates.
        
        Args:
            lat: Latitude.
            lon: Longitude.
            **kwargs: Additional query parameters.
            
        Returns:
            API response as dictionary.
        """
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": kwargs.get("units", "metric"),
            **kwargs
        }
        
        self.logger.info(f"Getting weather for coordinates: {lat}, {lon}")
        
        response = await self.request_context.get(
            f"{self.base_url}/weather",
            params=params
        )
        
        return {
            "status": response.status,
            "headers": dict(response.headers),
            "data": await response.json() if response.ok else await response.text()
        }
        
    async def get_weather_by_city_id(self, city_id: int, **kwargs) -> Dict[str, Any]:
        """Get weather data by city ID.
        
        Args:
            city_id: OpenWeatherMap city ID.
            **kwargs: Additional query parameters.
            
        Returns:
            API response as dictionary.
        """
        params = {
            "id": city_id,
            "appid": self.api_key,
            "units": kwargs.get("units", "metric"),
            **kwargs
        }
        
        self.logger.info(f"Getting weather for city ID: {city_id}")
        
        response = await self.request_context.get(
            f"{self.base_url}/weather",
            params=params
        )
        
        return {
            "status": response.status,
            "headers": dict(response.headers),
            "data": await response.json() if response.ok else await response.text()
        }
        
    async def get_5_day_forecast(self, city: str, **kwargs) -> Dict[str, Any]:
        """Get 5-day weather forecast for a city.
        
        Args:
            city: City name.
            **kwargs: Additional query parameters.
            
        Returns:
            API response as dictionary.
        """
        params = {
            "q": city,
            "appid": self.api_key,
            "units": kwargs.get("units", "metric"),
            **kwargs
        }
        
        self.logger.info(f"Getting 5-day forecast for: {city}")
        
        response = await self.request_context.get(
            f"{self.base_url}/forecast",
            params=params
        )
        
        return {
            "status": response.status,
            "headers": dict(response.headers),
            "data": await response.json() if response.ok else await response.text()
        }
        
    async def search_cities(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """Search for cities using geocoding API.
        
        Args:
            query: City name to search.
            limit: Number of results to return.
            
        Returns:
            API response as dictionary.
        """
        params = {
            "q": query,
            "limit": limit,
            "appid": self.api_key
        }
        
        self.logger.info(f"Searching cities for: {query}")
        
        response = await self.request_context.get(
            "http://api.openweathermap.org/geo/1.0/direct",
            params=params
        )
        
        return {
            "status": response.status,
            "headers": dict(response.headers),
            "data": await response.json() if response.ok else await response.text()
        }
        
    def validate_weather_response(self, response_data: Dict[str, Any]) -> bool:
        """Validate weather API response structure.
        
        Args:
            response_data: API response data.
            
        Returns:
            True if response is valid, False otherwise.
        """
        required_fields = ["coord", "weather", "main", "wind", "clouds", "dt", "sys", "id", "name"]
        
        if not isinstance(response_data, dict):
            return False
            
        return all(field in response_data for field in required_fields)
        
    def validate_forecast_response(self, response_data: Dict[str, Any]) -> bool:
        """Validate forecast API response structure.
        
        Args:
            response_data: API response data.
            
        Returns:
            True if response is valid, False otherwise.
        """
        required_fields = ["cod", "message", "cnt", "list", "city"]
        
        if not isinstance(response_data, dict):
            return False
            
        return all(field in response_data for field in required_fields) 