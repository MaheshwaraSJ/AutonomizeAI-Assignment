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
