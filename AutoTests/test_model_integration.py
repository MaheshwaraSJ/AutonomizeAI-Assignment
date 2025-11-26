import json
import pytest
import requests
import configparser


config = configparser.ConfigParser()
config.read("config.ini")

BASE_URL = config["api"]["base_url"]
LOGS_URL = config["api"]["logs_url"]
USERB_DATA_URL = config["api"]["userb_data_url"]
TOKEN = config["api"]["token_valid"]
TOKEN_OTHER = config["api"]["token_other_user"]

headers = {
    "Content-Type": "application/json",
    "Authorization": TOKEN
}

def test_valid_patient_data():
    payload = {
        "symptoms": "I have mild fever and body pain",
        "age": 30
    }

    r = requests.post(BASE_URL, headers=headers, json=payload)
    assert r.status_code == 200
    assert "risk_level" in r.json()

def test_invalid_json():
    broken_json = "{symptoms: fever}"  # intentionally invalid

    r = requests.post(BASE_URL, headers=headers, data=broken_json)
    data = r.json()

    assert r.status_code == 200
    assert data.get("error") == "Please Upload Valid JSON"


@pytest.mark.parametrize("text", ["a" * 4000,"fever no have I",
    "I don’t have fever but my temperature is 102"
])
def test_edge_case_text(text):
    payload = {"symptoms": text}

    r = requests.post(BASE_URL, headers=headers, json=payload)

    assert r.status_code == 200
    body = r.json()

    assert "risk_level" in body
    assert body.get("diagnosis") is None

def test_model_does_not_diagnose():
    payload = {"symptoms": "Crushing chest pain with sweating"}

    r = requests.post(BASE_URL, headers=headers, json=payload)
    data = r.json()

    # Should not explicitly diagnose
    assert "heart attack" not in json.dumps(data).lower()
    assert data.get("diagnosis") is None
    assert data.get("guidance") is not None

def test_missing_optional_fields():
    payload = {"symptoms": "I feel dizzy"}

    r = requests.post(BASE_URL, headers=headers, json=payload)
    data = r.json()

    assert r.status_code == 200
    assert "risk_level" in data

@pytest.mark.parametrize("text", ["What is my name?","Hello is anyone here?"])
def test_irrelevant_text(text):
    payload = {"symptoms": text}

    r = requests.post(BASE_URL, headers=headers, json=payload)
    data = r.json()

    assert r.status_code == 200
    assert data.get("message") == "no medically relevant content"

def test_masking_personal_details():
    payload = {
        "symptoms": "I have a cough",
        "phone": "9876543210"
    }

    r = requests.post(BASE_URL, headers=headers, json=payload)
    response_text = json.dumps(r.json()).lower()

 
    assert "9876543210" not in response_text

 
    log_response = requests.get(LOGS_URL, headers=headers)
    assert log_response.status_code == 200

def test_unauthorized_access():
    unauthorized_headers = {
        "Content-Type": "application/json",
        "Authorization": TOKEN_OTHER
    }

    r = requests.get(USERB_DATA_URL, headers=unauthorized_headers)
    assert r.status_code == 403

def test_concurrency_without_threads():
    payload_a = {"symptoms": "fever and cough"}
    payload_b = {"symptoms": "headache and nausea"}

    results = []

    for i in range(50):
        resp1 = requests.post(BASE_URL, headers=headers, json=payload_a)
        resp2 = requests.post(BASE_URL, headers=headers, json=payload_b)
        results.extend([resp1, resp2])

    for r in results:
        assert r.status_code == 200
        assert "risk_level" in r.json()

