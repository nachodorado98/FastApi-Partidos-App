CREATE DATABASE bbdd_partidos;

\c bbdd_partidos;

CREATE TABLE partidos (id SERIAL PRIMARY KEY,
						fecha DATE,
						hora VARCHAR(10),
						competicion VARCHAR(50),
						ronda VARCHAR(50),
						lugar VARCHAR(50),
						rival VARCHAR(50),
						marcador VARCHAR(50),
						resultado VARCHAR(50),
						posesion INT,
						publico INT,
						capitan VARCHAR(50),
						arbitro VARCHAR(50));

CREATE TABLE usuarios (usuario VARCHAR(20) PRIMARY KEY,
						nombre VARCHAR(20),
						contrasena VARCHAR(70),
						numero_partidos INT DEFAULT 0);

CREATE TABLE asistidos (asistido VARCHAR(32) PRIMARY KEY,
						id INT,
						usuario VARCHAR(20),
						comentarios VARCHAR(100),
						FOREIGN KEY (id) REFERENCES partidos(id) ON DELETE CASCADE,
						FOREIGN KEY (usuario) REFERENCES usuarios(usuario) ON DELETE CASCADE);