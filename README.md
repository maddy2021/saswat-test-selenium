# saswat-test-selenium

Pre-requisite:
1. Python3 - make sure you have python verision above 3
2. chrome browser compatible Selenium webdriver 
    -> put that webdriver(chromedriver.exe file for windows) in driver folder
    (You can find driver folder inside the coding-test directory)


To run the code,
1. Check you have python installed
2. pip install -r requirements.txt
3. cd coding_test => make sure you are in coding_test directory
4. python scraper.py [url]    (Pass the url which you want to scrape)
> python scraper.py https://www.abt.com/Apple-128GB-Starlight-iPhone-13-Cellular-Phone-ML953LLA6163D/p/168479.html


output will be stored in output folder in example.json -> file location name : output/example.json
output can be seen in console also.


Assumptions:
1. For now taking just 1st paragraph of description
2. Status of request is 200: sucess for this assignment, but we can add more regarding 404 or 500 error code
-> for our code only handeled one is 200
3. asin and reseller_id is same as product upc
4. analysis folder contains html and script tags json file as well as expected out file.
