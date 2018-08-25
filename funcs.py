#coding:utf8

# 将byte字节转成16进制格式 如：\x09
def byte2hex(byt):
	str_byt = str(byt).replace('b','').replace('\'','')
	if str_byt.find('\\x') == -1: #本身为16进制，无需转换
		str_byt = hex(ord(byt)).replace('0x','\\x')
	return str_byt

#二进制文件转16进制数组 如 ['ac','ed','00','05'......]
def file2hex(file_path):
	result = ''
	with open(file_path,'rb') as file:
		while True:
			byt = file.read(1)
			if len(byt) > 0:
				result+=byte2hex(byt)
			else:
				break
	return result.strip('\\x').split('\\x')
	
#十六进制数据转十进制
#输入十六进制字符串，输出十进制int，如"0004" 输入 4
def hex2num(arr):
	temp = ''
	for i in arr:
		temp+=i
	arr = temp
	length = len(arr)
	num = 0
	for i in range(length):
		single_num = arr[i]
		if single_num == 'a' or single_num == 'A':
			single_num = 10
		elif single_num == 'b' or single_num == 'B':
			single_num = 11
		elif single_num == 'c' or single_num == 'C':
			single_num = 12
		elif single_num == 'd' or single_num == 'D':
			single_num = 13
		elif single_num == 'e' or single_num == 'E':
			single_num = 14
		elif single_num == 'f' or single_num == 'F':
			single_num = 15
		else:
			single_num = int(single_num)
		for x in range(length-i-1):
			single_num*=16
		num+=single_num
	return num

#十六进制转ascii字符，输入十六进制字符数组，输出ascii字符串
def hex2ascii(arr):
	result = ''
	for i in arr:
		result+=chr(hex2num([i]))
	return result
if __name__ == '__main__':
	hex_arr = file2hex('data1')
	print(len(hex_arr))