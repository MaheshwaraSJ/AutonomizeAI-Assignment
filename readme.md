# Automation Framework – AI Model, UI & Security Validation

This repo contains an automation framework that validates:

1. **AI Model Integration** (backend API tests using `requests`)
2. **UI Error Handling & UX Validation** (using Selenium WebDriver)
3. **Security & Rate Limiting (DDoS Simulation)** using `requests`
4. **Automation readiness for CI/CD pipelines**

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

## CI/CD Integration:

Pipeline configs are added under:

```
.github/workflows/ci.yml
```
