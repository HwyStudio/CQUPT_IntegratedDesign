# -*- coding:utf-8 -*-
import itchat
import pymysql
from itchat.content import TEXT

# 向flag表增加
sql_insert = "insert into flag(target) values(%s)"
# 查询value表标志位，id
sql_check_id = "select id from value order by id desc limit 1"
# 查询value表数据位，target
sql_check_target = "select target from value order by id desc limit 1"
# flag
sql_truncate_flag = "truncate flag"
# 清空value表
sql_truncate_value = "truncate value"


def check():
	global data_last
	while True:
		count = cursor.execute(sql_check_id)
		mysql_db.commit()
		if count == 1:
			data_now = cursor.fetchall()
			if data_last != data_now[0][0]:
				data_last = data_now[0][0]
				cursor.execute(sql_check_target)
				return cursor.fetchall()[0][0]


@itchat.msg_register([TEXT])
def simple_reply(msg):
	print(msg['Content'])
	if msg['Content'] == "温度":
		cursor.execute(sql_insert, "getTemperature")
		mysql_db.commit()
		data = check()
		print(data)
		print("*************")
		# itchat.send("温度是: %s ℃" % data, msg['FromUserName'])
		itchat.send("温度是: %s ℃" % data,toUserName = 'filehelper')
	elif msg['Content'] == "湿度":
		cursor.execute(sql_insert, "getHumidity")
		mysql_db.commit()
		data = check()
		print(data)
		print("#############")
		# itchat.send("湿度是: %s" % data, msg['FromUserName'])
		itchat.send("湿度是:" + data + "%", toUserName='filehelper')


# 创建连接通道, 设置连接ip, port, 用户, 密码以及所要连接的数据库
mysql_db = pymysql.connect(
	host='localhost',
	port=3306,
	user='root',
	passwd='XJY19961113',
	db='check_design'
)
# 创建游标, 操作数据库, 指定游标返回内容为字典类型
cursor = mysql_db.cursor()
# 清空flag表
cursor.execute(sql_truncate_flag)
mysql_db.commit()
# 清空value表
cursor.execute(sql_truncate_value)
mysql_db.commit()
data_last = 0
# 微信登录
itchat.auto_login(hotReload=True)
itchat.run()