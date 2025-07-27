"""API tests for OpenWeatherMap weather endpoints."""

import pytest
import allure
from src.api import WeatherAPIClient


@allure.epic("API Testing")
@allure.feature("Weather API")
class TestWeatherAPI:
    """Test class for Weather API endpoints."""

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.critical
    @allure.title("Get weather data for valid city")
    @allure.description("Test that the API returns valid weather data for a known city")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("city", ["London", "Paris", "Tokyo", "New York"])
    async def test_get_weather_valid_city(self, weather_api: WeatherAPIClient, city: str):
        """Test API-001: Get weather data for valid city."""
        with allure.step(f"Request weather data for {city}"):
            response = await weather_api.get_current_weather(city)
        
        with allure.step("Verify response status"):
            assert response["status"] == 200, f"Expected status 200, got {response['status']}"
        
        with allure.step("Verify response structure"):
            data = response["data"]
            assert isinstance(data, dict), "Response data should be a dictionary"
            
            # Validate response schema
            is_valid = weather_api.validate_weather_response(data)
            assert is_valid, f"Response structure is invalid for {city}"
        
        with allure.step("Verify response content"):
            assert "name" in data, "Response should contain city name"
            assert data["name"].lower() in city.lower() or city.lower() in data["name"].lower()
            
            assert "main" in data, "Response should contain main weather data"
            assert "temp" in data["main"], "Response should contain temperature"
            
            allure.attach(
                str(data),
                name=f"Weather data for {city}",
                attachment_type=allure.attachment_type.JSON
            )

    @pytest.mark.api
    @pytest.mark.regression
    @allure.title("Handle invalid city gracefully")
    @allure.description("Test that the API handles invalid city names appropriately")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_invalid_city_handling(self, weather_api: WeatherAPIClient):
        """Test API-002: Handle invalid city names."""
        invalid_city = "InvalidCityName123456789"
        
        with allure.step(f"Request weather data for invalid city: {invalid_city}"):
            response = await weather_api.get_current_weather(invalid_city)
        
        with allure.step("Verify error response"):
            assert response["status"] == 404, f"Expected status 404 for invalid city, got {response['status']}"
            
            # Verify error message structure
            data = response["data"]
            if isinstance(data, dict):
                assert "message" in data or "cod" in data, "Error response should contain message or code"

    @pytest.mark.api
    @pytest.mark.regression
    @allure.title("Get weather by coordinates")
    @allure.description("Test weather API using geographical coordinates")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("coordinates", [
        {"lat": 51.5074, "lon": -0.1278, "city": "London"},
        {"lat": 40.7128, "lon": -74.0060, "city": "New York"},
        {"lat": 35.6762, "lon": 139.6503, "city": "Tokyo"}
    ])
    async def test_get_weather_by_coordinates(self, weather_api: WeatherAPIClient, coordinates: dict):
        """Test API-003: Get weather data using coordinates."""
        lat, lon, expected_city = coordinates["lat"], coordinates["lon"], coordinates["city"]
        
        with allure.step(f"Request weather data for coordinates: {lat}, {lon}"):
            response = await weather_api.get_weather_by_coordinates(lat, lon)
        
        with allure.step("Verify response status"):
            assert response["status"] == 200, f"Expected status 200, got {response['status']}"
        
        with allure.step("Verify location accuracy"):
            data = response["data"]
            assert "coord" in data, "Response should contain coordinates"
            
            # Verify coordinates are approximately correct (within reasonable range)
            coord = data["coord"]
            assert abs(coord["lat"] - lat) < 1.0, "Latitude should be approximately correct"
            assert abs(coord["lon"] - lon) < 1.0, "Longitude should be approximately correct"

    @pytest.mark.api
    @pytest.mark.regression
    @allure.title("Get 5-day weather forecast")
    @allure.description("Test 5-day weather forecast endpoint")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_get_5_day_forecast(self, weather_api: WeatherAPIClient):
        """Test API-004: Get 5-day weather forecast."""
        city = "London"
        
        with allure.step(f"Request 5-day forecast for {city}"):
            response = await weather_api.get_5_day_forecast(city)
        
        with allure.step("Verify response status"):
            assert response["status"] == 200, f"Expected status 200, got {response['status']}"
        
        with allure.step("Verify forecast structure"):
            data = response["data"]
            is_valid = weather_api.validate_forecast_response(data)
            assert is_valid, "Forecast response structure is invalid"
            
            assert "list" in data, "Forecast should contain list of weather data"
            forecast_list = data["list"]
            assert len(forecast_list) > 0, "Forecast list should not be empty"
            
            # Verify forecast contains multiple entries (typically 40 for 5 days)
            assert len(forecast_list) >= 8, "Should have at least 8 forecast entries"

    @pytest.mark.api
    @pytest.mark.performance
    @allure.title("API response time validation")
    @allure.description("Verify API response times are within acceptable limits")
    @allure.severity(allure.severity_level.MINOR)
    async def test_api_response_time(self, weather_api: WeatherAPIClient):
        """Test API-005: Verify API response time."""
        import time
        
        city = "London"
        
        with allure.step("Measure API response time"):
            start_time = time.time()
            response = await weather_api.get_current_weather(city)
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        with allure.step("Verify response time threshold"):
            # Assuming 5 seconds as reasonable threshold for external API
            max_response_time = 5000  # milliseconds
            
            assert response_time < max_response_time, \
                f"API response time {response_time:.2f}ms exceeds threshold {max_response_time}ms"
            
            allure.attach(
                f"Response time: {response_time:.2f}ms",
                name="Performance Metrics",
                attachment_type=allure.attachment_type.TEXT
            )

    @pytest.mark.api
    @pytest.mark.regression
    @allure.title("Test different units parameter")
    @allure.description("Test weather API with different unit systems")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.parametrize("units", ["metric", "imperial", "kelvin"])
    async def test_different_units(self, weather_api: WeatherAPIClient, units: str):
        """Test API-006: Test different unit systems."""
        city = "London"
        
        with allure.step(f"Request weather data with {units} units"):
            response = await weather_api.get_current_weather(city, units=units)
        
        with allure.step("Verify response status"):
            assert response["status"] == 200, f"Expected status 200, got {response['status']}"
        
        with allure.step("Verify temperature units"):
            data = response["data"]
            temp = data["main"]["temp"]
            
            # Basic sanity checks for temperature ranges
            if units == "metric":
                # Celsius: reasonable range -50 to 60
                assert -50 <= temp <= 60, f"Temperature {temp}°C seems unreasonable for metric units"
            elif units == "imperial":
                # Fahrenheit: reasonable range -60 to 140
                assert -60 <= temp <= 140, f"Temperature {temp}°F seems unreasonable for imperial units"
            elif units == "kelvin":
                # Kelvin: should be positive and reasonable
                assert 200 <= temp <= 350, f"Temperature {temp}K seems unreasonable for kelvin units" 