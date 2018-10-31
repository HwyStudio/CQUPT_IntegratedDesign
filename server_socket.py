# -*- coding:utf-8 -*-
from socket import *
from threading import Thread, Lock
import pymysql

# value
sql_insert = "insert into value(target) values(%s)"
# 查询flag表标志位，id
sql_check_id = "select id from flag order by id desc limit 1"
# 查询flag表数据位，target
sql_check_target = "select target from flag order by id desc limit 1"
send_info = ""
# 创建锁
mutex = Lock()


def recvData(client_socket, cursor, mysql_db):
	while True:
		recv_info = client_socket.recv(1024).decode('utf-8')
		print(recv_info)
		print("***************")
		mutex.acquire()
		cursor.execute(sql_insert, [recv_info])
		mysql_db.commit()
		mutex.release()


def sendData(client_socket, cursor, mysql_db):
	data_last = 0
	while True:
		mutex.acquire()
		count = cursor.execute(sql_check_id)
		mysql_db.commit()
		if count == 1:
			data_now = cursor.fetchall()
			if data_last != data_now[0][0]:
				data_last = data_now[0][0]
				cursor.execute(sql_check_target)
				check_target = cursor.fetchall()[0][0]
				print(check_target)
				print("#####################")
				client_socket.sendall(check_target.encode('utf-8'))
		mutex.release()
		
		
def main(cursor, mysql_db):
	# 创建socket
	tcp_ser_socket = socket(AF_INET, SOCK_STREAM)
	tcp_ser_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	# 绑定本地信息
	address = ('', 8889)
	tcp_ser_socket.bind(address)
	# 监听
	tcp_ser_socket.listen(1024)
	# 如果有新的客户端来链接服务器，那么就产生一个新的套接字专门为这个客户端服务器
	while True:
		client_socket, client_address = tcp_ser_socket.accept()
		print("[%s, %s]用户连接上了" % client_address)
		tr = Thread(target=recvData, args=(client_socket, cursor, mysql_db,))
		ts = Thread(target=sendData, args=(client_socket, cursor, mysql_db,))
		tr.start()
		ts.start()
		tr.join()
		ts.join()
	client_socket.close()
	tcpSerSocket.close()


if __name__ == '__main__':
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
	main(cursor, mysql_db)