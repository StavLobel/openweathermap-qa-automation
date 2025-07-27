# QA Automation Test Cases

This document outlines test cases categorized into UI Functional, API, E2E, and Non-Functional scenarios. Each test includes a unique ID, title, category, description, preconditions, steps, and expected results.

## 🧪 Test Implementation Status

### ✅ Implemented Test Suites
- **UI Tests**: Page Object Model with Playwright
- **API Tests**: Playwright APIRequestContext with validation
- **E2E Tests**: Complete user journey validation
- **Framework**: Comprehensive pytest fixtures and configuration

### 🚧 Framework Ready
- **Non-Functional Tests**: Performance and accessibility testing
- **Advanced Features**: Visual regression, mobile testing

---

## 🖥️ UI Test Cases

### UI-001 - Verify weather page loads successfully
**Category**: UI Functional  
**Status**: ✅ Implemented  
**Description**: Ensure the OpenWeatherMap homepage loads without errors.  
**Preconditions**: User has internet connection.  
**Steps**:  
1. Navigate to OpenWeatherMap homepage.
2. Wait for page to load completely.
3. Verify page title contains "OpenWeatherMap".
4. Verify URL contains "openweathermap.org".
**Expected Result**: Page loads successfully with correct title and URL.

### UI-002 - Verify city search functionality
**Category**: UI Functional  
**Status**: ✅ Implemented  
**Description**: Test that users can search for weather information by city name.  
**Preconditions**: User is on the OpenWeatherMap homepage.  
**Steps**:  
1. Navigate to weather page.
2. Enter valid city name (e.g., "London", "Paris", "Tokyo").
3. Submit search request.
4. Verify search results are displayed.
**Expected Result**: Weather information for the searched city is displayed correctly.

### UI-003 - Verify error handling for invalid city
**Category**: UI Functional  
**Status**: ✅ Implemented  
**Description**: Test that appropriate error messages are shown for invalid city names.  
**Preconditions**: User is on the OpenWeatherMap homepage.  
**Steps**:  
1. Navigate to weather page.
2. Enter invalid city name (e.g., "InvalidCityName123456").
3. Submit search request.
4. Verify error handling.
**Expected Result**: Application handles invalid city searches gracefully with appropriate error messages.

### UI-004 - Verify page accessibility
**Category**: UI Accessibility  
**Status**: ✅ Implemented  
**Description**: Basic accessibility check for the weather page.  
**Preconditions**: User is on the OpenWeatherMap homepage.  
**Steps**:  
1. Navigate to weather page.
2. Check page has meaningful title.
3. Verify basic HTML structure elements exist.
4. Validate page structure for screen readers.
**Expected Result**: Page meets basic accessibility requirements.

---

## 🌐 API Test Cases

### API-001 - GET weather data for valid city
**Category**: API  
**Status**: ✅ Implemented  
**Description**: Request weather data for a valid city using the OpenWeatherMap API.  
**Preconditions**: Valid API key and internet connection.  
**Steps**:  
1. Send GET request to `/weather` with `q=London` and valid API key.
2. Verify response status code is 200.
3. Validate response structure contains required fields.
4. Verify city name in response matches request.
**Expected Result**: Status code 200 with expected weather data JSON structure.

### API-002 - Handle invalid city gracefully
**Category**: API  
**Status**: ✅ Implemented  
**Description**: Test that the API handles invalid city names appropriately.  
**Preconditions**: Valid API key and internet connection.  
**Steps**:  
1. Send GET request to `/weather` with invalid city name.
2. Verify response status code is 404.
3. Validate error response structure.
4. Check error message content.
**Expected Result**: Status code 404 with appropriate error message.

### API-003 - Get weather by coordinates
**Category**: API  
**Status**: ✅ Implemented  
**Description**: Test weather API using geographical coordinates.  
**Preconditions**: Valid API key and internet connection.  
**Steps**:  
1. Send GET request to `/weather` with latitude and longitude parameters.
2. Verify response status code is 200.
3. Validate coordinates in response match input.
4. Verify weather data is returned.
**Expected Result**: Status code 200 with accurate location-based weather data.

### API-004 - Get 5-day weather forecast
**Category**: API  
**Status**: ✅ Implemented  
**Description**: Test 5-day weather forecast endpoint.  
**Preconditions**: Valid API key and internet connection.  
**Steps**:  
1. Send GET request to `/forecast` with valid city name.
2. Verify response status code is 200.
3. Validate forecast response structure.
4. Verify forecast contains multiple entries.
**Expected Result**: Status code 200 with 5-day forecast data.

### API-005 - API response time validation
**Category**: API Performance  
**Status**: ✅ Implemented  
**Description**: Verify API response times are within acceptable limits.  
**Preconditions**: Valid API key and internet connection.  
**Steps**:  
1. Measure response time for weather API call.
2. Compare against performance threshold.
3. Record performance metrics.
**Expected Result**: API response time is less than 5 seconds.

### API-006 - Test different units parameter
**Category**: API  
**Status**: ✅ Implemented  
**Description**: Test weather API with different unit systems.  
**Preconditions**: Valid API key and internet connection.  
**Steps**:  
1. Send requests with different units (metric, imperial, kelvin).
2. Verify response status code is 200.
3. Validate temperature values are in correct range for each unit.
**Expected Result**: Status code 200 with correctly formatted temperature data.

---

## 🔄 E2E Test Cases

### E2E-001 - Complete weather search journey
**Category**: E2E  
**Status**: ✅ Implemented  
**Description**: Test complete user journey from search to weather display.  
**Preconditions**: User has internet connection and valid API access.  
**Steps**:  
1. Validate API is accessible for target city.
2. Navigate to OpenWeatherMap homepage.
3. Search for weather in target city.
4. Verify search results are displayed.
5. Cross-validate with API data.
**Expected Result**: Complete user journey works end-to-end with data consistency.

### E2E-002 - Error handling journey
**Category**: E2E  
**Status**: ✅ Implemented  
**Description**: Test user journey with invalid search input.  
**Preconditions**: User has internet connection and valid API access.  
**Steps**:  
1. Validate API error response for invalid city.
2. Navigate to OpenWeatherMap homepage.
3. Search for invalid city name.
4. Verify error handling is graceful.
**Expected Result**: Application handles invalid searches gracefully with appropriate user feedback.

---

## ⚡ Non-Functional Test Cases

### NF-001 - Basic performance check
**Category**: Performance  
**Status**: 🚧 Framework Ready  
**Description**: Capture response time and check thresholds.  
**Preconditions**: Stable network connection.  
**Steps**:  
1. Use tracing context in Playwright.
2. Measure page load times.
3. Record performance metrics.
4. Compare against benchmarks.
**Expected Result**: Response time is less than 2 seconds.

### NF-002 - Browser compatibility testing
**Category**: Compatibility  
**Status**: 🚧 Framework Ready  
**Description**: Test application across different browsers.  
**Preconditions**: Multiple browsers available.  
**Steps**:  
1. Run tests in Chromium, Firefox, and WebKit.
2. Compare functionality across browsers.
3. Document any browser-specific issues.
**Expected Result**: Application works consistently across all supported browsers.

### NF-003 - Accessibility compliance
**Category**: Accessibility  
**Status**: 🚧 Framework Ready  
**Description**: Verify WCAG 2.1 compliance.  
**Preconditions**: Accessibility testing tools available.  
**Steps**:  
1. Run automated accessibility checks.
2. Verify keyboard navigation.
3. Check color contrast ratios.
4. Validate screen reader compatibility.
**Expected Result**: Application meets WCAG 2.1 AA standards.

---

## 🎯 Test Execution Commands

### Run All Tests
```bash
pytest
```

### Run by Category
```bash
# UI Tests
pytest tests/ui/ -m ui

# API Tests
pytest tests/api/ -m api

# E2E Tests
pytest tests/e2e/ -m e2e

# Performance Tests
pytest tests/non_functional/ -m performance
```

### Run by Severity
```bash
# Critical Tests
pytest -m critical

# Smoke Tests
pytest -m smoke

# Regression Tests
pytest -m regression
```

### Run with Specific Browser
```bash
# Firefox
pytest --browser firefox

# WebKit
pytest --browser webkit

# Headed Mode
pytest --headed
```

---

## 📊 Test Metrics

### Coverage Targets
- **Code Coverage**: >80%
- **Test Reliability**: >95%
- **API Response Time**: <2 seconds
- **UI Page Load Time**: <3 seconds

### Quality Gates
- All critical tests must pass
- Code coverage must meet threshold
- All linting checks must pass
- Performance benchmarks must be met

---

## 🔧 Framework Features

### ✅ Implemented Features
- **Page Object Model**: Maintainable UI test structure
- **API Client**: Professional API testing with validation
- **Test Fixtures**: Comprehensive pytest configuration
- **Multi-Browser Support**: Chromium, Firefox, WebKit
- **Rich Reporting**: Allure integration with attachments
- **CI/CD Integration**: GitHub Actions automation
- **Code Quality**: Black, Flake8, MyPy integration

### 🚧 Planned Features
- **Visual Regression Testing**: Screenshot comparison
- **Mobile Testing**: Responsive design validation
- **Load Testing**: Performance under stress
- **Advanced Monitoring**: Test execution analytics
