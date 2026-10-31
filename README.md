# Hospital Harmonia de Blanes

Sistema de gestió hospitalària per a un hospital comarcal, desenvolupat com a **projecte intermodular del CFGS d'Administració de Sistemes Informàtics en Xarxa (ASIX)**.

L'aplicació és una eina d'escriptori feta amb **Python** (Tkinter) connectada a **PostgreSQL 16**. Permet iniciar sessió amb rols, mantenir pacients, personal, visites, habitacions i quiròfans, explotar la informació amb consultes i informes, i exportar les visites a **XML** i **JSON** per integrar-les amb la Seguretat Social.

> Projecte acadèmic del curs 2025—2027. Les dades que genera el mode *dummy* són fictícies.

## Funcionalitats

| Mòdul | Què fa |
|---|---|
| **Accés i seguretat** | Login en Tkinter, contrasenyes xifrades amb **bcrypt**, quatre rols (admin, metge, infermer, administratiu) i connexió a la base de dades amb un usuari de PostgreSQL diferent per a cada rol. Registre d'accessos. |
| **Manteniment** | Altes i consultes de pacients i personal, assignació d'infermeria als metges, dades d'habitacions i quiròfans, aparells mèdics i visites per dia. |
| **Consultes i informes** | Visites per planta, rànquing de metges, informes de personal i estadístiques de malalties. |
| **Exportacions** | Exportació de visites a **JSON** i **XML** amb esquema propi (`schema_visites.json` i `schema_visites.xsd`) i historial de cada exportació. |
| **Dades de prova** | Generador massiu de dades amb **Faker** (inclou alfabet ciríl·lic), esborrat de dades i recreació d'índexs. |
| **Documentació** | Model ER, model relacional, DDL, rols i permisos, protecció de dades (AGPD), alta disponibilitat i manuals d'instal·lació i d'usuari. |

## Tecnologies

| Capa | Tecnologia |
|---|---|
| Llenguatge | Python 3.13 |
| Interfície | Tkinter |
| Base de dades | PostgreSQL 16 (pgAdmin 4) |
| Accés a dades | `psycopg2` |
| Seguretat | `bcrypt` + rols i permisos de PostgreSQL |
| Dades de prova | `faker` |
| Intercanvi de dades | `json`, `xml.etree.ElementTree` |
| Analítica | Power BI (`docs/dashboard_harmonia.pbix`) |
| Desplegament | Ubuntu Server o Docker (vegeu la documentació d'alta disponibilitat) |

## Estructura del repositori

```
.
├── config/
│   └── config.ini              # paràmetres d'entorn (no es versiona la configuració real)
├── docs/                       # documentació oficial del projecte, per entregues
│   ├── 2026-04-08-planificació/
│   ├── 2026-04-11-model-relacional/
│   ├── 2026-04-12-model-ER/
│   ├── 2026-04-13-codi-sql-Creació-de-Taules/
│   ├── 2026-04-17-SQL-rols-permisos/
│   ├── 2026-05-6 - Alta disponibilitat/
│   └── Entregues_Finals/       # document final i manuals
└── src/
    ├── main.py                 # punt d'entrada
    ├── pantalles/              # login i menús per rol
    ├── login/                  # usuaris, hash, permisos i log d'accessos
    ├── manteniment/            # altes i gestió de pacients, personal, visites i espais
    ├── consultes/              # informes i consultes avançades
    ├── exportacions/           # exportació JSON/XML i esquemes
    └── dummy/                  # generació i esborrat de dades de prova
```

## Base de dades

El disseny parteix d'un model entitat-relació que després es tradueix a taules:

- **Personal** amb especialització exclusiva en *metge*, *infermeria* i *personal vari*.
- **Pacients** i **visites**, amb el metge que atén cada visita i els medicaments receptats (dosi i freqüència).
- **Plantes**, **habitacions** i **quiròfans**, amb els aparells mèdics de cada quiròfan i les seves quantitats.
- **Operacions** i assistències del personal d'infermeria.
- **Reserves d'habitació** i **logs d'accés**.

Documentació relacionada:

- [Model ER i explicació de les cardinalitats](docs/2026-04-12-model-ER/Documentaci%C3%B3%20MER.md)
- [Diagrama del model ER](docs/2026-04-12-model-ER/Model-ER-Hospital-Blanes.drawio.png)
- [Model relacional](docs/2026-04-11-model-relacional/Model%20Relacional%20Hospital%20de%20Blanes.pdf)
- [DDL de creació de taules](docs/2026-04-13-codi-sql-Creaci%C3%B3-de-Taules/SQL-DDL-Taules-BBD)
- [Rols de PostgreSQL](docs/2026-04-17-SQL-rols-permisos/rols.sql) i [permisos](docs/2026-04-17-SQL-rols-permisos/permisos.sql)

## Instal·lació

### Requisits

- Python 3.11 o superior
- PostgreSQL 16 en funcionament
- Tkinter (inclòs a la instal·lació estàndard de Python a Windows i macOS; a Linux cal `python3-tk`)

### Passos

```bash
git clone https://github.com/josedaaaasilva-code/Projecta-Intermodular-ASIX-Hospital.git
cd Projecta-Intermodular-ASIX-Hospital

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install psycopg2-binary bcrypt faker
```

1. Crea la base de dades `hospital` a PostgreSQL.
2. Executa el DDL de `docs/2026-04-13-codi-sql-Creació-de-Taules/` per crear les taules.
3. Crea els rols i aplica els permisos amb els scripts de `docs/2026-04-17-SQL-rols-permisos/`.
4. Ajusta els paràmetres de connexió (amfitrió, base de dades, usuari i contrasenya) als mòduls de `src/` perquè apuntin al teu servidor. Al repositori no es publiquen credencials reals.

### Dades de prova (opcional)

Des de `src/dummy/` es poden generar desenes de milers de registres amb `faker`, i esborrar-los després per deixar la base de dades neta. També hi ha els índexs per accelerar les consultes massives.

## Ús

```bash
python src/main.py
```

S'inicia la finestra de login. Un cop validat l'usuari, l'aplicació obre el menú corresponent al seu rol:

| Rol | Accés |
|---|---|
| **Admin** | Gestió completa: usuaris, manteniment, consultes i exportacions |
| **Administratiu** | Altes i consultes de pacients, personal i visites |
| **Metge** | Consulta de les seves visites i informes clínics |
| **Infermer** | Consulta de pacients assignats i assistències |

## Exportacions

Les visites es poden exportar entre dues dates a JSON i XML. Cada exportació queda guardada amb marca de temps a `src/exportacions/historial_json/` i `historial_xml/`, d'acord amb els esquemes `schema_visites.json` i `schema_visites.xsd`.

## Documentació

Tota la documentació del projecte és a [`docs/`](docs/), organitzada per entregues:

| Data | Contingut |
|---|---|
| 2026-04-08 | [Planificació del projecte](docs/2026-04-08-planificaci%C3%B3/README.md): eines, metodologia i cronograma |
| 2026-04-11 | Model relacional |
| 2026-04-12 | [Model ER i diccionari](docs/2026-04-12-model-ER/Documentaci%C3%B3%20MER.md) |
| 2026-04-13 | DDL de creació de taules |
| 2026-04-17 | Rols i permisos, i document de protecció de dades (AGPD) |
| 2026-04-28 | Bloc de manteniment (obligatoris i opcionals) |
| 2026-05-06 | Alta disponibilitat: maquinari, còpies de seguretat i rèplica activa-passiva |
| 2026-05-13 | Dades dummy i índexs |

**Entregues finals**

- [Document final del projecte](docs/Entregues_Finals/HospitalHarmoniaBlanes_Document-Final.pdf)
- [Manual d'instal·lació](docs/Entregues_Finals/HospitalHarmoniaBlanes_Manual-Instal%C2%B7laci%C3%B3.pdf)
- [Manual d'usuari](docs/Entregues_Finals/HospitalHarmoniaBlanes_Manual-Usuari%20.pdf)

## Equip

Projecte intermodular del CFGS ASIX (2025—2027), IES Sa Palomera (Blanes):

- **Gabriela Borrull López**
- **Jose da Silva Silva**

## Avís

Projecte acadèmic sense ànim comercial. Els noms, DNIs i dades clíniques que genera el mode *dummy* són inventats i no corresponen a persones reals.
