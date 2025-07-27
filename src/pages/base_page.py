"""Base page class for Page Object Model implementation."""

from typing import Any, Optional
from playwright.async_api import Page, Locator, expect
from src.config import get_settings
from src.utils import get_logger


class BasePage:
    """Base page class providing common functionality for all page objects."""
    
    def __init__(self, page: Page) -> None:
        """Initialize base page.
        
        Args:
            page: Playwright page instance.
        """
        self.page = page
        self.settings = get_settings()
        self.logger = get_logger(self.__class__.__name__)
        
    async def navigate_to(self, url: str) -> None:
        """Navigate to a specific URL.
        
        Args:
            url: URL to navigate to.
        """
        self.logger.info(f"Navigating to: {url}")
        await self.page.goto(url)
        
    async def wait_for_page_load(self) -> None:
        """Wait for page to be fully loaded."""
        await self.page.wait_for_load_state("networkidle")
        
    async def get_title(self) -> str:
        """Get page title.
        
        Returns:
            Page title.
        """
        return await self.page.title()
        
    async def get_url(self) -> str:
        """Get current page URL.
        
        Returns:
            Current URL.
        """
        return self.page.url
        
    async def click_element(self, locator: str | Locator) -> None:
        """Click an element.
        
        Args:
            locator: Element locator string or Locator object.
        """
        element = self.page.locator(locator) if isinstance(locator, str) else locator
        await element.click()
        self.logger.info(f"Clicked element: {locator}")
        
    async def fill_input(self, locator: str | Locator, text: str) -> None:
        """Fill input field with text.
        
        Args:
            locator: Input element locator.
            text: Text to fill.
        """
        element = self.page.locator(locator) if isinstance(locator, str) else locator
        await element.fill(text)
        self.logger.info(f"Filled input {locator} with: {text}")
        
    async def get_text(self, locator: str | Locator) -> str:
        """Get text content of an element.
        
        Args:
            locator: Element locator.
            
        Returns:
            Element text content.
        """
        element = self.page.locator(locator) if isinstance(locator, str) else locator
        return await element.text_content() or ""
        
    async def is_visible(self, locator: str | Locator) -> bool:
        """Check if element is visible.
        
        Args:
            locator: Element locator.
            
        Returns:
            True if element is visible, False otherwise.
        """
        element = self.page.locator(locator) if isinstance(locator, str) else locator
        return await element.is_visible()
        
    async def wait_for_element(self, locator: str | Locator, timeout: Optional[int] = None) -> None:
        """Wait for element to be visible.
        
        Args:
            locator: Element locator.
            timeout: Timeout in milliseconds.
        """
        timeout = timeout or self.settings.browser_timeout
        element = self.page.locator(locator) if isinstance(locator, str) else locator
        await element.wait_for(state="visible", timeout=timeout)
        
    async def expect_element_visible(self, locator: str | Locator) -> None:
        """Assert that element is visible.
        
        Args:
            locator: Element locator.
        """
        element = self.page.locator(locator) if isinstance(locator, str) else locator
        await expect(element).to_be_visible()
        
    async def expect_text_content(self, locator: str | Locator, expected_text: str) -> None:
        """Assert element contains expected text.
        
        Args:
            locator: Element locator.
            expected_text: Expected text content.
        """
        element = self.page.locator(locator) if isinstance(locator, str) else locator
        await expect(element).to_contain_text(expected_text)
        
    async def take_screenshot(self, name: str) -> None:
        """Take a screenshot.
        
        Args:
            name: Screenshot file name.
        """
        await self.page.screenshot(path=f"reports/screenshots/{name}.png")
        self.logger.info(f"Screenshot saved: {name}.png") 