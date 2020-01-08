import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class StatFinder:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    extensions = ["pets-animals", "cars-bikes", "fitness-sports", "food-nutrition", "fashion-style",
                  "photography-travel", "humuor-memes", "luxury-motivation", "art-gaming", "realestate-interior",
                  "vape-smoke", "quotes-texts"]

    names = ['humor / memes', 'quotes / sayings', 'cars / bikes', 'fitness / sports', 'fashion / style',
               'food / nutrition', 'luxury / motivation', 'outdoor / travel', 'pets / animals',
               'models / celebrities', 'movies / tv / fanpages', 'educational / qa', 'gaming / entertainment',
               'reviews / how-to']

    def socialtradia(self, f, driver):
        website = "https://socialtradia.com/"
        category_count = 0
        all_followers = []
        all_prices = []
        all_ratio = []

        f.write("Website: socialtradia\n")
        while len(self.extensions[0]) > category_count:
            all_followers.clear()
            all_prices.clear()
            all_ratio.clear()
            driver.get(website + self.extensions[category_count])
            sale_list = driver.find_elements_by_class_name("""nm-shop-loop-details""")
            if sale_list.__len__() != 0:
                for s in sale_list:
                    all_followers.append(self.parse_followers(s.text))
                    all_prices.append(self.parse_price(s.text))
                ratio_count = 0
                while ratio_count < all_followers.__len__() and ratio_count < all_prices.__len__():
                    all_ratio.append(all_followers[ratio_count] / all_prices[ratio_count])
                    ratio_count += 1
                total = 0
                for ratio in all_ratio:
                    total += ratio
                f.write('    ' + self.extensions[category_count].replace('-', ' / ') + ': ' +
                        str(int(total / all_ratio.__len__())) + "\n")
            else:
                f.write('    ' + self.extensions[category_count].replace('-', ' / ') + ': ' + "No Sales" + "\n")
            category_count += 1

    def fameswap(self, f, driver):
        website = "https://fameswap.com/browse?&social=1&cat=1"
        category_count = 1
        all_followers = []
        all_prices = []
        all_ratio = []

        f.write("\nWebsite: fameswap\n")
        while category_count < 15:
            all_followers.clear()
            all_prices.clear()
            all_ratio.clear()

            driver.get(website[0:website.index("cat=") + 4] + str(category_count))
            sale_list = driver.find_elements_by_class_name("""hidden-xs""")
            sale_count = 0
            for s in sale_list:
                if (sale_count - 4) % 3 == 0 and sale_count != 0 and sale_count != 1:
                    follower = s.text
                    follower = follower.replace('k', '')
                    if 'm' in follower:
                        follower = float(follower.replace('m', ''))
                        follower = follower * 1000
                    all_followers.append(float(follower))
                if (sale_count - 4) % 3 == 1 and sale_count != 2:
                    price = s.text
                    price = price.replace('$', '')
                    price = price.replace(',', '')
                    price = price.replace('.00', '')
                    all_prices.append(int(price))
                sale_count += 1
            if sale_list.__len__() != 0:
                ratio_count = 0
                while ratio_count < all_followers.__len__() and ratio_count < all_prices.__len__():
                    all_ratio.append(all_followers[ratio_count] * 1000 / all_prices[ratio_count])
                    ratio_count += 1
                total = 0
                for ratio in all_ratio:
                    total += ratio
                if all_ratio.__len__() != 0 and total != 0:
                    f.write('    ' + self.names[category_count - 1] + ': ' + str(int(total / all_ratio.__len__()))
                            + "\n")
            else:
                f.write('    ' + self.names[category_count - 1].replace('-', ' / ') + ': ' + "No Sales" + "\n")
            category_count += 1

    @staticmethod
    def parse_price(sale):
        on = False
        price = ""
        for s in sale:
            if on and s == '.':
                return int(price)
            if on and s != ',':
                price += s
            if s == '$':
                on = True

    @staticmethod
    def parse_followers(sale):
        on = False
        followers = ""
        for s in sale:
            if on and (s == ' ' or s == 'k'):
                return float(followers) * 1000
            if on:
                followers += s
            if s == '(':
                on = True

    def core(self):
        driver = self.driver
        # Need Logs folder to work
        path = "Logs/" + str(datetime.datetime.now()) + ".txt"
        file = open(path, "w+")

        self.socialtradia(file, driver)
        self.fameswap(file, driver)

        file.close()
        driver.quit()
        print("Price Finder Complete")


if __name__ == "__main__":
    StatFinder = StatFinder()
    StatFinder.core()
