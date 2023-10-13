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