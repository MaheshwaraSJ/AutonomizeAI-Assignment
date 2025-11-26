from selenium.webdriver.common.by import By

class UploadPage:

    def __init__(self, driver):
        self.driver = driver
        self.file_input = (By.ID, "file-upload")
        self.upload_btn = (By.ID, "upload-btn")
        self.cancel_btn = (By.ID, "cancel-btn")
        self.error_msg = (By.ID, "error")
        self.file_name_display = (By.ID, "file-name")

    def upload_file(self, file_path):
        self.driver.find_element(*self.file_input).send_keys(file_path)
        self.driver.find_element(*self.upload_btn).click()

    def cancel_upload(self):
        self.driver.find_element(*self.cancel_btn).click()

    def get_error_message(self):
        return self.driver.find_element(*self.error_msg).text

    def get_displayed_filename(self):
        return self.driver.find_element(*self.file_name_display).text

    def is_upload_enabled(self):
        return self.driver.find_element(*self.upload_btn).is_enabled()
