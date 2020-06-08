import psycopg2
import redis
import json
import os
from bottle import Bottle, request

class Envia(Bottle):
	def __init__(self):
		super().__init__()
		self.route('/', method='POST', callback=self.send)
		
		redis_host = os.getenv('REDIS_HOST', 'fila')
		self.fila = redis.StrictRedis(host=redis_host, port=6379, db=0)
		#self.fila = redis.StrictRedis(host='fila', port=6379, db=0)
		
		db_name = os.getenv('DB_NAME', 'fake')
		db_user = os.getenv('DB_USER', 'postgres')
		db_host = os.getenv('DB_HOST', 'db')
		dsn = f'dbname={db_name} user={db_user} host={db_host}'
		self.connecta = psycopg2.connect(dsn)
		#DSN = 'dbname=solicitacoes user=postgres host=db'
		#self.connecta = psycopg2.connect(DSN)
    
	def registro_pedido(self, nome, assunto, mensagem):
		SQL = 'INSERT INTO pedidos (nome, assunto, mensagem) VALUES (%s, %s, %s)'
		cursosql = self.connecta.cursor()
		cursosql.execute(SQL, (nome, assunto, mensagem))
		self.connecta.commit()
		cursosql.close()
		
		msg = {'nome': nome, 'assunto': assunto, 'mensagem': mensagem}
		self.fila.rpush('envia', json.dumps(msg))   
		
		print('Mensagem registrada!')
		
	#@route('/', method='POST')
	def send (self):
		nome = request.forms.get('nome')
		assunto = request.forms.get('assunto')
		mensagem = request.forms.get('mensagem')
		
		self.registro_pedido(nome, assunto, mensagem)
		return 'Mensagem enviada: Nome: {} Assunto: {} Mensagem: {}'.format(
			nome, assunto, mensagem
		)

if __name__ == '__main__':
	envia = Envia()
	envia.run(host='0.0.0.0', port=8080, debug=True)