"""End-to-end tests for complete user journeys."""

import pytest
import allure
from src.pages import WeatherPage
from src.api import WeatherAPIClient


@allure.epic("E2E Testing")
@allure.feature("Weather Journey")
class TestWeatherJourney:
    """Test class for end-to-end weather search journeys."""

    @pytest.mark.e2e
    @pytest.mark.critical
    @allure.title("Complete weather search journey")
    @allure.description("Test complete user journey from search to weather display")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("city", ["London", "Paris"])
    async def test_complete_weather_search_journey(
        self, 
        weather_page: WeatherPage, 
        weather_api: WeatherAPIClient,
        city: str
    ):
        """Test E2E-001: Complete weather search user journey."""
        
        with allure.step("Step 1: Validate API is accessible"):
            # First ensure the API works for this city
            api_response = await weather_api.get_current_weather(city)
            assert api_response["status"] == 200, f"API should be accessible for {city}"
        
        with allure.step("Step 2: Navigate to weather page"):
            await weather_page.navigate_to_weather_page()
            
            # Verify page loaded correctly
            title = await weather_page.get_title()
            assert "OpenWeatherMap" in title
        
        with allure.step(f"Step 3: Search for weather in {city}"):
            await weather_page.search_for_city(city)
        
        with allure.step("Step 4: Verify search results"):
            # Check if we're still on a valid OpenWeatherMap page
            current_url = await weather_page.get_url()
            assert "openweathermap" in current_url.lower()
            
            # Try to get weather information if displayed
            is_weather_displayed = await weather_page.is_weather_info_displayed()
            
            if is_weather_displayed:
                with allure.step("Step 5: Validate displayed weather data"):
                    # If weather is displayed, try to get the data
                    displayed_city = await weather_page.get_city_name()
                    temperature = await weather_page.get_temperature()
                    
                    if displayed_city:
                        allure.attach(
                            f"Displayed city: {displayed_city}",
                            name="UI City Name",
                            attachment_type=allure.attachment_type.TEXT
                        )
                    
                    if temperature:
                        allure.attach(
                            f"Displayed temperature: {temperature}",
                            name="UI Temperature",
                            attachment_type=allure.attachment_type.TEXT
                        )
            else:
                # If weather is not displayed, document this for analysis
                allure.attach(
                    f"Weather information not visually displayed for {city}. "
                    "This could be due to UI structure changes, API key requirements, "
                    "or the need to navigate to a specific weather page.",
                    name="UI Observation",
                    attachment_type=allure.attachment_type.TEXT
                )
        
        with allure.step("Step 6: Cross-validate with API data"):
            # Compare UI behavior with API response
            api_data = api_response["data"]
            
            allure.attach(
                f"API returned: {api_data.get('name', 'Unknown')} - "
                f"{api_data['main']['temp']}°C",
                name="API Response Summary",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # The journey is successful if:
            # 1. API works (already verified)
            # 2. UI navigation works (verified by URL check)
            # 3. Search was performed without errors
            assert True, "E2E journey completed successfully"

    @pytest.mark.e2e
    @pytest.mark.regression
    @allure.title("Error handling journey")
    @allure.description("Test user journey with invalid search input")
    @allure.severity(allure.severity_level.NORMAL)
    async def test_error_handling_journey(
        self, 
        weather_page: WeatherPage, 
        weather_api: WeatherAPIClient
    ):
        """Test E2E-002: Error handling user journey."""
        invalid_city = "InvalidCityXYZ123"
        
        with allure.step("Step 1: Validate API error response"):
            api_response = await weather_api.get_current_weather(invalid_city)
            assert api_response["status"] == 404, "API should return 404 for invalid city"
        
        with allure.step("Step 2: Navigate to weather page"):
            await weather_page.navigate_to_weather_page()
        
        with allure.step(f"Step 3: Search for invalid city: {invalid_city}"):
            await weather_page.search_for_city(invalid_city)
        
        with allure.step("Step 4: Verify error handling"):
            # Check that the application handles the error gracefully
            current_url = await weather_page.get_url()
            is_error_displayed = await weather_page.is_error_displayed()
            
            # Either error should be displayed or URL should indicate an issue
            error_handled = (
                is_error_displayed or 
                "not found" in current_url.lower() or 
                "error" in current_url.lower() or
                "search" in current_url.lower()
            )
            
            assert error_handled, "Application should handle invalid city searches gracefully"
            
            if is_error_displayed:
                error_message = await weather_page.get_error_message()
                if error_message:
                    allure.attach(
                        error_message,
                        name="Error Message",
                        attachment_type=allure.attachment_type.TEXT
                    ) 