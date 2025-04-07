from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.settings import IMPLICIT_WAIT
import time

class TestExecutor:
    def __init__(self, driver=None):
        self.driver = driver or self._create_driver()
        
    def _create_driver(self):
        driver = webdriver.Chrome()
        driver.implicitly_wait(IMPLICIT_WAIT)
        return driver
        
    def execute_script(self, script_lines):
        results = []
        for line in script_lines:
            try:
                print(f"Executing: {line}")
                exec(line, {'driver': self.driver, 'By': By, 
                           'WebDriverWait': WebDriverWait, 'EC': EC})
                results.append("PASS")
            except Exception as e:
                results.append(f"FAIL: {str(e)}")
        return results

    def close(self):
        if self.driver:
            self.driver.quit()