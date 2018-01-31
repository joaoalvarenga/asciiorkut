create database orkut;
use orkut;

create table `atores` (
	`codigo` int(10) not null AUTO_INCREMENT,
	primary key (`codigo`)
);

create table `publicaveis` (
	`codigo` int(10) not null AUTO_INCREMENT,
	primary key (`codigo`)
);

create table `interativos` (
	`codigo` int(10) not null AUTO_INCREMENT,
	primary key (`codigo`)
);

CREATE TABLE `usuarios` (
	`codigo` int(11) NOT NULL AUTO_INCREMENT,
	`email` varchar(50) NOT NULL,
	`nome` varchar(100) NOT NULL,
	`dataNascimento` date NOT NULL,
	`sexo` char(1) NOT NULL,
	`senha` varchar(10) NOT NULL,
	`codigo_ator` int(10) NOT NULL,
	`codigo_publicavel` int(10) NOT NULL,
	PRIMARY KEY (`codigo`),
	FOREIGN KEY (`codigo_ator`) REFERENCES `atores`(`codigo`) ON DELETE CASCADE,
	FOREIGN KEY (`codigo_publicavel`) REFERENCES `publicaveis`(`codigo`) ON DELETE CASCADE
);

CREATE TABLE `paginas` (
	`codigo` int(10) NOT NULL AUTO_INCREMENT,
	`codigo_ator` int(10) NOT NULL,
	`nome` varchar(50) NOT NULL,
	`data_criacao` date NOT NULL,
	PRIMARY KEY (`codigo`),
	FOREIGN KEY (`codigo_ator`) REFERENCES `atores`(`codigo`) ON DELETE CASCADE
);

create table `grupos` (
	`codigo` int(10) not null AUTO_INCREMENT,
	`nome` varchar(50) not null,
	`data_criacao` date not null,
	`criado_por` int(10) not null,
	primary key(`codigo`),
	FOREIGN KEY (`criado_por`) REFERENCES `usuarios`(`codigo`) ON DELETE RESTRICT
);

create table `grupos_publicacoes` (
	`codigo_grupo` int(10) not null,
	`codigo_publicavel` int(10) not null,
	primary key (`codigo_grupo`, `codigo_publicavel`),
	FOREIGN KEY (`codigo_grupo`) REFERENCES `grupos`(`codigo`) ON DELETE CASCADE,
	FOREIGN KEY (`codigo_publicavel`) REFERENCES `publicaveis`(`codigo`) ON DELETE CASCADE
);

create table `grupos_mensagem` (
	`codigo` int(10) not null,
	primary key (`codigo`),
	FOREIGN KEY (`codigo`) REFERENCES `grupos`(`codigo`) ON DELETE CASCADE
);

create table `eventos` (
	`codigo` int(10) not null AUTO_INCREMENT,
	`nome` varchar(100) not null,
	`data` date not null,
	`local` varchar(100) not null,
	`codigo_publicavel` int(10) not null,
	`criado_por` int(10) not null,
	`data_criacao` date not null,
	primary key (`codigo`),
	FOREIGN KEY (`codigo_publicavel`) REFERENCES `publicaveis`(`codigo`) ON DELETE CASCADE,
	FOREIGN KEY (`criado_por`) REFERENCES `usuarios`(`codigo`) ON DELETE RESTRICT
);

create table `publicacoes` (
	`codigo` int(10) not null AUTO_INCREMENT,
	`data_publicacao` date not null,
	`conteudo` varchar(100) not null,
	`codigo_ator` int(10) not null,
	`codigo_aublicavel` int(10) not null,
	`codigo_interativo` int(10) not null,
	`codigo_pertence` int(10) not null,
	primary key(`codigo`),
	FOREIGN KEY (`codigo_publicavel`) REFERENCES `publicaveis`(`codigo`) ON DELETE CASCADE,
	FOREIGN KEY (`codigo_interativo`) REFERENCES `interativos`(`codigo`) ON DELETE CASCADE,
	FOREIGN KEY (`codigo_pertence`) REFERENCES `publicacoes`(`codigo`) ON DELETE CASCADE
);

create table `historias` (
	`codigo` int(10) not null AUTO_INCREMENT,
	`data_criacao` date not null,
	`conteudo` varchar(100) not null,
	`duracao` int(10) not null,
	`codigo_ator` int(10) not null,
	`codigo_interativo` int(10) not null,
	primary key(`codigo`),
	FOREIGN KEY (`codigo_ator`) REFERENCES `atores`(`codigo`) ON DELETE CASCADE,
	FOREIGN KEY (`codigo_interativo`) REFERENCES `interativos`(`codigo`) ON DELETE CASCADE
);

create table `interacoes` (
	`codigo_ator` int(10) not null,
	`codigo_interativo` int(10) not null,
	`data` date not null,
	primary key(`codigo_ator`, `codigo_interativo`),
	FOREIGN KEY (`codigo_interativo`) REFERENCES `interativos`(`codigo`) ON DELETE CASCADE,
	FOREIGN KEY (`codigo_ator`) REFERENCES `atores`(`codigo`) ON DELETE CASCADE
);

CREATE TABLE `sao_amigos` (
	`codigo_usuario_1` int(10) NOT NULL,
	`codigo_usuario_2` int(10) NOT NULL,
	PRIMARY KEY (`codigo_usuario_1`, `codigo_usuario_2`),
	FOREIGN KEY (`codigo_usuario_1`) REFERENCES `usuarios`(`codigo`) ON DELETE CASCADE,
	FOREIGN KEY (`codigo_usuario_2`) REFERENCES `usuarios`(`codigo`) ON DELETE CASCADE
);

CREATE TABLE `mensagens_privadas` (
	`codigo` int(10) NOT NULL AUTO_INCREMENT,
	`conteudo` varchar(100) NOT NULL,
	`data` date NOT NULL,
	`de` int(10) NOT NULL,
	`para` int(10) NOT NULL,
	PRIMARY KEY (`codigo`),
	FOREIGN KEY (`de`) REFERENCES `usuarios`(`codigo`) ON DELETE CASCADE,
	FOREIGN KEY (`para`) REFERENCES `usuarios`(`codigo`) ON DELETE CASCADE
);

CREATE TABLE `participam_eventos` (
	`codigo_usuario` int(10) NOT NULL,
	`codigo_evento` int(10) NOT NULL,
	`tipo` varchar(10) NOT NULL,
	PRIMARY KEY (`codigo_usuario`, `codigo_evento`),
	FOREIGN KEY (`codigo_usuario`) REFERENCES `usuarios`(`codigo`) ON DELETE CASCADE,
	FOREIGN KEY (`codigo_evento`) REFERENCES `eventos`(`codigo`) ON DELETE CASCADE
);

CREATE TABLE `seguem_paginas` (
	`codigo_usuario` int(10) NOT NULL,
	`codigo_pagina` int(10) NOT NULL,
	PRIMARY KEY (`codigo_usuario`, `codigo_pagina`),
	FOREIGN KEY (`codigo_usuario`) REFERENCES `usuarios`(`codigo`) ON DELETE CASCADE,
	FOREIGN KEY (`codigo_pagina`) REFERENCES `paginas`(`codigo`) ON DELETE CASCADE
);

CREATE TABLE `pertencem_grupos` (
	`codigo_usuario` int(10) NOT NULL,
	`codigo_grupo` int(10) NOT NULL,
	`tipo` varchar(10),
	`data` date NOT NULL,
	PRIMARY KEY (`codigo_usuario`, `codigo_grupo`),
	FOREIGN KEY (`codigo_usuario`) REFERENCES `usuarios`(`codigo`) ON DELETE CASCADE,
	FOREIGN KEY (`codigo_grupo`) REFERENCES `grupos`(`codigo`) ON DELETE CASCADE
);

create table `administram_paginas` (
	`codigo_usuario` int(10) not null,
	`codigo_pagina` int(10) not null,
	primary key (`codigo_usuario`, `codigo_pagina`),
	FOREIGN KEY (`codigo_usuario`) REFERENCES `usuarios`(`codigo`) ON DELETE CASCADE,
	FOREIGN KEY (`codigo_pagina`) REFERENCES `paginas`(`codigo`) ON DELETE CASCADE
);

create table `mensagens_grupos` (
	`codigo` int(10) not null AUTO_INCREMENT,
	`data` date not null,
	`conteudo` varchar(100) not null,
	`codigo_grupo` int(10) not null,
	`codigo_usuario` int(10) not null,
	primary key(`codigo`),
	FOREIGN KEY (`codigo_grupo`) REFERENCES `grupos`(`codigo`) ON DELETE CASCADE,
	FOREIGN KEY (`codigo_usuario`) REFERENCES `usuarios`(`codigo`) ON DELETE CASCADE
);


