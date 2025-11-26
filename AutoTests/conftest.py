import pytest
import configparser
import os
from selenium import webdriver

@pytest.fixture(scope="session")
def config():
    cfg = configparser.ConfigParser()
    path = os.path.join(os.path.dirname(__file__), "config.ini")
    cfg.read(path)
    return cfg


@pytest.fixture
def driver():
 // Init selenium webdriver
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()
