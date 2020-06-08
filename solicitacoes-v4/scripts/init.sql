CREATE DATABASE solicitacoes;
\c solicitacoes

CREATE TABLE pedidos (
	id serial not NULL,
	data TIMESTAMP not null DEFAULT CURRENT_TIMESTAMP,
	nome VARCHAR(100) not NULL,
	assunto VARCHAR(100) not NULL,
	mensagem VARCHAR(250) not NULL
);