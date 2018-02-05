#coding:utf-8
import sqlite3

class DataOutput(object):
	def __init__(self):
		self.cx = sqlite3.connect("Ojut.db")
		self.create_table('Ojut')#存储刷币成功的表
		self.create_table('Ojut_failed')#存储刷币成功的表
		self.datas = []
		self.datasfailed = []

	def create_table(self,table_name):
		'''
		创建数据表
		:param table_name:表名称
		:return:
		'''
		values = '''
		id integer primary key,
		Name varchar(40) NOT NULL,
		Phone varchar(40) NOT NULL,
		Email varchar(40) NOT NULL,
		Password varchar(1024) NOT NULL,
		Coin single NOT NULL
		'''
		valuesfailed = '''
		id integer primary key,
		Name varchar(40) NOT NULL,
		Phone varchar(40) NOT NULL,
		Email varchar(40) NOT NULL,
		Password varchar(1024) NOT NULL
		'''
		if table_name == 'Ojut':
			self.cx.execute('CREATE TABLE IF NOT EXISTS %s(%s)'%(table_name,values))
		else:
			self.cx.execute('CREATE TABLE IF NOT EXISTS %s(%s)'%(table_name,valuesfailed))

	def store_data(self,data):
		'''
		数据存储
		:param data:
		:return:
		'''
		if data[4]:
			#存储数据前删掉flag数据
			del data[4]
			self.datas.append(data)
			if len(self.datas)>5:
				self.output_db('Ojut')
		else:
			del data[4]
			self.datasfailed.append(data)
			if len(self.datasfailed)>5:
				self.output_db('Ojut_failed')

	def output_db(self,table_name):
		'''
		将数据存储到sqlite
		:return:
		'''
		if table_name == 'Ojut':
			for data in self.datas:
				self.cx.execute("INSERT INTO %s(Name,"
					"Phone,Email,Password,Coin)VALUES(?,?,?,?,?)"
					""%table_name,data)
				self.datas.remove(data)
		else:
			for data in self.datasfailed:
				self.cx.execute("INSERT INTO %s(Name,"
					"Phone,Email,Password)VALUES(?,?,?,?)"
					""%table_name,data)
				self.datasfailed.remove(data)
		self.cx.commit()

	def output_end(self):
		'''
		关闭数据库
		:return:
		'''
		while len(self.datas)>0:
			self.output_db('Ojut')
		while len(self.datasfailed)>0:
			self.output_db('Ojut_failed')
		self.cx.close()


#测试代码
if __name__ == '__main__':
	store = DataOutput()
	data1 = [[1,2,3,4,False],[2,3,4,5,False],[3,4,5,6,True,8],[4,5,6,7,False],[5,6,7,8,False],[2,3,4,2,True,0]]
	for i in range(len(data1)):
		print data1[i]
		store.store_data(data1[i])
	store.output_end()