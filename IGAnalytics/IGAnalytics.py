import time
import sys
import random
# import datetime
import os.path
# import numpy as np

from IGAnalytics.IGSaleStats import StatFinder as SaleStats
from explicit import waiter, XPATH  # , NAME, CSS
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class IGAnalytics:
    def __init__(self, username, password, actionstring, inspoaccounts, inspohashtags):
        self.username = username
        self.password = password
        self.actionString = str(actionstring)
        self.inspoAccounts = (str(inspoaccounts).split('|', 30))
        self.inspoHashtags = (str(inspohashtags).split('|', 30))
        self.hashtags = []
        chrome_options2 = Options()
        chrome_options2.add_experimental_option("mobileEmulation", {"deviceName": "Galaxy S5"})
        self.driver = WebDriver(executable_path="venv/Lib/chromedriver_win32/chromedriver.exe",
                                chrome_options=chrome_options2)
        self.driver.set_window_size(331, 731)
        self.driver.delete_all_cookies()

    # region UTILITY METHODS

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
        time.sleep(random.randint(1, 2))
        username_element = driver.find_element_by_xpath("//input[@name='username']")
        username_element.clear()
        username_element.send_keys(self.username)
        time.sleep(random.randint(1, 3))
        password_element = driver.find_element_by_xpath("//input[@name='password']")
        password_element.clear()
        password_element.send_keys(self.password)
        time.sleep(random.randint(2, 3))
        password_element.send_keys(Keys.ENTER)
        time.sleep(random.randint(1, 2))

    def logout(self):
        self.driver.close()

    '''
    def resolve_actions_to_perform(self):
        if self.actionString[0] == 'y':
            self.debug_method()
    '''

    def ensure_folder_system_exists(self):
        if not os.path.exists(os.path.join(os.path.dirname(__file__) + '/Photos/', self.username)):
            os.makedirs(os.path.join(os.path.dirname(__file__) + '/Photos/', self.username))
        for inspo in self.inspoAccounts:
            if not os.path.exists(os.path.join(os.path.dirname(__file__) + '/Photos/', self.username, ('@' + inspo))):
                os.makedirs(os.path.join(os.path.dirname(__file__) + '/Photos/', self.username, ('@' + inspo)))
        for inspo in self.inspoHashtags:
            if not os.path.exists(os.path.join(os.path.dirname(__file__) + '/Photos/', self.username, ('#' + inspo))):
                os.makedirs(os.path.join(os.path.dirname(__file__) + '/Photos/', self.username, ('#' + inspo)))

    @staticmethod
    def clean_path(path):
        new_path = (str(path)).replace('\\', '/', 10)
        new_path2 = new_path.replace('/', '\\', 10)
        return new_path2

    @staticmethod
    def debug_method(self):
        # incomplete
        a = 1
    # endregion

    def combomash_method(self):
        first_hashtag = input('What hashtag do you want to use as the first reference: ')
        while True:
            what_is_second_ref = input('Do you want to use a location or a second hashtag as your second source '
                                       '(enter H ''for hashtag and L for location): ')
            if (what_is_second_ref == 'h') or (what_is_second_ref == 'h'):
                # second_ref = input('What hashtag do you want to use as the second reference: ')
                break
            elif (what_is_second_ref == 'l') or (what_is_second_ref == 'L'):
                # holder = input('What location do you want to use as the second reference: ')
                # second_ref = self.resolveLocation(holder)
                break
            else:
                print('Please pic chose one of the two options')
        num_to_act = int(input('How many pictures from each source do you want to get: '))

        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + first_hashtag + "/")
        time.sleep(random.randint(3, 5))
        pic_hrefs = []
        hrefs_scraped = 0
        all_hrefs = []

        while hrefs_scraped <= num_to_act:
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randint(2, 7))
                all_hrefs = driver.find_elements_by_tag_name('a')
                all_hrefs = [elem.get_attribute('href') for elem in all_hrefs if '.com/p/'
                             in elem.get_attribute('href')]
                [pic_hrefs.append(href) for href in all_hrefs if href not in pic_hrefs]
                hrefs_scraped = pic_hrefs.__len__()
            except Exception:
                # self.error_file.write('Exception thrown when getting hrefs for #' + first_hashtag)
                continue
        first_hrefs = []
        counter = 0
        for h in all_hrefs:
            if counter < num_to_act:
                if not first_hrefs.__contains__(h):
                    first_hrefs.append(h)
                    counter += 1
            else:
                break

        if (what_is_second_ref == 'h') or (what_is_second_ref == 'h'):
            driver.get("https://www.instagram.com/explore/tags/" + first_hashtag + "/")
        # else:
            # driver.get("https://www.instagram.com/explore/locations/" + second_ref + "/")

        time.sleep(random.randint(3, 7))
        pic_hrefs = []
        hrefs_scraped = 0
        while hrefs_scraped <= num_to_act:
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randint(2, 7))
                all_hrefs = driver.find_elements_by_tag_name('a')
                all_hrefs = [elem.get_attribute('href') for elem in all_hrefs if '.com/p/'
                             in elem.get_attribute('href')]
                [pic_hrefs.append(href) for href in all_hrefs if href not in pic_hrefs]
                hrefs_scraped = pic_hrefs.__len__()
            except Exception:
                # self.errorFile.write('Exception thrown when getting hrefs for #' + first_hashtag)
                continue
        second_hrefs = []
        counter = 0
        for h in all_hrefs:
            if counter < num_to_act:
                if not second_hrefs.__contains__(h):
                    second_hrefs.append(h)
                    counter += 1
            else:
                break
        self.compare_hrefs(first_hrefs, second_hrefs)

    def compare_hrefs(self, hrefs1, hrefs2):
        driver = self.driver
        first_user_array = []
        second_user_array = []
        for h1 in hrefs1:
            driver.get(h1)
            time.sleep(random.randint(1, 3))
            username_link = driver.find_element_by_xpath('// *[ @ id = "react-root"] / section '
                                                         '/ main / div / div / article / header '
                                                         '/ div[2] / div[1] / div[1] / h2 / a')
            user1 = username_link.text
            first_user_array.append(user1)
            time.sleep(random.randint(1, 3))
        for h2 in hrefs2:
            driver.get(h2)
            time.sleep(random.randint(1, 3))
            username_link = driver.find_element_by_xpath('// *[ @ id = "react-root"] / section /'
                                                         ' main / div / div / article / header /'
                                                         ' div[2] / div[1] / div[1] / h2 / a')
            user2 = username_link.text
            second_user_array.append(user2)
            time.sleep(random.randint(1, 3))

        '''
        first_user_array = np.array(first_user_array)
        second_user_array = np.array(second_user_array)
        result_user_array = np.intersect1d(first_user_array, second_user_array)

        self.userleadsFile.write('User Leads:\n')
        self.userleadsFile.write('Started At: ' + datetime.datetime.now().strftime("%I%M%p_%d%b%y") + '\n')
        self.userleadsFile.write('Total objects compared: ' + (hrefs1.count() * 2) + '\n\n')

        self.userleadsFile.write('Users in both sources: ' '\n')
        for u in result_user_array:
            self.userleadsFile.write(u + '\n')
        if result_user_array.count() == 0:
            self.userleadsFile('None.\n')
        self.userleadsFile.write('Stopped At: ' + datetime.datetime.now().strftime("%I%M%p_%d%b%y") + '\n\n')
        self.userleadsFile.close()
        '''

    def check_for_following(self):
        driver = self.driver
        time.sleep(5)
        driver.get('https://www.instagram.com/' + self.username + '/')
        followers_string = "//a[@href='/" + self.username + "/followers/']"
        waiter.find_element(driver, followers_string, by=XPATH).click()
        time.sleep(random.randint(2, 4))
        user_hrefs = []
        all_hrefs = ""
        # hrefs_scraped = 0
        counter = 0
        while counter < 4:
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randint(4, 5))
                all_hrefs = driver.find_elements_by_tag_name('a')
                all_hrefs = [elem.get_attribute('href') for elem in all_hrefs if
                             '.com/' in elem.get_attribute('href')]
                all_user_hrefs = []
                for ref in all_hrefs[19:]:
                    u = list(ref.split("/"))
                    if u.__len__() == 5:
                        if (u[3] != 'explore') or (u[3] != self.username):
                            all_user_hrefs.append(u)
                [user_hrefs.append(href) for href in all_user_hrefs if href not in user_hrefs]
                # hrefs_scraped = user_hrefs.__len__()
            except Exception:
                # self.errorFile.write('Exception thrown when getting hrefs for people that follow you')
                continue
            counter += 1
        href = []
        counter = 0
        for h in all_hrefs:
            if counter < 100:
                if not href.__contains__(h):
                    href.append(h)
                    counter += 1
            else:
                break
        return href


# region MAIN
if __name__ == "__main__":
    myIG = IGAnalytics(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    # linked in my sale stat file after I cleaned it up
    myIGSale = SaleStats()
    myIGSale.core()
    try:
        myIG.login()
        # myIG.resolveActionsToPerform()
        myIG.logout()
    except Exception:
        a = 1
        myIG.logout()
# endregion
