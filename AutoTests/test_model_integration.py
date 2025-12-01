import json
import re
import pytest
import requests
import configparser
import os
from utils import generate_random_phone

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


def test_valid_patient_data(excel_reader):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(_file_)))
    xlsx_path = os.path.join(project_root, "TestData", "model_integration_tests.xlsx")
    rows = excel_reader(xlsx_path, "valid_patient")

    for row in rows:
        payload = {"symptoms": row.get("symptoms")}
        age = row.get("age")
        if age is not None:
            try:
                payload["age"] = int(age)
            except Exception:
                pass

        r = requests.post(BASE_URL, headers=headers, json=payload)
        assert r.status_code == 200
        assert "risk_level" in r.json()


def test_invalid_json(excel_reader):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(_file_)))
    xlsx_path = os.path.join(project_root, "TestData", "model_integration_tests.xlsx")
    rows = excel_reader(xlsx_path, "invalid_json")

    for row in rows:
        broken_json = row.get("broken_json")  # intentionally invalid
        expected_error = row.get("expected_error")

        r = requests.post(BASE_URL, headers=headers, data=broken_json)
        data = r.json()

        assert r.status_code == 200
        assert data.get("error") == expected_error


def test_edge_case_text(excel_reader):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(_file_)))
    xlsx_path = os.path.join(project_root, "TestData", "model_integration_tests.xlsx")
    rows = excel_reader(xlsx_path, "edge_text")

    for row in rows:
        text = row.get("text")
        if text is None:
            for v in row.values():
                if v is not None and str(v).strip():
                    text = str(v)
                    break
        if text is None:
            continue

        payload = {"symptoms": text}
        r = requests.post(BASE_URL, headers=headers, json=payload)
        assert r.status_code == 200
        body = r.json()
        assert "risk_level" in body
        assert body.get("diagnosis") is None


@pytest.mark.parametrize("text", ["What is my name?", "Hello is anyone here?"])
def test_irrelevant_text(text):
    payload = {"symptoms": text}

    r = requests.post(BASE_URL, headers=headers, json=payload)
    data = r.json()

    assert r.status_code == 200
    assert data.get("message") == "no medically relevant content"


def test_masking_personal_details():
    payload = {
        "symptoms": "I have a cough",
        "phone": generate_random_phone()
    }

    r = requests.post(BASE_URL, headers=headers, json=payload)
    response_text = json.dumps(r.json()).lower()

    assert not re.search(r"\b\d{10}\b", response_text)


log_response = requests.get(LOGS_URL, headers=headers)
assert log_response.status_code == 200