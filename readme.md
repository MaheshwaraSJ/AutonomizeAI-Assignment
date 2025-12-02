# Automation Framework – AI Model, UI & Security Validation

This repo contains an automation framework that validates:

1. **AI Model Integration** (backend API tests using `requests`)
2. **UI Error Handling & UX Validation** (using Selenium WebDriver)
3. **Security & Rate Limiting (DDoS Simulation)** using `requests`
4. **Automation readiness for CI/CD pipelines**

---
## AI Model – what we validate and how

The AI model is treated as a pre‑trained service reachable at config['api']['base_url']. Tests send JSON to the model and validate structure, safety, and behavior. Key assertions:

- *Valid patient data*: For each row in valid_patient, POST payload and expect:
  - HTTP 200
  - Response contains risk_level
- *Invalid JSON*: For each row in invalid_json, POST the raw broken_json string:
  - HTTP 200
  - Response error equals expected_error
- *Edge-case text*: For each row in edge_text, POST symptoms as free text:
  - HTTP 200
  - Response contains risk_level and diagnosis is None
- *Irrelevant text*: Parametric check that unrelated prompts return:
  - message == "no medically relevant content"
- *PII masking (phones)*:
  - Send a payload with "phone": generate_random_phone()
  - Ensure the JSON response does not contain any unmasked 10‑digit sequence (\b\d{10}\b)
- *Logs endpoint*:
  - Verify logs endpoint (config['api']['logs_url']) responds with 200 for observability

### Test data (.xlsx)

Test input data for the API (and some UI scenarios) are sourced from an Excel workbook. By default the framework expects an .xlsx file (for example: automation/testdata/testdata.xlsx) that contains one or more sheets matching the test data sets referenced in tests.

Typical expected sheet names and usage:
- valid_patient — rows containing valid patient JSON fields used for positive model integration tests
- invalid_json — rows containing broken_json strings and expected_error values
- edge_text — free-text symptom cases for edge checks
- irrelevant_text — prompts that should yield "no medically relevant content"
- pii_masking — rows used to validate PII redaction (phones, etc.)

Notes:
- Tests read the spreadsheet at runtime (using pandas/openpyxl). Ensure pandas and openpyxl are installed:
  - pip install pandas openpyxl
- The test loader uses the path configured in your test config (e.g., config['testdata']['file']). You can override this by setting the appropriate config value or by providing a path via environment variable if the test harness supports it.
- Keep sheet column names aligned with the test expectations (e.g., 'symptoms', 'broken_json', 'expected_error', 'phone', etc.).

---

## Tech Stack:

### 1. Frontend/UI Automation

* Selenium WebDriver
* Page Object Model (POM)

### 2. Backend Testing

* Requests library (API calls)

### 3. Test Runner

* Pytest

### 4. Optional Integrations

* Docker for containerized test execution
* Spinnaker/GitHub Actions for CI/CD automation

---

## Test Case Summary:

### **1. Model Integration Test (API)**

Validates:

* JSON input schema
* Response structure
* HTTP 200 OK
* Correct risk classification or prediction format

**File:** `test_model_integration.py`

---

### **2. UI Validation Test (Selenium)**

Validates:

* Incorrect file upload format
* Oversized medical chart upload
* Proper UI error messaging
* Smooth user experience

**File:** `test_ui_validation.py`

---

### **3. DDoS Test**

Validates:

* Simulation of **150 requests in 60 seconds** where the policy allows only **120/minute**

**File:** `test_ddos.py`

---

## Running Tests:

### Run all tests

```
pytest automation/tests -v
```

### Run only UI tests

```
pytest automation/tests/test_ui_validation.py -v
```

### Run only API tests

```
pytest automation/tests/test_model_integration.py -v
```

If you want to run tests against a specific testdata workbook, update your test config to point to that .xlsx (e.g., config['testdata']['file'] = "automation/testdata/testdata.xlsx") or set the corresponding environment variable if supported by your test runner.

---

## Reports

Generate a self‑contained HTML report (requires pytest-html):


pytest AutonomizeAI-Assignment/AutoTests/test_model_integration.py -v --html=AutonomizeAI-Assignment/Reports/model_integration_report.html --self-contained-html


Open the report on macOS:


open "./AutonomizeAI-Assignment/Reports/Sample_Report.html"


---

## CI/CD Integration:

Pipeline configs are added under:

```
.github/workflows/ci.yml
```
