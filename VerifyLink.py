#coding:utf-8
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

class VerifyLink(object):
	"""docstring for VerifyLink"""
	def __init__(self):
		#设置浏览器USER-AGENT,再调用浏览器
		dcap = dict(DesiredCapabilities.CHROME)
		dcap["chrome.page.setting.userAgent"] = (
			"Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30")

	def verify(self,url):
		if url != None:
			#将验证过程浏览器弹窗进行隐藏
			self.options = webdriver.ChromeOptions()
			self.options.add_argument('--headless')
			self.options.add_argument('--disable-gpu')
			self.driver = webdriver.Chrome(chrome_options = self.options)
			self.driver.get(url)
			self.driver.implicitly_wait(5)
			self.driver.quit()
		else:
			print 'The email without POP3 couldnt be verified,please verify artifically'
