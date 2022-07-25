from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
class TestExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = webdriver.Chrome()

    def test_testform2(self):
        self.selenium.get('http://127.0.0.1:8000/account/signup')
        player_name = self.selenium.find_element('name','name')
        player_email = self.selenium.find_element('name','email')
        player_password= self.selenium.find_element('name','pass')
        submit =  self.selenium.find_element('name','but1')
        player_name.send_keys('Aravind')
        player_email.send_keys('aravind2021b@mca.ajce.in')
        player_password.send_keys('Aravind@123')
        submit.send_keys(Keys.RETURN)

        player_email = self.selenium.find_element('name','email')
        player_password= self.selenium.find_element('name','pass')
        submit =  self.selenium.find_element('name','button')
        player_email.send_keys('aravind2021b@mca.ajce.in')
        player_password.send_keys('Aravind@123')

        submit.send_keys(Keys.RETURN)
        self.selenium.get('http://127.0.0.1:8000/account/cus_home')



        # self.selenium.get('http://127.0.0.1:8000/account/search')



