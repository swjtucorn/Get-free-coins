#coding:utf-8
from HtmlRegister import HtmlRegister
from DataOutput import DataOutput
from GetVerifyLink import GetVerifyLink
from VerifyLink import VerifyLink
import random
import time
import re
import sys

class RegisterMan(object):
 	"""docstring for RegisterMan"""
 	def __init__(self):
 		self.register = HtmlRegister()
 		self.output = DataOutput()
 		self.getlink = GetVerifyLink()
 		self.verifylink = VerifyLink()

 	def crawl(self,name,phone,email,password):
 		try:
 			self.register.openhtml()
 			data = self.register.register(name,phone,email,password)
 			#判断是否注册成功
 			if data[4]:
	 			time.sleep(3)
	 			#判断是否成功获取验证链接
	 			while True:
		 			link = self.getlink.getlink(email,password)
		 			#先判断邮箱是否打开POP3服务
		 			if link != None:
		 				#利用正则表达式再判断链接是否为验证链接
		 				#若非验证链接则等待2s继续读取
		 				if len(re.findall(r'https://oju.io/t/',link))!=0:
		 					break
	 					else:
	 						time.sleep(2)
					else:
						break
				if link != None:
					self.verifylink.verify(link)
					coin = self.register.getcoin()
					data.append(coin)
					self.output.store_data(data)
					self.register.quithtml()
				else:
					data[4] = False
					self.output.store_data(data)
					self.register.quithtml()
			else:
				self.output.store_data(data)
 				self.register.quithtml()
		except Exception as e:
			print e,'registerman failed'
			data[4] = False
			self.output.store_data(data)
			self.register.quithtml()

	def crawl_end(self):
		self.output.output_end()
		print 'crawl finished'



if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')
	register = RegisterMan()
	filename = '002.txt'
	with open(filename,'r') as f:
		for line in f.readlines():
			linestr = line.strip()
			linestrlist = linestr.split('----')
			print linestrlist
			try:
				email = linestrlist[0]
				password = linestrlist[1]
				name = ''
				for j in range(10):
					a = random.randint(97,122)
					c = chr(a)
					name+=c
				phone = '1'
				for k in range(10):
					a = random.randint(0,9)
					c = str(a)
					phone+=c
				register.crawl(name,phone,email,password)
			except Exception as e:
				print e,'main_input failed'
			time.sleep(5)
		register.crawl_end()

	
