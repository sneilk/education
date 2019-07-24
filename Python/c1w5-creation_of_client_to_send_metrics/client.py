import socket

class ClientError(Exception):
	pass

class Client:
	def __init__(self, addres, port, timeout):
		self.addres = addres
		self.port = port
		self.timeout = timeout
		self.metrics = {}

	def send(self, data_to_sever):
		with socket.create_connection((self.addres, self.port), self.timeout) as sock:
			sock.sendall(data_to_sever.encode("utf8"))
			data_from_server = sock.recv(1024)
		return data_from_server.decode("utf8")

	def put(self, metric, val, timestamp=None):
		ans_from_server = self.send('put ' + str(metric) + ' ' + str(val) 
			+ ' ' + str(int(timestamp) if timestamp else int(time.time())) + '\n')
		if ans_from_server != 'ok\n\n':
			raise ClientError(ans_from_server)

	def get(self, metric):
		ans_from_server = self.send('get ' + str(metric) + "\n")
		if ans_from_server[:3] != 'ok\n':
			raise ClientError(ans_from_server)
		fin_answer = dict()
		server_ans_splitted = ans_from_server.split('\n')
		for i in server_ans_splitted[1:-2]:
			key = i.split(" ")[0]
			data = (int(i.split(" ")[2]), float(i.split(" ")[1]))
			if key not in fin_answer:
				fin_answer[key] = list()
			fin_answer[key].append(data)
			fin_answer[key].sort(key=lambda x: x[0])
		return fin_answer