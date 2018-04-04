#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import re
import datetime
import time
import math
import inspect
#import traceback

import types
import hashlib
import p4utils

# int = checkVcode(vcode) # 0,1,2,3,4
# vcode = reviseVcode(vin_code):
# int = vin2year(char)
# model = modelCheck(model)

# p4id = pk4yo.generateP4ID(astring)
# Usage:	import p4utils
# p4id = p4utils.generateP4ID('asdf')
# 

# DEBUG layer: 1 - Critical, 2 - Urgent, 3 - Important, 4 - Debug , 5 - Info, 6 - Env, 7 - Trivial, above - no debug
# Only 0, 4 and 10 Used Here !!!
_Z_DEBUG_LEVEL = 0
_Z_DEBUG_CRTITICAL = 1
_Z_DEBUG_URGENT = 2
_Z_DEBUG_IMPORTANT = 3
_Z_DEBUG_DEBUG = 4
def _function_enter(debug = 100):
	if debug <= _Z_DEBUG_LEVEL:
		fname = sys._getframe().f_code.co_filename
		#fcname = sys._getframe().f_code.co_name
		fcname = inspect.stack()[1][3]
		#print str(time.time()) + ' Enter function : ------ ' + fname + '->' + fcname + '-----'
		print '%.6f Enter function : ------ %s->%s-----' % (time.time(), fname, fcname)
	return
def _function_exit(debug = 100):
	if debug <= _Z_DEBUG_LEVEL:
		fname = sys._getframe().f_code.co_filename
		#fcname = sys._getframe().f_code.co_name
		fcname = inspect.stack()[1][3]
		#print str(time.time()) + ' Exit function : ------ ' + fcname + '-----'
		print '%.6f Exit function : ------ %s -----' % (time.time(), fcname)
	return
def _debug(msg,debug = _Z_DEBUG_DEBUG):
	if debug <= _Z_DEBUG_LEVEL:
		print msg
	return

def debug(msg,debug = _Z_DEBUG_DEBUG):
	if debug <= _Z_DEBUG_LEVEL:
		print msg
	return

def getFirstFromVlineString(vline):
	if vline == '':
		return ''
	seg = vline.split('|')
	return seg[0]

def replaceCommaWithQuote(astring):
	astr = astring
	ls = len(astr)
	c1 = astr.find('"')
	while c1 >= 0:
		if c1 == 0:
			astr = astr[1:]
		else:
			astr = astr[:c1] + astr[c1+1:]
		ls -= 1
		c2 = astr.find('"')
		if c2 >= c1:
			astr = astr[:c1] + astr[c1:c2].replace(',','，') + astr[c2+1:]
			c1 = astr.find('"')
		else:
			return astring
	return astr



# URL
regex = re.compile(
		r'^(?:http|ftp)s?://' # http:// or https://
		r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
		r'localhost|' #localhost...
		r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
		r'(?::\d+)?' # optional port
		r'(?:/?|[/?]\S+)$', re.IGNORECASE)

# check a valid date day,  True - correct, False - wrong.
# NOTICE: Only 8 digit is accepted. Eg. 20150905
def isDateDay(astring):
	dayno = astring
	if not dayno.isdigit() or len(dayno) != 8:
		return True
	#闰年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))
	#平年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))
	if(int(dayno) % 4 == 0 or (int(dayno) % 100 == 0 and int(dayno)%4 == 0 )):
		ereg=re.compile('(19[0-9]{2}|20[0-9]{2})[-/]?((01|03|05|07|08|10|12)[-/]?(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)[-/]?(0[1-9]|[1-2][0-9]|30)|02[-/]?(0[1-9]|[1-2][0-9]))$')#//闰年出生日期的合法性正则表达式
	else:
		ereg=re.compile('(19[0-9]{2}|20[0-9]{2})[-/]?((01|03|05|07|08|10|12)[-/]?(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)[-/]?(0[1-9]|[1-2][0-9]|30)|02[-/]?(0[1-9]|1[0-9]|2[0-8]))$')#//平年出生日期的合法性正则表达式
	if(re.match(ereg,dayno)):
		return False
	else:
		return True

def isMobileCn(astring):
	return re.match('^[+]?(86)?(1[3578]\d)|(14[56789])|(166)|(19[89])\d{8}',astring)		# '^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}'

def isTelephoneCn(astring):
	return re.match('^[+]?(86)?[-0]?\d{2,3}[-]?\d{7,8}$|^[+]?(86)?(1[3578]\d)|(14[56789])|(166)|(19[89])\d{8}$',astring)		# '^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}'

def checkTrueName(astring):
	ls = len(astring)
	return 0
	

#
# Function to check id card no.
# Param: id card no. string
# Return: 0 - right, 1 - wrong length, 2 - containing incorrect char, 3 - wrong check digit, 4 - wrong area
#
def checkPassportMRPZ(line1, line2):
	results=['验证通过!','位数不对!','含有非法字符!','校验错误!','地区非法!']
	results=[0,1,2,3,4]
	mrpz1=str(line1).upper().strip()
	mrpz2=str(line2).upper().strip()
	mrpz1_list=list(mrpz1)
	mrpz2_list=list(mrpz2)
	lm1 = len(mrpz1)
	lm2 = len(mrpz2)
 
	if lm1 != 44 or lm2 != 44:
		return results[1]
	else:
		return results[0]

def generateId(username, userid, ts='0'):
	_function_enter(_Z_DEBUG_DEBUG)
	s = str(username) + '' + str(userid) # + '_' + str(ts)
	sid = p4utils.generateP4ID(s)
	_debug(username + ',' + userid + ' ==> ' + sid)
	_function_exit(_Z_DEBUG_DEBUG)
	return sid
		
#
# Function to check the TYPE of a string.
# Param: code string
# Return: 0 - Unknown, 1 - email,  2 - Birthday, 3 - Mobile, 4 - CN ID Card No., 5 - ;
#		 0 - Unknown, 1 - email,  2 - Birthday, 3 - Mobile, 4 - CN ID Card No., 5 - ;
#
def getStringType(astring):
	_function_enter(_Z_DEBUG_DEBUG)
	ss = astring
	if re.match("[-_\w\.]{0,64}@([-\w]{1,63}\.)*[-\w]{1,63}",ss) != None:		# '[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$'  
		_function_exit(_Z_DEBUG_DEBUG)
		return 1
	elif ss.isdigit():
		sl = len(ss)
		if sl == 11 and re.match('1[3-57-9]\d{9}',ss) != None:
			return 3
	return 0

#	if re.match('[A-Z]{2}[A-Z]?[1345][0-9]{3}[A-Z]+',mdl) == None:
#		return 4



'''
import 其他程序
'''


#
# Function to check id card no.
# Param: id card no. string
# Return: 0 - right, 1 - wrong length, 2 - containing incorrect char, 3 - wrong check digit, 4 - wrong area
#

#results=['验证通过!','身份证号码位数不对!','身份证号码出生日期超出范围或含有非法字符!','身份证号码校验错误!','身份证地区非法!']
def checkIdCardCn(idcard):
	results=['验证通过!','身份证号码位数不对!','身份证号码出生日期超出范围或含有非法字符!','身份证号码校验错误!','身份证地区非法!']
	results=[0,1,2,3,4]
	area={"11":"北京","12":"天津","13":"河北","14":"山西","15":"内蒙古","21":"辽宁","22":"吉林","23":"黑龙江","31":"上海","32":"江苏","33":"浙江","34":"安徽","35":"福建","36":"江西","37":"山东","41":"河南","42":"湖北","43":"湖南","44":"广东","45":"广西","46":"海南","50":"重庆","51":"四川","52":"贵州","53":"云南","54":"西藏","61":"陕西","62":"甘肃","63":"青海","64":"宁夏","65":"新疆","71":"台湾","81":"香港","82":"澳门","91":"国外"}
	idcard=str(idcard).upper()
	idcard=idcard.strip()
	idcard_list=list(idcard)
 
	#地区校验
	if idcard[0:2] not in area:
		return results[4]
	#15位身份号码检测
	if(len(idcard)==15):
		if not idcard.isdigit() :
			return results[2]
		if((int(idcard[6:8])+1900) % 4 == 0 or((int(idcard[6:8])+1900) % 100 == 0 and (int(idcard[6:8])+1900) % 4 == 0 )):
			ereg=re.compile('[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}$')#//测试出生日期的合法性
		else:
			ereg=re.compile('[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}$')#//测试出生日期的合法性
		if(re.match(ereg,idcard)):
			return results[0]
		else:
			return results[2]
	#18位身份号码检测
	elif(len(idcard)==18):
		if not (idcard.isdigit() or (idcard[-1] == 'X' and idcard[:-1].isdigit())):
			return results[2]
		#出生日期的合法性检查
		#闰年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))
		#平年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))
		if(int(idcard[6:10]) % 4 == 0 or (int(idcard[6:10]) % 100 == 0 and int(idcard[6:10])%4 == 0 )):
			ereg=re.compile('[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}[0-9Xx]$')#//闰年出生日期的合法性正则表达式
		else:
			ereg=re.compile('[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}[0-9Xx]$')#//平年出生日期的合法性正则表达式
		#//测试出生日期的合法性
		if(re.match(ereg,idcard)):
			#//计算校验位
			S = (int(idcard_list[0]) + int(idcard_list[10])) * 7 + (int(idcard_list[1]) + int(idcard_list[11])) * 9 + (int(idcard_list[2]) + int(idcard_list[12])) * 10 + (int(idcard_list[3]) + int(idcard_list[13])) * 5 + (int(idcard_list[4]) + int(idcard_list[14])) * 8 + (int(idcard_list[5]) + int(idcard_list[15])) * 4 + (int(idcard_list[6]) + int(idcard_list[16])) * 2 + int(idcard_list[7]) * 1 + int(idcard_list[8]) * 6 + int(idcard_list[9]) * 3
			Y = S % 11
			M = "F"
			JYM = "10X98765432"
			M = JYM[Y]#判断校验位
			if(M == idcard_list[17]):#检测ID的校验位
				return results[0]
			else:
				return results[3]
		else:
			return results[2]
	else:
		return results[1]
'''
# unused
def getdistrictcode():
  with open('districtcode') as file:
	data = file.read()
  districtlist = data.split('\n')
  global codelist
  codelist = []
  for node in districtlist:
	#print node
	if node[10:11] != ' ':
	  state = node[10:].strip()
	if node[10:11]==' 'and node[12:13]!=' ':
	  city = node[12:].strip()
	if node[10:11] == ' 'and node[12:13]==' ':
	  district = node[14:].strip()
	  code = node[0:6]
	codelist.append({"state":state,"city":city,"district":district,"code":code})

# unused
def generateIdCardCn():
	id = codelist[random.randint(0,len(codelist))]['code'] #地区项
	id = id + str(random.randint(1930,2013)) #年份项
	da = date.today()+timedelta(days=random.randint(1,366)) #月份和日期项
	id = id + da.strftime('%m%d')
	id = id+ str(random.randint(100,300))#，顺序号简单处理
 
	i = 0
	count = 0
	weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2] #权重项
	checkcode ={'0':'1','1':'0','2':'X','3':'9','4':'8','5':'7','6':'6','7':'5','8':'5','9':'3','10':'2'} #校验码映射
	for i in range(0,len(id)):
		count = count +int(id[i])*weight[i]
	id = id + checkcode[str(count%11)] #算出校验码
	return id
'''

"""
验证所有表单提交的数据
"""

#判断是否为整数 15
def isNumber(varObj):
	return type(varObj) is types.IntType

#判断是否为字符串 string
def isString(varObj):
	return type(varObj) is types.StringType

#判断是否为浮点数 1.324
def isFloat(varObj):
	return type(varObj) is types.FloatType

#判断是否为字典 {'a1':'1','a2':'2'}
def isDict(varObj):
	return type(varObj) is types.DictType

#判断是否为tuple [1,2,3]
def isTuple(varObj):
	return type(varObj) is types.TupleType

#判断是否为List [1,3,4]
def isList(varObj):
	return type(varObj) is types.ListType

#判断是否为布尔值 True
def isBoolean(varObj):
	return type(varObj) is types.BooleanType

#判断是否为货币型 1.32
def isCurrency(varObj):
	#数字是否为整数或浮点数
	if isFloat(varObj) and isNumber(varObj):
		#数字不能为负数
		if varObj >0:
			return isNumber(varObj)
		else:
			return False
	return True

#判断某个变量是否为空 x
def isEmpty(varObj):
	if len(varObj) == 0:
		return True
	return False

#判断变量是否为None None
def isNone(varObj):
	return type(varObj) is types.NoneType# == "None" or varObj == "none":

#判断是否为日期格式,并且是否符合日历规则 2010-01-31
def isDate(varObj):
	if len(varObj) == 10:
		rule = '(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)$/'
		match = re.match( rule , varObj )
		if match:
			return True
		return False
	return False

#判断是否为邮件地址
def isEmail(varObj):
	rule = '[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$'
	match = re.match( rule , varObj )

	if match:
		return True
	return False

#判断是否为中文字符串
def isChineseCharString(varObj):
	for x in varObj:
		if (x >= u"\u4e00" and x<=u"\u9fa5") or (x >= u'\u0041' and x<=u'\u005a') or (x >= u'\u0061' and x<=u'\u007a'):
			continue
		else:
			return False
	return True


#判断是否为中文字符
def isChineseChar(varObj):
	if varObj[0] > chr(127):
		return True
	return False

#判断帐号是否合法 字母开头，允许4-16字节，允许字母数字下划线
def isLegalAccounts(varObj):
	rule = '[a-zA-Z][a-zA-Z0-9_]{3,15}$'
	match = re.match( rule , varObj )

	if match:
		return True
	return False

#匹配IP地址
def isIpAddr(varObj):
	rule = '\d+\.\d+\.\d+\.\d+'
	match = re.match( rule , varObj )

	if match:
		return True
	return False

'''
if __name__=='__main__':
	print 'isDate:',isDate('2010-01-31')
	print 'isNone:',isNone(None)
	print 'isEmpty:',isEmpty('1')
	print 'isCurrency:',isCurrency(1.32)
	print 'isList:',isList([1,3,4])
	print 'isTuple:',isTuple([1,3,4])
	print 'isDict:',isDict({'a1':'1','a2':'2'})
	print 'isFloat:',isFloat(1.2)
	print 'isString:',isString('string')
	print 'isNumber:',isNumber(15)
	print 'isEmail:',isEmail('sgicer@163.com')
	print 'isChineseChar:',isChineseChar(u'啊')
	print 'isChineseCharString:',isChineseCharString(u'啊倒萨')
	print 'isLegalAccounts:',isLegalAccounts('alan_z')
	print 'isIpAddr:',isIpAddr('127.1110.0.1')
	pass
'''
