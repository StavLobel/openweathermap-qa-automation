# OpenWeatherMap QA Automation Framework

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)
![Allure](https://img.shields.io/badge/Allure-F7931E?style=for-the-badge&logo=allure&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

[![Tests](https://github.com/username/openweathermap-qa-automation/actions/workflows/tests.yml/badge.svg)](https://github.com/username/openweathermap-qa-automation/actions/workflows/tests.yml)
[![Code Quality](https://github.com/username/openweathermap-qa-automation/actions/workflows/code-quality.yml/badge.svg)](https://github.com/username/openweathermap-qa-automation/actions/workflows/code-quality.yml)
[![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen)](https://github.com/username/openweathermap-qa-automation/actions)

A professional-grade QA Automation framework for comprehensive testing of OpenWeatherMap services. This framework demonstrates advanced testing skills using Python, Pytest, and Playwright, supporting UI, API, E2E, and non-functional testing with full CI/CD integration.

## 🌟 Features

### Multi-Layer Testing
- **UI Testing**: Browser automation with Playwright across multiple browsers
- **API Testing**: RESTful API testing using Playwright's APIRequestContext
- **E2E Testing**: Complete user journey validations
- **Non-Functional Testing**: Performance and accessibility testing

### Advanced Framework Capabilities
- **Page Object Model**: Maintainable and scalable UI test architecture
- **Data-Driven Testing**: Parameterized tests with multiple data sets
- **Cross-Browser Testing**: Support for Chromium, Firefox, and WebKit
- **Parallel Execution**: Fast test execution with pytest-xdist
- **Rich Reporting**: Allure reports with screenshots and videos
- **CI/CD Integration**: Full GitHub Actions pipeline

### Quality Assurance
- **Code Quality**: Black formatting, Flake8 linting, MyPy type checking
- **Test Coverage**: Comprehensive coverage reporting
- **Error Handling**: Robust error handling and retry mechanisms
- **Logging**: Structured logging with color-coded output

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- Git
- OpenWeatherMap API key (free at [openweathermap.org](https://openweathermap.org/api))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/username/openweathermap-qa-automation.git
   cd openweathermap-qa-automation
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenWeatherMap API key
   ```

### Configuration

Create a `.env` file in the project root:

```env
OPENWEATHER_API_KEY=your_api_key_here
ENVIRONMENT=test
DEBUG=false
BROWSER_NAME=chromium
HEADLESS=true
UI_BASE_URL=https://openweathermap.org
```

## 🧪 Running Tests

### All Tests
```bash
pytest
```

### By Test Type
```bash
# UI Tests only
pytest tests/ui/ -m ui

# API Tests only
pytest tests/api/ -m api

# E2E Tests only
pytest tests/e2e/ -m e2e

# Performance Tests
pytest tests/non_functional/ -m performance
```

### By Severity
```bash
# Critical tests only
pytest -m critical

# Smoke tests
pytest -m smoke
```

### Parallel Execution
```bash
# Run tests in parallel with 4 workers
pytest -n 4
```

### Specific Browser
```bash
# Run UI tests in Firefox
pytest tests/ui/ --browser firefox

# Run in headed mode
pytest tests/ui/ --headed
```

## 📊 Reporting

### Allure Reports
```bash
# Generate Allure report
allure serve reports/allure-results

# Generate static report
allure generate reports/allure-results -o reports/allure-report
```

### Coverage Reports
```bash
# Generate coverage report
pytest --cov=src --cov-report=html

# View coverage report
open reports/coverage/index.html
```

## 🏗️ Project Structure

```
openweathermap-qa-automation/
├── .cursor/                    # Cursor IDE rules
├── .github/workflows/          # GitHub Actions CI/CD
├── docs/                       # Project documentation
├── reports/                    # Test reports and artifacts
│   ├── allure-results/
│   ├── coverage/
│   └── html/
├── src/                        # Source code
│   ├── api/                    # API client modules
│   ├── config/                 # Configuration management
│   ├── pages/                  # Page Object Model classes
│   └── utils/                  # Utility functions
├── tests/                      # Test suites
│   ├── api/                    # API tests
│   ├── e2e/                    # End-to-end tests
│   ├── non_functional/         # Performance/accessibility tests
│   └── ui/                     # UI tests
├── pytest.ini                 # Pytest configuration
├── pyproject.toml             # Project configuration
└── requirements.txt           # Python dependencies
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | Required |
| `ENVIRONMENT` | Test environment | `test` |
| `BROWSER_NAME` | Browser for UI tests | `chromium` |
| `HEADLESS` | Run browser in headless mode | `true` |
| `UI_BASE_URL` | Base URL for UI testing | `https://openweathermap.org` |
| `PERFORMANCE_THRESHOLD_MS` | Performance threshold | `2000` |

### Pytest Markers

| Marker | Description |
|--------|-------------|
| `smoke` | Quick smoke tests |
| `regression` | Regression test suite |
| `ui` | UI tests |
| `api` | API tests |
| `e2e` | End-to-end tests |
| `performance` | Performance tests |
| `accessibility` | Accessibility tests |
| `critical` | Critical functionality tests |
| `slow` | Slow-running tests |

## 🌐 API Testing

The framework tests the following OpenWeatherMap APIs:

- **Current Weather**: `/weather`
- **5-Day Forecast**: `/forecast`
- **Geocoding**: `/geo/1.0/direct`

### Example API Test Cases
- Valid city weather requests
- Invalid city handling
- Coordinates-based weather requests
- City ID-based weather requests
- API key validation
- Rate limiting tests
- Response schema validation

## 🖥️ UI Testing

UI tests cover the OpenWeatherMap website functionality:

### Test Scenarios
- Homepage navigation
- City search functionality
- Weather display validation
- Error handling for invalid cities
- Responsive design testing
- Cross-browser compatibility

## 🚦 CI/CD Pipeline

The GitHub Actions pipeline includes:

1. **Code Quality Checks**
   - Black code formatting
   - Flake8 linting
   - MyPy type checking

2. **Test Execution**
   - Multi-browser testing
   - Parallel test execution
   - Coverage reporting

3. **Reporting**
   - Allure report generation
   - Test artifacts upload
   - GitHub Pages deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 code style
- Add type hints to all functions
- Write comprehensive docstrings
- Include unit tests for new features
- Update documentation as needed

## 📋 Test Case Examples

### UI Test Case: City Search
```python
@pytest.mark.ui
@pytest.mark.smoke
@allure.title("Verify city search functionality")
async def test_city_search(weather_page):
    await weather_page.navigate_to_weather_page()
    await weather_page.search_for_city("London")
    assert await weather_page.is_weather_info_displayed()
```

### API Test Case: Weather Data
```python
@pytest.mark.api
@pytest.mark.regression
@allure.title("Get weather data for valid city")
async def test_get_weather_valid_city(weather_api):
    response = await weather_api.get_current_weather("London")
    assert response["status"] == 200
    assert weather_api.validate_weather_response(response["data"])
```

## 📈 Performance Testing

The framework includes basic performance testing:

- Response time validation
- Load time measurements
- Memory usage monitoring
- Network performance analysis

## ♿ Accessibility Testing

Accessibility tests ensure compliance with:

- WCAG 2.1 guidelines
- Screen reader compatibility
- Keyboard navigation
- Color contrast validation

## 🐛 Troubleshooting

### Common Issues

1. **Browser Installation**: Run `playwright install` if browsers are missing
2. **API Key**: Ensure valid OpenWeatherMap API key in `.env`
3. **Dependencies**: Update requirements with `pip install -r requirements.txt`
4. **Permissions**: Check file permissions for report directories

### Debug Mode
```bash
# Run tests with debug logging
pytest --log-cli-level=DEBUG

# Run with video recording
pytest --video=on

# Run with headed browser
pytest --headed
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenWeatherMap](https://openweathermap.org/) for providing the weather API
- [Playwright](https://playwright.dev/) for the excellent testing framework
- [Pytest](https://pytest.org/) for the testing infrastructure
- [Allure](https://docs.qameta.io/allure/) for beautiful test reporting

## 📞 Support

For questions and support:

- Create an [issue](https://github.com/username/openweathermap-qa-automation/issues)
- Check the [documentation](./docs/)
- Review [test cases](./docs/QA_Automation_Test_Cases.md)

---

**Built with ❤️ for QA Excellence** 