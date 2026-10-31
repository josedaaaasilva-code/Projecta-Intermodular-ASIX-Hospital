
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;


-- metge
-- Consultar informació
GRANT SELECT ON pacient, visita, operacio, medicament, medicament_receptat,
infermeria, habitacio, reserva_habitacio, quirofan, aparell_medic,
aparell_en_quirofan, personal TO metge;

-- Crear visites, operacions i medicació receptada
GRANT INSERT ON visita, operacio, medicament_receptat TO metge;

-- Actualitzar diagnòstic de les seves visites
GRANT UPDATE (diagnostic) ON visita TO metge;



--INFERMER
GRANT SELECT ON pacient, visita, operacio, infermeria, metge, personal
TO infermer;


-- ADMINISTRATIU
-- Consultar informació general
GRANT SELECT ON pacient, visita, reserva_habitacio, habitacio, quirofan,
aparell_medic, aparell_en_quirofan, planta, personal, metge, infermeria
TO administratiu;
-- Crear i modificar pacients, visites i reserves
GRANT INSERT, UPDATE ON pacient TO administratiu;
GRANT INSERT, UPDATE ON visita TO administratiu;
GRANT INSERT, UPDATE ON reserva_habitacio TO administratiu;



--admin
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin;


--permisos automatics futurs
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT, INSERT, UPDATE ON TABLES TO metge;
