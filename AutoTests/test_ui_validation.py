import os
import pytest


def full_path(relative):
    return os.path.abspath(relative)


def test_unsupported_file_format(driver, config, login_page, upload_page):
    driver.get(config["UI"]["login_page"])
    login_page.login("user", "pwd")

    driver.get(config["UI"]["upload_page"])
    file_path = full_path(config["TestFiles"]["unsupported"])
    upload_page.upload_file(file_path)

    assert "unsupported" in upload_page.get_error_message().lower()


def test_exceed_page_limit(driver, config, login_page, upload_page):
    driver.get(config["UI"]["login_page"])
    login_page.login("user", "pwd")

    driver.get(config["UI"]["upload_page"])
    file_path = full_path(config["TestFiles"]["too_many_pages"])
    upload_page.upload_file(file_path)

    assert "exceeded" in upload_page.get_error_message().lower()

def test_corrupted_file(driver, config, login_page, upload_page):
    driver.get(config["UI"]["login_page"])
    login_page.login("user", "pwd")

    driver.get(config["UI"]["upload_page"])
    file_path = full_path(config["TestFiles"]["corrupted"])
    upload_page.upload_file(file_path)

    assert "corrupt" in upload_page.get_error_message().lower()


def test_large_file(driver, config, login_page, upload_page):
    driver.get(config["UI"]["login_page"])
    login_page.login("user", "pwd")

    driver.get(config["UI"]["upload_page"])
    file_path = full_path(config["TestFiles"]["large_file"])
    upload_page.upload_file(file_path)

    assert "exceeds" in upload_page.get_error_message().lower()

def test_cancel_upload(driver, config, login_page, upload_page):
    driver.get(config["UI"]["login_page"])
    login_page.login("user", "pwd")

    driver.get(config["UI"]["upload_page"])
    file_path = full_path(config["TestFiles"]["valid_pdf"])

    upload_page.upload_file(file_path)
    upload_page.cancel_upload()

    assert upload_page.get_displayed_filename() == ""


def test_zero_byte_file(driver, config, login_page, upload_page):
    driver.get(config["UI"]["login_page"])
    login_page.login("user", "pwd")

    driver.get(config["UI"]["upload_page"])
    file_path = full_path(config["TestFiles"]["zero_byte"])
    upload_page.upload_file(file_path)

    assert "empty" in upload_page.get_error_message().lower()


def test_responsive_mobile(driver, config):
    mobile = driver.set_window_size(375, 812)  
    driver.get(config["UI"]["upload_page"])

    assert driver.find_element("id", "upload-btn").is_displayed()
    assert driver.find_element("id", "file-upload").is_displayed()


def test_multiple_file_selection(driver, config, login_page, upload_page):
    driver.get(config["UI"]["login_page"])
    login_page.login("user", "pwd")

    driver.get(config["UI"]["upload_page"])
    
    files = [
        full_path(f.strip()) 
        for f in config["TestFiles"]["multiple_files"].split(",")
    ]

    input_elem = driver.find_element("id", "file-upload")
    input_elem.send_keys("\n".join(files))

    displayed = upload_page.get_displayed_filename()

    assert "multi" in displayed.lower()

def test_filename_display(driver, config, login_page, upload_page):
    driver.get(config["UI"]["login_page"])
    login_page.login("user", "pwd")

    driver.get(config["UI"]["upload_page"])
    file_path = full_path(config["TestFiles"]["valid_pdf"])
    upload_page.upload_file(file_path)

    assert "pdf" in upload_page.get_displayed_filename().lower()

def test_upload_button_disabled(driver, config, login_page, upload_page):
    driver.get(config["UI"]["login_page"])
    login_page.login("user", "pwd")

    driver.get(config["UI"]["upload_page"])

    assert upload_page.is_upload_enabled() is False


def test_state_reset_on_refresh(driver, config, login_page, upload_page):
    driver.get(config["UI"]["login_page"])
    login_page.login("user", "pwd")

    driver.get(config["UI"]["upload_page"])

    file_path = full_path(config["TestFiles"]["valid_pdf"])
    upload_page.upload_file(file_path)

    driver.refresh()

    assert upload_page.get_displayed_filename() == ""
