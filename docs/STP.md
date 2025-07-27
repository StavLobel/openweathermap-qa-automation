# Software Test Plan (STP)

## 1. Test Objectives
- ✅ Verify UI, API, and end-to-end flows of OpenWeatherMap application.
- ✅ Ensure correctness, stability, and performance of all layers.
- ✅ Automate CI execution and reporting.
- ✅ Simulate real-world use cases across multiple scenarios.

## 2. Scope

### In-Scope
- ✅ UI tests using Playwright for real browser simulation.
- ✅ API testing with Playwright's APIRequestContext module.
- ✅ E2E testing covering full workflows.
- ✅ Non-functional validations: basic performance + accessibility.

### Out-of-Scope
- Load/stress testing beyond functional validation.
- Native mobile testing.

## 3. Assumptions
- ✅ API endpoints are accessible and under a free usage quota.
- ✅ GitHub runners are used for CI/CD.
- ✅ Secrets (e.g. API keys) are securely managed via GitHub Secrets.

## 4. Test Strategy
- ✅ Structured test modules for each layer.
- ✅ Use of Pytest fixtures, markers, and parameterization.
- ✅ Automatic Allure reporting and GitHub Actions workflows.
- ✅ Retry failed flaky tests and capture videos/screenshots.

## 5. Test Types

| Type             | Status | Description                                                      |
|------------------|--------|------------------------------------------------------------------|
| Functional       | ✅     | DOM elements, navigation, field validations                      |
| API              | ✅     | Playwright-based tests of endpoints, status codes, payloads      |
| E2E              | ✅     | Full user journeys (e.g., login → fetch weather → logout)        |
| Non-Functional   | 🚧     | Tracing for performance metrics, basic a11y checks (axe-core)    |

## 6. Tools

| Tool               | Status | Usage                               |
|--------------------|--------|--------------------------------------|
| Playwright (Python)| ✅     | UI + API + E2E testing               |
| Pytest             | ✅     | Test runner & structure              |
| Allure             | ✅     | Reporting and test traceability      |
| GitHub Actions     | ✅     | CI/CD for test execution             |
| GitHub Pages       | ✅     | Publish reports after each run       |
| Black              | ✅     | Code formatting                      |
| Flake8             | ✅     | Code linting                         |
| MyPy               | ✅     | Type checking                        |

## 7. CI/CD Plan
- ✅ All tests run on every push/PR to `main`.
- ✅ Test artifacts uploaded and reports deployed.
- ✅ Linting + formatting checks (black, flake8, mypy).
- ✅ Fail builds on test errors, low coverage, or format violations.

## 8. Test Case Examples (Implemented)

| Test ID | Title                      | Type  | Status | Description                                     | Steps                                               | Expected Result              |
|--------|----------------------------|-------|--------|-------------------------------------------------|------------------------------------------------------|------------------------------|
| UI-001 | Verify search field works  | UI    | ✅     | Ensure city input accepts text                  | Go to page → Type → Submit                          | Data fetched & displayed     |
| API-001| GET /weather valid query   | API   | ✅     | Validate 200 OK for valid city param            | Use APIRequestContext → Call API                    | Status 200 + valid response  |
| E2E-001| Full weather lookup flow   | E2E   | ✅     | Search → View → Logout                          | Simulate user journey                               | All steps pass successfully  |
| NF-001| Basic performance check     | NF    | 🚧     | Capture response time and check thresholds      | Use tracing context in Playwright                   | Response time < 2s           |

## 9. Framework Architecture

### ✅ Implemented Components

#### **Configuration Management**
- Pydantic-based settings with environment variable support
- Type-safe configuration validation
- Environment-specific configurations (test, ci, production)

#### **Page Object Model**
- Base page class with common functionality
- Weather page implementation with robust selectors
- Error handling and fallback mechanisms

#### **API Testing Framework**
- WeatherAPIClient using Playwright's APIRequestContext
- Response validation and schema checking
- Error handling and retry mechanisms

#### **Test Infrastructure**
- Comprehensive pytest fixtures for all test types
- Async support for Playwright operations
- Screenshot and video capture on failures
- Multi-browser support (Chromium, Firefox, WebKit)

#### **CI/CD Pipeline**
- GitHub Actions workflows for testing and code quality
- Multi-browser matrix testing
- Allure report generation and deployment
- Code coverage reporting

## 10. Test Execution Strategy

### **Local Development**
```bash
# Run all tests
pytest

# Run specific test types
pytest tests/ui/ -m ui
pytest tests/api/ -m api
pytest tests/e2e/ -m e2e

# Run with specific browser
pytest --browser firefox

# Run in headed mode
pytest --headed
```

### **CI/CD Execution**
- **Trigger**: Push to main/develop or pull requests
- **Matrix**: Python 3.11/3.12 × Chromium/Firefox/WebKit
- **Parallel**: Multi-worker execution for faster results
- **Artifacts**: Test results, screenshots, videos, traces

## 11. Reporting Strategy

### **Allure Reports**
- Rich HTML reports with test steps
- Screenshots and videos attached to failures
- Trend analysis and defect tracking
- GitHub Pages deployment for accessibility

### **Coverage Reports**
- HTML coverage reports in `reports/coverage/`
- XML coverage for CI/CD integration
- Coverage thresholds (80% minimum)

### **Test Metrics**
- Test execution time tracking
- Pass/fail rates by test type
- Browser compatibility matrix
- Performance benchmarks

## 12. Risk Mitigation

### **High Risk**: API Rate Limiting
- **Mitigation**: Implement request caching and rate limiting
- **Monitoring**: Track API usage and response times
- **Fallback**: Mock data for offline testing

### **Medium Risk**: Browser Compatibility
- **Mitigation**: Multi-browser testing matrix
- **Monitoring**: Cross-browser test results
- **Fallback**: Chromium as primary browser

### **Low Risk**: Test Data Management
- **Mitigation**: Faker library for test data generation
- **Monitoring**: Test data consistency checks
- **Fallback**: Static test data sets

## 13. Success Metrics

### **Quality Metrics**
- ✅ Code coverage > 80%
- ✅ Test reliability > 95%
- ✅ Zero critical bugs in production
- ✅ All CI/CD checks passing

### **Performance Metrics**
- 🎯 API response time < 2 seconds
- 🎯 UI page load time < 3 seconds
- 🎯 Test execution time < 10 minutes
- 🎯 Parallel execution efficiency > 80%

### **Maintenance Metrics**
- ✅ Zero technical debt
- ✅ All dependencies up to date
- ✅ Documentation completeness > 90%
- ✅ Code review coverage 100%
