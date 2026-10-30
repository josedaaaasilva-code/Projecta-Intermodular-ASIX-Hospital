#index per taula base
-- PERSONAL
#accelera cerques per dni
CREATE INDEX IF NOT EXISTS idx_personal_dni ON personal(dni);
#optimitza cerques per nom
CREATE INDEX IF NOT EXISTS idx_personal_nom ON personal(nom);
#optimitza cerques per cognoms
CREATE INDEX IF NOT EXISTS idx_personal_cognoms ON personal(cognoms);

-- PACIENT
#cerques ràpides per dni_pacient
CREATE INDEX IF NOT EXISTS idx_pacient_dni ON pacient(dni_pacient);
#cerques ràpides per nom_pacient
CREATE INDEX IF NOT EXISTS idx_pacient_nom ON pacient(nom_pacient);
#cerques ràpides per cognoms_pacient
CREATE INDEX IF NOT EXISTS idx_pacient_cognoms ON pacient(cognoms_pacient)

#índexs per a taules dependents de personal
-- METGE
#accelera el JOIN entre metge.id_personal i personal.id_personal
CREATE INDEX IF NOT EXISTS idx_metge_personal ON metge(id_personal);
#cerques per especialitat
CREATE INDEX IF NOT EXISTS idx_metge_especialitat ON metge(especialitat_metge);

-- INFERMERIA
#JOIN ràpid amb PERSONAL
CREATE INDEX IF NOT EXISTS idx_infermeria_personal ON infermeria(id_personal);
#consultes del tipus: “quines infermeres treballen amb aquest metge”
CREATE INDEX IF NOT EXISTS idx_infermeria_metge ON infermeria(id_metge);
#consultes per planta assignada
CREATE INDEX IF NOT EXISTS idx_infermeria_planta ON infermeria(id_planta);

-- VARI
#JOIN ràpid amb PERSONAL
CREATE INDEX IF NOT EXISTS idx_vari_personal ON vari(id_personal);

#índexs per a infraestructura
-- HABITACIO
#consultes per planta (habitacions d’una planta concreta)
CREATE INDEX IF NOT EXISTS idx_habitacio_planta ON habitacio(num_planta);

-- QUIROFAN
#consultes per planta (quirofans d’una planta)
CREATE INDEX IF NOT EXISTS idx_quirofan_planta ON quirofan(num_planta);

-- APARELL_MEDIC
#consultes per tipus d’aparell (ex: “tots els monitors cardíacs”)
CREATE INDEX IF NOT EXISTS idx_aparell_medic_tipus ON aparell_medic(id_tipus);

-- APARELL_EN_QUIROFAN
#consultes per quiròfan (quins aparells té)
CREATE INDEX IF NOT EXISTS idx_aparell_en_quirofan_quirofan ON aparell_en_quirofan(id_quirofan);
#consultes inverses (en quin quiròfan està un aparell)
CREATE INDEX IF NOT EXISTS idx_aparell_en_quirofan_aparell ON aparell_en_quirofan(id_aparell);

#índex per a activitat
-- VISITA
#consultes de visites d’un pacient
CREATE INDEX IF NOT EXISTS idx_visita_pacient ON visita(id_pacient);
#consultes de visites d’un metge
CREATE INDEX IF NOT EXISTS idx_visita_metge ON visita(id_metge);
#consultes per data (agenda, informes, estadístiques)
CREATE INDEX IF NOT EXISTS idx_visita_data ON visita(data);

-- OPERACIO
#operacios d'un pacient
CREATE INDEX IF NOT EXISTS idx_operacio_pacient ON operacio(id_pacient);
#operacis d'un metge
CREATE INDEX IF NOT EXISTS idx_operacio_metge ON operacio(id_metge);
#operacios en un quiròfan concret
CREATE INDEX IF NOT EXISTS idx_operacio_quirofan ON operacio(id_quirofan);
#consultes per data d'operació
CREATE INDEX IF NOT EXISTS idx_operacio_data ON operacio(data_operacio);

-- ASSISTENCIA_OPERACIO
#consultes de personal assignat a una operació
CREATE INDEX IF NOT EXISTS idx_assistencia_operacio_operacio ON assistencia_operacio(id_operacio);
#consultes d’operacions on ha assistit una infermera
CREATE INDEX IF NOT EXISTS idx_assistencia_operacio_infermeria ON assistencia_operacio(id_infermeria);

-- 
#medicaments receptats en una visita
CREATE INDEX IF NOT EXISTS idx_medicament_receptat_visita ON medicament_receptat(id_visita);
#consultes per medicament (estadístiques, informes)
CREATE INDEX IF NOT EXISTS idx_medicament_receptat_medicament ON medicament_receptat(id_medicament);

-- RESERVA_HABITACIO
#habitacions reservades per un pacient
CREATE INDEX IF NOT EXISTS idx_reserva_habitacio_pacient ON reserva_habitacio(id_pacient);
#consultes per habitació
CREATE INDEX IF NOT EXISTS idx_reserva_habitacio_habitacio ON reserva_habitacio(id_habitacio);
#consultes per data d'ingrés(gestió d'ocupació)
CREATE INDEX IF NOT EXISTS idx_reserva_habitacio_data_ingres ON

 #índexs per a usuaris
-- USUARIS
#relacionar usuari amb personal
CREATE INDEX IF NOT EXISTS idx_usuaris_personal ON usuaris(id_personal);
#consultar per rol (administradors, metges...)
CREATE INDEX IF NOT EXISTS idx_usuaris_rol ON usuaris(id_rol);

-- LOGS_ACCESSOS
#consultes d'accessos d'un usuari
CREATE INDEX IF NOT EXISTS idx_logs_accessos_usuari ON logs_accessos(id_usuari);
#consultes per data(auditories, informes de seguretat)
CREATE INDEX IF NOT EXISTS idx_logs_accessos_data ON logs_accessos(data_hora);
