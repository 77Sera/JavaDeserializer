#coding:utf8

from funcs import *

'''
java 反序列化工具
每个函数都是独立的，只要传入一个十六进制序列化数组
'''

#获取序列化版本信息，即magic number，返回s-e位置
def getMagicNumber(hex_arr,debug=False):
	start = 0
	end = 4
	info_arr = hex_arr[start:end]
	
	if debug is True:
		print('magic_number=>',' '.join(info_arr))
	return start,end

#获取序列化类名，返回从长度到类名截至的start-end位置
def getClassName(hex_arr,debug=False):
	start = -1
	end = -1
	for i in range(len(hex_arr)):
		if hex_arr[i] == '73': #匹配到73新建对象标志头
			if hex_arr[i+1] == '72': #匹配到72新建类标志头
				start = i+2 #确定长度起始位置
				break
	if start != -1:
		class_name_length = hex2num([hex_arr[start],hex_arr[start+1]])
		end = start+2+class_name_length
		class_name = hex2ascii(hex_arr[start+2:end])
		
		if debug is True:
			print('class_name=>',class_name)
	return start,end
	
#获取序列化ID
def getSerialVersionUID(hex_arr,debug=False):
	start,end = getClassName(hex_arr)
	start = end
	
	#找到序列化ID终止位置
	for i in range(len(hex_arr)):
		#判断标志位
		#01表示实现了serializable接口，并且自定义了writeObject()
		#02表示实现了serializable接口
		#04表示实现externalizable接口，
		#08表示XXX，没明白英文
		#10表示该类是个Enum类
		if hex_arr[i] == '01' or hex_arr[i] == '02' or hex_arr[i] == '04' or hex_arr[i] == '08' or hex_arr[i] == '10':
			if hex_arr[i+1] == '00':
				end = i
				break
	
	if debug is True:
		print('SerialVersionUID=>',''.join(hex_arr[start:end]))
	return start,end
	
#获取各个变量名和各个变量值
def getVar(hex_arr,debug=False):
	start,end = getSerialVersionUID(hex_arr) #end的位置是标志位的位置
	
	fields_num = hex2num([hex_arr[end+1],hex_arr[end+2]])
	field_name_arr = []
	field_value_arr = []
	
	start = end+3
	end = -1

	count = 0 #变量计数器
	
	temp_start = start #每轮循环判断一个对应变量
	while True:
		field_type = hex_arr[temp_start]
		
		if  count == fields_num:
			end = temp_start
			break
		elif field_type in ['42','43','44','46','49','4a','4c','53','5a']:
			count+=1
			
			field_name_length = hex2num([hex_arr[temp_start+1],hex_arr[temp_start+2]])
			field_name = hex2ascii(hex_arr[temp_start+3:temp_start+3+field_name_length])
			temp_start = temp_start+3+field_name_length
			
			field_name_arr.append(field_name)
		elif field_type == '71': #这是表示前面已经声明过某类型
			temp_start = temp_start+5 # 通常字符串 71 00 7e 00 01 5个字节
		elif field_type == '74': #该值表示字符串对象，但声明的不是值，而是java/lang/string;
			field_name_length = hex2num([hex_arr[temp_start+1],hex_arr[temp_start+2]])
			temp_start = temp_start+3+field_name_length
		elif count > 100:
			print('[!] Serial Object Error!')
			break
			
	# 接下来开始获取变量值
	for i in range(len(hex_arr)):
		if hex_arr[i] == '78': #获取到块结束标志78 TC_ENDBLOCK
			if hex_arr[i+1] == '70': #获取到无父类标志70 TC_NULL
				temp_start = i+2
				break
	
	count = 0
	while True:
		if temp_start == len(hex_arr):
			break
	
		field_type = hex_arr[temp_start]
		if count == fields_num:
			break
		elif field_type in ['74']: #特殊对象目前只碰到过74，74表示对象（字符串）
			count+=1
			field_length = hex2num([hex_arr[temp_start+1],hex_arr[temp_start+2]])
			field_value = hex2ascii(hex_arr[temp_start+3:temp_start+3+field_length])
			temp_start = temp_start+field_length+3
			
			field_value_arr.append(field_value)
		else:
			count+=1
			field_length = 4
			field_value = hex2num(hex_arr[temp_start:temp_start+4])
			temp_start = temp_start+4
			field_value_arr.append(field_value)
	if debug is True:
		for i in range(fields_num):
			print(field_name_arr[i],'=>',field_value_arr[i])
	return start,end
	
if __name__ == '__main__':
	file_path = input('file_path=>')
	hex_arr = file2hex(file_path)
	
	getMagicNumber(hex_arr,True) #获取序列化magic number
	getClassName(hex_arr,True) #获取序列化类名
	getSerialVersionUID(hex_arr,True) #获取序列化版本ID
	getVar(hex_arr,True) #获取序列化变量(key-value)