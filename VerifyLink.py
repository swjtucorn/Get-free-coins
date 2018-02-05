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
			self.driver = webdriver.Chrome()
			self.driver.get(url)
			self.driver.implicitly_wait(5)#控制间隔时间，等待浏览器反应
			self.driver.quit()
		else:
			print 'The email without POP3 couldnt be verified,please verify artifically'

if __name__ == '__main__':
	verify = VerifyLink()
	verify.verify('https://oju.io/t/email_verify.php?u=52455&h=b643318eb31ce6112111649f7fce30d11983d16c25266d76c5e97299dde39bb8069a51a52d73903340c3e58f219dac171f18076537af27f58165ddba49fd67b3')