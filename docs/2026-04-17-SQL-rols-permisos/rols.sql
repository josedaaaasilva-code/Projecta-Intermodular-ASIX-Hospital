CREATE ROLE admin;
CREATE ROLE metge;          
CREATE ROLE infermer;
CREATE ROLE administratiu;
CREATE ROLE personal_vari;


CREATE USER admin_user WITH PASSWORD '1234';
CREATE USER metge_user WITH PASSWORD '1234';
CREATE USER infermer_user WITH PASSWORD '1234';
CREATE USER administratiu_user WITH PASSWORD '1234';

-- Assignar rols
GRANT admin TO admin_user;
GRANT metge TO metge_user;
GRANT infermer TO infermer_user;
GRANT administratiu TO administratiu_user;
