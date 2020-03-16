from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class AmazonManager:
    def __init__(self):
        chrome_options = Options()  
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)

    def loadProduct(self, url):
        self.driver.get(url)

    def getPrice(self):
        e = self.driver.find_element_by_xpath("//span[@id='priceblock_ourprice']")
        return e.text

    def getProductName(self):
        e = self.driver.find_element_by_xpath("//span[@id='productTitle']")
        return e.text

    def getImgUrl(self):
        e = self.driver.find_element_by_xpath("//img[@id='landingImage']")
        return e.get_attribute("src")

if __name__ == "__main__":
    am = amazonManager()
    am.loadProduct("https://www.amazon.com/gp/product/B008GRTSV6?pf_rd_r=WJ8EBKP4996F3JHZEWZD&pf_rd_p=ab873d20-a0ca-439b-ac45-cd78f07a84d8")
    print(am.getProductName())
    print(am.getPrice())
    print(am.getImgUrl())