import os
import time
import random

import amazonManager
import groupMeBot

class AmznBot(groupMeBot.GroupMeBot):
    def __init__(self, token, botId, groupId):
        super().__init__(token, botId, groupId)

        self.amznManager = amazonManager.AmazonManager()
        self.products = []

        self.functionDict = {
            "!rm": self.removeProduct,
            "!add": self.addProduct,
            "!ls": self.listProducts
        }

    def addProduct(self, url):
        if "https://www.amazon.com" not in url:
            self.postMsg("Invalid URL")
            return

        self.amznManager.loadProduct(url)
        name = self.amznManager.getProductName()
        price = self.amznManager.getPrice()
        imgUrl = self.amznManager.getImgUrl()
        p = {
            "url":url,
            "name":name,
            "price":price,
            "img_url":imgUrl
        }
        self.products.append(p)
        self.postMsg(f"{p['name']}\n{p['price']}", p['img_url'])


    # def checkForNewProducts(self):
    #     for msg in self.getNewMsgs(10):
    #         if "www." in msg['text']:
    #             p = self.getProduct(msg['text'])
    #             self.addProduct(p)

    # def checkForRemovedProducts(self):
    #    for msg in self.getNewMsgs(10):
    #         if "!rm" in msg['text']:
    #             url = msg['text'].split(" ")
    #             for p in self.products:
    #                 if p['url'] == url[1]:
    #                     self.products.remove(p)
    #                     self.postMsg(f"Removed {p['name']}")
    #                 else:
    #                     self.postMsg("Item not in list")

    def listProducts(self):
        msg = ""
        for p in self.products:
            msg += f"{p['name']} - {p['price']}\n\n"
        self.postMsg(msg[:len(msg)-1])

    def removeProduct(self, url):
        for p in self.products:
            if p['url'] == url:
                # print(f"\n{p}\n{url}")
                self.products.remove(p)
                self.postMsg(f"Removed {p['name']}")

    def checkAllProductPrices(self):
        random.shuffle(self.products)
        for p in self.products:
            time.sleep(random.uniform(5, 13))
            updatedProduct = self.getProduct(p['url'])
            if p['price'] != updatedProduct['price']:
                msg = f"{p['name']}\n\n{p['price']} -> {updatedProduct['price']}"
                self.products.remove(p)
                self.addProduct(updatedProduct)

if __name__ == "__main__":
    TOKEN = os.getenv("TOKEN")
    BOT_ID = os.getenv("BOT_ID")
    GROUP_ID = os.getenv("GROUP_ID")

    bot = AmznBot(TOKEN, BOT_ID, GROUP_ID)

    cycles = 0
    while True:
        time.sleep(3)
        # bot.checkForNewProducts()
        # bot.checkForRemovedProducts()
        bot.checkForCommands()
        if cycles >= 120:
            bot.checkAllProductPrices()
            cycles = 0
        cycles += 1