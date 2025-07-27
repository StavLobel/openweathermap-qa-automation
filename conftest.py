"""Global test configuration and fixtures."""

import asyncio
import pytest
import pytest_asyncio
from typing import AsyncGenerator, Generator
from playwright.async_api import async_playwright, Playwright, Browser, BrowserContext, Page, APIRequestContext

from src.config import get_settings
from src.pages import WeatherPage
from src.api import WeatherAPIClient
from src.utils import get_logger

logger = get_logger(__name__)


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add custom command line options."""
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="Browser to use for testing (chromium, firefox, webkit)",
        choices=["chromium", "firefox", "webkit"]
    )
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run browser in headed mode"
    )
    parser.addoption(
        "--slowmo",
        action="store",
        default=0,
        type=int,
        help="Slow down operations by specified milliseconds"
    )


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def settings():
    """Get application settings."""
    return get_settings()


@pytest_asyncio.fixture(scope="session")
async def playwright() -> AsyncGenerator[Playwright, None]:
    """Initialize Playwright."""
    async with async_playwright() as playwright_instance:
        yield playwright_instance


@pytest_asyncio.fixture(scope="session")
async def browser(playwright: Playwright, request: pytest.FixtureRequest) -> AsyncGenerator[Browser, None]:
    """Launch browser instance."""
    browser_name = request.config.getoption("--browser")
    headed = request.config.getoption("--headed")
    slowmo = request.config.getoption("--slowmo")
    
    # Browser launch options
    launch_options = {
        "headless": not headed,
        "slow_mo": slowmo,
        "args": [
            "--disable-blink-features=AutomationControlled",
            "--disable-extensions",
            "--disable-plugins",
            "--disable-dev-shm-usage",
            "--no-sandbox"
        ]
    }
    
    # Launch the appropriate browser
    if browser_name == "chromium":
        browser_instance = await playwright.chromium.launch(**launch_options)
    elif browser_name == "firefox":
        browser_instance = await playwright.firefox.launch(**launch_options)
    elif browser_name == "webkit":
        browser_instance = await playwright.webkit.launch(**launch_options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    
    logger.info(f"Launched {browser_name} browser")
    yield browser_instance
    await browser_instance.close()


@pytest_asyncio.fixture
async def context(browser: Browser, settings) -> AsyncGenerator[BrowserContext, None]:
    """Create browser context with configuration."""
    context_options = {
        "viewport": {"width": 1920, "height": 1080},
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "locale": "en-US",
        "timezone_id": "America/New_York",
        "permissions": ["geolocation"],
        "record_video_dir": "test-results/videos" if settings.video_mode != "off" else None,
        "record_video_size": {"width": 1920, "height": 1080}
    }
    
    context_instance = await browser.new_context(**context_options)
    
    # Enable tracing for debugging
    await context_instance.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )
    
    yield context_instance
    
    # Stop tracing and save
    await context_instance.tracing.stop(path="test-results/trace.zip")
    await context_instance.close()


@pytest_asyncio.fixture
async def page(context: BrowserContext) -> AsyncGenerator[Page, None]:
    """Create a new page."""
    page_instance = await context.new_page()
    
    # Set default timeout
    page_instance.set_default_timeout(30000)
    page_instance.set_default_navigation_timeout(30000)
    
    # Add console logging for debugging
    page_instance.on("console", lambda msg: logger.info(f"Console: {msg.text}"))
    page_instance.on("pageerror", lambda exc: logger.error(f"Page error: {exc}"))
    
    yield page_instance
    await page_instance.close()


@pytest_asyncio.fixture
async def api_context(playwright: Playwright, settings) -> AsyncGenerator[APIRequestContext, None]:
    """Create API request context."""
    api_context_instance = await playwright.request.new_context(
        base_url=settings.openweather_base_url,
        extra_http_headers={
            "User-Agent": "OpenWeatherMap-QA-Automation/1.0"
        }
    )
    
    yield api_context_instance
    await api_context_instance.dispose()


# Page Object Fixtures
@pytest_asyncio.fixture
async def weather_page(page: Page) -> WeatherPage:
    """Create WeatherPage instance."""
    return WeatherPage(page)


# API Client Fixtures
@pytest_asyncio.fixture
async def weather_api(api_context: APIRequestContext) -> WeatherAPIClient:
    """Create WeatherAPIClient instance."""
    return WeatherAPIClient(api_context)


# Test Data Fixtures
@pytest.fixture
def valid_cities() -> list[str]:
    """List of valid cities for testing."""
    return [
        "London",
        "New York",
        "Tokyo",
        "Paris",
        "Berlin",
        "Sydney",
        "Moscow",
        "Mumbai"
    ]


@pytest.fixture
def invalid_cities() -> list[str]:
    """List of invalid cities for testing."""
    return [
        "InvalidCityName123",
        "NonExistentPlace",
        "zzzzz",
        "12345",
        "",
        "   "
    ]


@pytest.fixture
def test_coordinates() -> list[dict]:
    """List of test coordinates."""
    return [
        {"lat": 51.5074, "lon": -0.1278, "city": "London"},
        {"lat": 40.7128, "lon": -74.0060, "city": "New York"},
        {"lat": 35.6762, "lon": 139.6503, "city": "Tokyo"},
        {"lat": 48.8566, "lon": 2.3522, "city": "Paris"}
    ]


# Hooks and Configuration
def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "smoke: marks tests as smoke tests")
    config.addinivalue_line("markers", "regression: marks tests as regression tests")
    config.addinivalue_line("markers", "ui: marks tests as UI tests")
    config.addinivalue_line("markers", "api: marks tests as API tests")
    config.addinivalue_line("markers", "e2e: marks tests as end-to-end tests")
    config.addinivalue_line("markers", "performance: marks tests as performance tests")
    config.addinivalue_line("markers", "accessibility: marks tests as accessibility tests")
    config.addinivalue_line("markers", "critical: marks tests as critical functionality")
    config.addinivalue_line("markers", "slow: marks tests as slow running")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> Generator:
    """Make test results available to fixtures."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest_asyncio.fixture(autouse=True)
async def handle_test_failure(request: pytest.FixtureRequest, page: Page):
    """Handle test failures by taking screenshots."""
    yield
    
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        # Take screenshot on failure
        screenshot_path = f"test-results/screenshots/{request.node.name}.png"
        await page.screenshot(path=screenshot_path)
        logger.error(f"Test failed. Screenshot saved: {screenshot_path}")


# Custom markers for parametrization
pytest_plugins = ["pytest_asyncio"] 