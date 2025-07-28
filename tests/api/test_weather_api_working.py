"""Working API tests for OpenWeatherMap weather endpoints using httpx directly."""

import pytest
import allure
import httpx
from src.config import get_settings


@allure.epic("API Testing")
@allure.feature("Weather API")
class TestWeatherAPIWorking:
    """Working test class for Weather API endpoints using httpx."""

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.critical
    @pytest.mark.asyncio
    @allure.title("Get weather data for valid city")
    @allure.description("Test that the API returns valid weather data for a known city")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("city", ["London", "Paris", "Tokyo", "New York"])
    async def test_get_weather_valid_city(self, city: str):
        """Test API-001: Get weather data for valid city."""
        settings = get_settings()
        
        if not settings.openweather_api_key:
            pytest.skip("OpenWeatherMap API key not provided")
        
        with allure.step(f"Request weather data for {city}"):
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.openweather_base_url}/weather",
                    params={
                        "q": city,
                        "appid": settings.openweather_api_key,
                        "units": "metric"
                    }
                )
        
        with allure.step("Verify response status"):
            assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        with allure.step("Verify response structure"):
            data = response.json()
            assert isinstance(data, dict), "Response data should be a dictionary"
            
            # Validate response schema
            assert "name" in data, "Response should contain city name"
            assert "main" in data, "Response should contain main weather data"
            assert "temp" in data["main"], "Response should contain temperature"
            
        with allure.step("Verify response content"):
            assert data["name"].lower() in city.lower() or city.lower() in data["name"].lower()
            
            allure.attach(
                str(data),
                name=f"Weather data for {city}",
                attachment_type=allure.attachment_type.JSON
            )

    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.asyncio
    @allure.title("Handle invalid city gracefully")
    @allure.description("Test that the API handles invalid city names appropriately")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_invalid_city_handling(self):
        """Test API-002: Handle invalid city names."""
        settings = get_settings()
        
        if not settings.openweather_api_key:
            pytest.skip("OpenWeatherMap API key not provided")
        
        invalid_city = "InvalidCityName123456789"
        
        with allure.step(f"Request weather data for invalid city: {invalid_city}"):
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.openweather_base_url}/weather",
                    params={
                        "q": invalid_city,
                        "appid": settings.openweather_api_key,
                        "units": "metric"
                    }
                )
        
        with allure.step("Verify error response"):
            assert response.status_code == 404, f"Expected status 404 for invalid city, got {response.status_code}"
            
            # Verify error message structure
            data = response.json()
            if isinstance(data, dict):
                assert "message" in data or "cod" in data, "Error response should contain message or code"

    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.asyncio
    @allure.title("Get weather by coordinates")
    @allure.description("Test weather API using geographical coordinates")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("coordinates", [
        {"lat": 51.5074, "lon": -0.1278, "city": "London"},
        {"lat": 40.7128, "lon": -74.0060, "city": "New York"},
        {"lat": 35.6762, "lon": 139.6503, "city": "Tokyo"}
    ])
    async def test_get_weather_by_coordinates(self, coordinates: dict):
        """Test API-003: Get weather data using coordinates."""
        settings = get_settings()
        
        if not settings.openweather_api_key:
            pytest.skip("OpenWeatherMap API key not provided")
        
        lat, lon, expected_city = coordinates["lat"], coordinates["lon"], coordinates["city"]
        
        with allure.step(f"Request weather data for coordinates: {lat}, {lon}"):
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.openweather_base_url}/weather",
                    params={
                        "lat": lat,
                        "lon": lon,
                        "appid": settings.openweather_api_key,
                        "units": "metric"
                    }
                )
        
        with allure.step("Verify response status"):
            assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        with allure.step("Verify location accuracy"):
            data = response.json()
            assert "coord" in data, "Response should contain coordinates"
            
            # Verify coordinates are approximately correct (within reasonable range)
            coord = data["coord"]
            assert abs(coord["lat"] - lat) < 1.0, "Latitude should be approximately correct"
            assert abs(coord["lon"] - lon) < 1.0, "Longitude should be approximately correct"

    @pytest.mark.api
    @pytest.mark.performance
    @pytest.mark.asyncio
    @allure.title("API response time validation")
    @allure.description("Verify API response times are within acceptable limits")
    @allure.severity(allure.severity_level.MINOR)
    async def test_api_response_time(self):
        """Test API performance: response time validation."""
        settings = get_settings()
        
        if not settings.openweather_api_key:
            pytest.skip("OpenWeatherMap API key not provided")
        
        import time
        
        with allure.step("Measure API response time"):
            start_time = time.time()
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.openweather_base_url}/weather",
                    params={
                        "q": "London",
                        "appid": settings.openweather_api_key,
                        "units": "metric"
                    }
                )
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        with allure.step("Verify response time"):
            assert response.status_code == 200, "API call should succeed"
            assert response_time < settings.performance_threshold_ms, f"Response time {response_time:.2f}ms exceeds threshold {settings.performance_threshold_ms}ms"
            
            allure.attach(
                f"Response time: {response_time:.2f}ms",
                name="Performance Data",
                attachment_type=allure.attachment_type.TEXT
            )

    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.asyncio
    @allure.title("Test 5-day forecast endpoint")
    @allure.description("Test the 5-day forecast API endpoint")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_five_day_forecast(self):
        """Test API-004: Get 5-day weather forecast."""
        settings = get_settings()
        
        if not settings.openweather_api_key:
            pytest.skip("OpenWeatherMap API key not provided")
        
        with allure.step("Request 5-day forecast for London"):
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.openweather_base_url}/forecast",
                    params={
                        "q": "London",
                        "appid": settings.openweather_api_key,
                        "units": "metric"
                    }
                )
        
        with allure.step("Verify response status"):
            assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        with allure.step("Verify forecast structure"):
            data = response.json()
            assert isinstance(data, dict), "Response data should be a dictionary"
            assert "list" in data, "Forecast response should contain list of forecasts"
            assert len(data["list"]) > 0, "Forecast should contain at least one entry"
            
            # Verify first forecast entry structure
            first_forecast = data["list"][0]
            assert "dt" in first_forecast, "Forecast should contain timestamp"
            assert "main" in first_forecast, "Forecast should contain main weather data"

    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.asyncio
    @allure.title("Test different temperature units")
    @allure.description("Test API with different temperature units (metric, imperial)")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.parametrize("units", ["metric", "imperial"])
    async def test_temperature_units(self, units: str):
        """Test API-005: Different temperature units."""
        settings = get_settings()
        
        if not settings.openweather_api_key:
            pytest.skip("OpenWeatherMap API key not provided")
        
        with allure.step(f"Request weather data with {units} units"):
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.openweather_base_url}/weather",
                    params={
                        "q": "London",
                        "appid": settings.openweather_api_key,
                        "units": units
                    }
                )
        
        with allure.step("Verify response status"):
            assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        
        with allure.step("Verify temperature units"):
            data = response.json()
            assert "main" in data, "Response should contain main weather data"
            assert "temp" in data["main"], "Response should contain temperature"
            
            # Verify temperature is numeric
            temp = data["main"]["temp"]
            assert isinstance(temp, (int, float)), "Temperature should be numeric"
            
            # Verify temperature is in reasonable range for the unit
            if units == "metric":
                assert -50 <= temp <= 50, "Celsius temperature should be in reasonable range"
            elif units == "imperial":
                assert -58 <= temp <= 122, "Fahrenheit temperature should be in reasonable range" 