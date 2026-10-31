CREATE TABLE roles (
    id_rol SERIAL PRIMARY KEY,
    nom_rol VARCHAR(30) UNIQUE NOT NULL
);

INSERT INTO roles (nom_rol) VALUES
('admin'),
('metge'),
('infermeria'),
('administracio');

CREATE TABLE usuaris (
    id_usuari SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    id_rol INT REFERENCES roles(id_rol),
    intents_fallits INT DEFAULT 0,
    bloquejat BOOLEAN DEFAULT FALSE,
    actiu BOOLEAN DEFAULT TRUE
);

-- Assegurar que dni a PERSONAL és únic
ALTER TABLE PERSONAL ADD UNIQUE (dni);

-- Afegir columna dni a USUARI com a FK
ALTER TABLE USUARI 
ADD COLUMN dni VARCHAR(12),
ADD FOREIGN KEY (dni) REFERENCES PERSONAL(dni) ON DELETE SET NULL;

CREATE TABLE logs_accessos (
    id_log SERIAL PRIMARY KEY,
    username VARCHAR(50),
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resultat VARCHAR(30)
);

CREATE TABLE horari_metge (
    id_horari    SERIAL PRIMARY KEY,
    id_metge     INTEGER NOT NULL,
    dia_setmana  VARCHAR(20) NOT NULL,
    hora_inici   TIME NOT NULL,
    hora_fi      TIME NOT NULL,

    FOREIGN KEY (id_metge) REFERENCES personal(id_personal)
);



#rols: guarda tipus d'usuari
#usuaris: usuaris reals
#logs_accessos: registre d'accesos
