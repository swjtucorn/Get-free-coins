#coding:utf-8
import poplib
import email
import sys
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from bs4 import BeautifulSoup

class GetVerifyLink(object):	

	def guess_charset(self,msg):
	    charset = msg.get_charset()
	    if charset is None:
	        content_type = msg.get('Content-Type', '').lower()
	        pos = content_type.find('charset=')
	        if pos >= 0:
	            charset = content_type[pos + 8:].strip()
	    return charset

	def decode_str(self,s):
	    value, charset = decode_header(s)[0]
	    if charset:
	        value = value.decode(charset)
	    return value

	def print_info(self,msg,indent=0):
		#首先处理邮件头
		# indent用于缩进显示
	    if indent == 0:
	    	# 获取邮件的From, To, Subject相应的键值
	        for header in ['From', 'To', 'Subject']:
	            value = msg.get(header)
	            '''
	            由于From、To以及Subject的内容形式各不相同，以普通邮件为例：
	            date: Wed, 16 Nov 2016 16:04:44 +0800
				From: 3456789 <3456789@qq.com>
				To: 1234567 <1234567@qq.com>
				Cc: 23456780 <23456780@qq.com>
				Reply-To: 3456789 <3456789@qq.com>
				Subject: email test!
				X-Priority: 3
				X-Has-Attach: no
				X-Mailer: Foxmail 7.0.1.91[cn]
				Mime-Version: 1.0
				Message-ID: <201611161604440653250@qq.com>
				Content-Type: multipart/alternative;
				    boundary="----=_001_NextPart245273401224_=----"
	            因此需要进行分开处理
	            '''
	            if value:
	                if header=='Subject':
	                    value = self.decode_str(value)
	                else:
	                    hdr, addr = parseaddr(value)#parseaddr函数解析出名称与邮箱地址
	                    name = self.decode_str(hdr)
	                    value = u'%s <%s>' % (name, addr)
                #有需要可以打印邮件的'From', 'To', 'Subject'三行消息，去掉下面一行代码前面的#即可
	            #print('%s%s: %s' % ('  ' * indent, header, value))
        #再处理邮件内容对象
        #如果邮件对象是MIMEMultipart
	    if (msg.is_multipart()):
	    	#get_payload()返回邮件内容里面的所有的子对象，是个list数据
	        parts = msg.get_payload()
	        #enumerate()将列表加上索引变成字典
	        for n, part in enumerate(parts):
	        	#递归打印每一个子对象
	            print('%spart %s' % ('  ' * indent, n))
	            print('%s--------------------' % ('  ' * indent))
	            print_info(part, indent + 1)
        # 如果邮件对象不是一个MIMEMultipart
        # 就根据content_type判断:
	    else:
	        content_type = msg.get_content_type()
	        #纯文本或HTML内容，Ojut邮件为HTML内容，因此这段代码才有效
	        if content_type=='text/plain' or content_type=='text/html':
	            content = msg.get_payload(decode=True)
	            #检测文本编码，并转换成Unicode编码
	            charset = self.guess_charset(msg)
	            if charset:
	                content = content.decode(charset)
	            #打印并返回邮件的文本内容，用于提取验证链接
	            return content
	            print('%sText: %s' % ('  ' * indent, content + '...'))
	        #若不是文本则当做附件处理
	        else:
	            print('%sAttachment: %s' % ('  ' * indent, content_type))

	def getlink(self,email,password):
		# 输入邮件地址, 口令和POP3服务器地址:
		pop3_server = 'pop.163.com'
		# 连接到POP3服务器:例如pop.163.com
		server = poplib.POP3(pop3_server)
		#身份验证,并判断是否开启POP3服务
		try:
			server.user(email)
			server.pass_(password)
			flag = True
		except:
			print "This email has not opened the POP3 service"
			flag = False
			return None
		if flag:
			#list()返回所有邮件的编号
			resp,mails,octets = server.list()#返回一个三元组(返回信息, 邮件列表, 邮件大小)
			#获取最新的邮件，注意索引号从1开始
			index = len(mails)
			resp,lines,octets = server.retr(index)#获取详细的邮件内容三元组(返回信息, 邮件的所以内容, 邮件字节数)
			#lines存储了邮件的原始文本的每一行，是个列表
			#获取整个邮件的原始文本，用回车转行符号连接起来
			msg_content = '\r\n'.join(lines)
			#解析出邮件,得到字典数据
			msg = Parser().parsestr(msg_content)
			#打印邮件内容
			content = self.print_info(msg)
			#关闭连接
			server.quit()
			#用BeautifulSoup模块解析HTML，并提取验证链接
			soup = BeautifulSoup(content,'lxml')
			link = soup.find_all('a')
			return link[0].get_text()
