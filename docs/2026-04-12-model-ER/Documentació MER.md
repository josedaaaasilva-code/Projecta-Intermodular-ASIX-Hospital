# Model ER

## Especialització del personal
Al model hi ha un Triangle “ES D,T” que connecta PERSONAL amb METGE, INFERMERIA i VARI. Això vol dir que cada treballador només pot ser d’un tipus (és exclusiu), però obligatòriament ha de ser-ne d’algun (total).

Per exemple, els metges guarden el currículum i l’especialitat, les infermeres també, i el personal vari només guarda el tipus de tasca. ç

## Relació "assignat"
La relació entre METGE i INFERMERIA s’anomena “assignat”. Un metge pot tenir un o més infermers assignats (1,N), mentre que un infermer pot estar assignat a un únic metge o a cap (0,1), ja que hi pot haver infermers de planta que no depenguin d’un metge concret.

## Plantes, habitacions i quiròfans
Al diagrama hi ha PLANTA, HABITACIÓ i QUIRÒFAN. Una planta té moltes habitacions (1,N) i cada habitació pertany a una sola planta (1,1).

Pel que fa als quiròfans, també estan dins de plantes, però no totes les plantes en tenen, per això la cardinalitat des de PLANTA és (0,N). Així es reflecteix millor la realitat.

## Aparells mèdics als quiròfans
Hi ha una relació anomenada “està” entre QUIRÒFAN i APARELL_MÈDIC que inclou l’atribut “quantitat”. Això permet saber quants aparells de cada tipus hi ha a cada quiròfan.

Sense aquesta relació intermèdia, no es podria guardar aquesta informació.

## Visites i pacients
A la relació “realitza” entre PACIENT i VISITA hi ha una línia doble des de PACIENT, que indica que tot pacient té almenys una visita. Les cardinalitats són (1,1) des de PACIENT i (1,N) des de VISITA.

Després, la relació “atén” connecta METGE amb VISITA amb cardinalitat (0,N), ja que un metge pot no haver atès cap visita.

## Medicaments receptats
Al model hi ha MEDICAMENT i una entitat intermèdia anomenada MEDICAMENT_RECEPTAT (corregint una errada inicial).

Aquesta entitat guarda la dosi i la freqüència, i connecta amb VISITA i MEDICAMENT. Així, una visita pot receptar diversos medicaments (0,N) i un medicament pot aparèixer en moltes receptes (1,N).

## Reserves d’habitació
L’entitat RESERVA_HABITACIÓ es relaciona amb PACIENT amb cardinalitat (0,N), perquè no tots els pacients fan reserves, i amb HABITACIÓ també amb (0,N), ja que no totes les habitacions estan reservades.

Aquestes cardinalitats són coherents amb la realitat.

## Operacions i assistències
Finalment, hi ha OPERACIÓ i ASSISTÈNCIA_OPERACIÓ. Aquesta última es relaciona amb OPERACIÓ (1,N) i amb INFERMERIA (0,N).

Això vol dir que una operació pot tenir diverses infermeres assistint, i una infermera pot participar en diverses operacions. A més, la relació “assisteix” connecta INFERMERIA amb ASSISTÈNCIA_OPERACIÓ, indicant que cada assistència correspon a una única infermera, però una infermera pot tenir moltes assistències.
