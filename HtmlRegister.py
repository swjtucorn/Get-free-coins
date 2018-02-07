#coding:utf-8
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class HtmlRegister(object):
	def __init__(self):
		#设置浏览器USER-AGENT,再调用浏览器
		dcap = dict(DesiredCapabilities.CHROME)
		dcap["chrome.page.setting.userAgent"] = (
			"Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30")
	
	def openhtml(self):
		self.driver = webdriver.Chrome()
		url = 'https://oju.io/t/cn/refer/KXyRzss5VEg'
		#控制间隔时间，等待浏览器反应,若无反应则退出脚本
		try:
			self.driver.get(url)
			self.driver.implicitly_wait(10)
		except:
			print e,'Time Out : Your IP has been banned'
			sys.exit()


	def register(self,name,phone,email,password):
		ele_name = self.driver.find_element_by_xpath(".//input[@name='name']")
		ele_phone = self.driver.find_element_by_xpath(".//input[@name='tel_num']")
		ele_email = self.driver.find_element_by_xpath(".//form[@id='frmSignUp']//input[@name='email']")#
		ele_password = self.driver.find_element_by_xpath(".//form[@id='frmSignUp']//input[@name='password']")#
		ele_password_cfm = self.driver.find_element_by_xpath(".//form[@id='frmSignUp']//input[@name='password_cfm']")
		ele_phone_cty = self.driver.find_element_by_xpath(".//option[@value='86']")
		ele_register = self.driver.find_element_by_xpath(".//input[@value='注册']")
		try:
			ele_name.clear()
			ele_name.send_keys(name)
			time.sleep(2)
			ele_phone.clear()
			ele_phone.send_keys(phone)
			time.sleep(2)
			ele_email.clear()
			ele_email.send_keys(email)
			time.sleep(2)
			ele_password.clear()
			ele_password.send_keys(password)
			time.sleep(2)
			ele_password_cfm.clear()
			ele_password_cfm.send_keys(password)
			time.sleep(2)
			ele_phone_cty.click()
			ele_register.click()
			#flag用于判断是否注册成功
			flag = True
			return [name,phone,email,password,flag]
		except Exception as e:
			print e,('name = %s phone = %s email = %s password =%s,register failed'%(name,phone,email,password))
			flag = False
			return [name,phone,email,password,flag]

	def quithtml(self):
		self.driver.quit()

	def getcoin(self):
		ele_icon = self.driver.find_element_by_xpath(".//a[@href='https://oju.io/t/cn/ojut-freecoins']")
		ele_icon.click()
		ele_here = self.driver.find_element_by_xpath('.//a[@href="https://oju.io/t/cn/claim-free-coins"]')
		ele_here.click()
		time.sleep(2)
		ele_coin = self.driver.find_element_by_xpath(".//h1/a[@href='https://oju.io/t/cn/ojut-account']").text
		return ele_coin

