# Eines tecnològiques del projecte

## Base de dades: PostgreSQL 16
Triem PostgreSQL perquè:
- És lliure i gratuït.
- Suporta Unicode complet (UTF‑8), necessari per noms en alfabet ciríl·lic.
- Inclou eines natives de seguretat: data masking, rols, permisos i connexions SSL.
- Permet replicació síncrona i asíncrona per alta disponibilitat.
- pgAdmin 4 facilita la gestió gràfica de l’esquema i la monitorització.

## Llenguatge de programació: Python
Python és ideal per l’hospital perquè:
- És multiplataforma i funciona en equips de baix consum.
- Té llibreries per totes les funcionalitats del projecte:
  - `psycopg2` → connexió segura a PostgreSQL.
  - `faker` → generació de dades fictícies realistes (incloent ciríl·lic).
  - `xml.etree.ElementTree` → exportació XML.
  - `json` → exportació JSON.
  - `bcrypt` → hash de contrasenyes.
  - `requests` → connexió amb l’API remota de la Seguretat Social.

## Estructura del projecte
L’aplicació seguirà una estructura modular:

- `/src` → codi font principal  
- `/src/login` → validació, hash i control d’accés  
- `/src/manteniment` → CRUD de pacients, metges, personal i visites  
- `/src/consultes` → informes i consultes avançades  
- `/src/exportacions` → XML, JSON i integració amb API  
- `/src/utils` → funcions auxiliars i connexió BD  
- `/config` → paràmetres, SSL i variables d’entorn  
- `/scripts` → backups, restauració i generació de dummy data  
- `/docs` → documentació oficial del projecte

## Estratègia de desplegament
- **Opció principal:** Ubuntu Server + PostgreSQL + aplicació Python.
- **Opció alternativa:** Docker amb contenidors separats (BD + aplicació).
- Pensat per equips amb pocs recursos i instal·lació senzilla.

## Seguretat
- Connexions SSL.
- Data masking amb pgcrypto.
- Rols i permisos restrictius.
- Hash de contrasenyes amb bcrypt.

## Alta disponibilitat
- PostgreSQL en esquema actiu-actiu.
- Gestió de failover amb pgpool-II o Patroni.

## Dummy Data
- Generació massiva amb `faker`.
- Dades en ciríl·lic.
- Índexs per optimitzar consultes amb grans volums.

## Exportacions XML/JSON
- XML amb ElementTree.
- JSON per ús intern.
- Enviament a API remota via HTTPS amb `requests`.

## Dashboard Power BI
- Connexió directa a PostgreSQL.
- Quadre de comandament amb visites, metges i activitat diària.

## Metodologia
- **SCRUM** amb entregues incrementals.
- Gestió de tasques amb **JIRA**.
