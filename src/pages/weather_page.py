"""Weather page class for OpenWeatherMap UI testing."""

from typing import Optional
from playwright.async_api import Page
from .base_page import BasePage


class WeatherPage(BasePage):
    """Page object for OpenWeatherMap weather page."""
    
    # Locators
    SEARCH_INPUT = "[data-testid='search-input'], input[placeholder*='city'], #search_str"
    SEARCH_BUTTON = "[data-testid='search-button'], button[type='submit'], .search-btn"
    WEATHER_INFO = "[data-testid='weather-info'], .weather-widget, .current-weather"
    TEMPERATURE = "[data-testid='temperature'], .temperature, .heading"
    CITY_NAME = "[data-testid='city-name'], .city-name, h2"
    WEATHER_DESCRIPTION = "[data-testid='description'], .weather-description"
    ERROR_MESSAGE = "[data-testid='error'], .error, .alert"
    
    def __init__(self, page: Page) -> None:
        """Initialize weather page.
        
        Args:
            page: Playwright page instance.
        """
        super().__init__(page)
        
    async def navigate_to_weather_page(self) -> None:
        """Navigate to the weather page."""
        await self.navigate_to(self.settings.ui_base_url)
        await self.wait_for_page_load()
        
    async def search_for_city(self, city_name: str) -> None:
        """Search for weather information for a specific city.
        
        Args:
            city_name: Name of the city to search for.
        """
        self.logger.info(f"Searching for weather in: {city_name}")
        
        # Try multiple possible search input selectors
        search_selectors = [
            self.SEARCH_INPUT,
            "input[name='q']",
            "input[id*='search']",
            "input[placeholder*='Search']"
        ]
        
        search_input = None
        for selector in search_selectors:
            try:
                search_input = self.page.locator(selector).first
                if await search_input.is_visible(timeout=5000):
                    break
            except:
                continue
                
        if search_input:
            await search_input.fill(city_name)
            await search_input.press("Enter")
        else:
            # Fallback to URL navigation if search input not found
            search_url = f"{self.settings.ui_base_url}/find?q={city_name}"
            await self.navigate_to(search_url)
            
        await self.wait_for_page_load()
        
    async def get_temperature(self) -> Optional[str]:
        """Get the current temperature.
        
        Returns:
            Temperature string or None if not found.
        """
        temperature_selectors = [
            self.TEMPERATURE,
            ".temperature",
            ".temp",
            "[class*='temperature']"
        ]
        
        for selector in temperature_selectors:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible(timeout=5000):
                    return await element.text_content()
            except:
                continue
                
        return None
        
    async def get_city_name(self) -> Optional[str]:
        """Get the displayed city name.
        
        Returns:
            City name string or None if not found.
        """
        city_selectors = [
            self.CITY_NAME,
            "h1",
            "h2",
            ".city",
            "[class*='city']"
        ]
        
        for selector in city_selectors:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible(timeout=5000):
                    return await element.text_content()
            except:
                continue
                
        return None
        
    async def get_weather_description(self) -> Optional[str]:
        """Get the weather description.
        
        Returns:
            Weather description string or None if not found.
        """
        description_selectors = [
            self.WEATHER_DESCRIPTION,
            ".description",
            ".weather-desc",
            "[class*='description']"
        ]
        
        for selector in description_selectors:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible(timeout=5000):
                    return await element.text_content()
            except:
                continue
                
        return None
        
    async def is_weather_info_displayed(self) -> bool:
        """Check if weather information is displayed.
        
        Returns:
            True if weather info is visible, False otherwise.
        """
        weather_selectors = [
            self.WEATHER_INFO,
            ".weather",
            ".current-weather",
            "[class*='weather']"
        ]
        
        for selector in weather_selectors:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible(timeout=10000):
                    return True
            except:
                continue
                
        return False
        
    async def is_error_displayed(self) -> bool:
        """Check if error message is displayed.
        
        Returns:
            True if error is visible, False otherwise.
        """
        error_selectors = [
            self.ERROR_MESSAGE,
            ".error",
            ".alert-danger",
            "[class*='error']"
        ]
        
        for selector in error_selectors:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible(timeout=5000):
                    return True
            except:
                continue
                
        return False
        
    async def get_error_message(self) -> Optional[str]:
        """Get error message text.
        
        Returns:
            Error message string or None if not found.
        """
        if await self.is_error_displayed():
            error_selectors = [
                self.ERROR_MESSAGE,
                ".error",
                ".alert-danger",
                "[class*='error']"
            ]
            
            for selector in error_selectors:
                try:
                    element = self.page.locator(selector).first
                    if await element.is_visible(timeout=5000):
                        return await element.text_content()
                except:
                    continue
                    
        return None 