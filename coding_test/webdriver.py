from selenium import webdriver
import os
from selenium.webdriver.chrome.service import Service
dirname, filename = os.path.split(os.path.abspath(__file__))
CHROME_DRIVER_PATH = os.path.join(dirname,"driver","chromedriver.exe")

class WebDriver():
    def __init__(self,drivername):
        if drivername == 'Firefox':
            print("currently this test is only for chromedriver, you can enhance it by poviding phantomjs drive")
            self.driver = None
        elif drivername == 'ChromeDriver':
            chrome_service = Service(executable_path=CHROME_DRIVER_PATH) 
            # options = webdriver.ChromeOptions() #Helpful to add oprtions
            self.driver = webdriver.Chrome(service=chrome_service)  # provide the chromedriver execution path in case of error
        elif drivername == 'PhantomJS':
            print("currently this test is only for chromedriver, you can enhance it by poviding phantomjs drive")
            self.driver = None
            # self.driver = webdriver.PhantomJS(r"")  

        # self.driver.implicitly_wait(1)  # seconds
		#This tells Selenium that we would like it to wait for a certain amount of time before throwing an exception that if it cannot find the element on the page.
