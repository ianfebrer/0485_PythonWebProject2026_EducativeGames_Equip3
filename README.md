# 0485_PythonWebProject2026_EducativeGames_Equip3

---

# 1️⃣ Educative games (objectiu educatiu)

Desenvolupar una **aplicació web amb Flask** basada en el **paradigma de la programació orientada a objectes**, que permeta a l’usuari interactuar amb **jocs educatius de figures geomètriques i colors**, gestionant usuaris, jocs i resultats mitjançant **objectes Python**.

## Requisits generals de disseny

L’aplicació haurà d’estar estructurada utilitzant **classes Python**, com a mínim per representar:

* Usuaris
* Jocs
* Figures geomètriques
* Resultats i puntuacions

L’aplicació haurà de permetre a la persona usuària **seleccionar almenys tres jocs diferents**, cadascun amb un tipus d’interacció diferent:

1. Prémer el teclat i que passe cada cop una cosa diferent.
2. Moure el ratolí per interactuar amb la pantalla.
3. Fer clic amb el ratolí per arrossegar figures a la seua correcta posició.

**Web referència** -> [https://elbuhoboo.com/cat/jocs-educatius/](https://elbuhoboo.com/cat/jocs-educatius/)

---

| Backend (Flask – Python) | Frontend (Client web) |
| --- | --- |
| • Carregar les pàgines web | • Gestionar la interacció de l’usuari: |
| • Gestionar les rutes de l’aplicació |     ◦ Drag & drop |
| • Validar les accions del joc mitjançant mètodes d’objectes |     ◦ Accions de teclat |
| • Mostrar missatges de resultat (èxit/error) |     ◦ Moviment i clics del ratolí |
| • Emmagatzemar l’històric de resultats per usuari, utilitzant classes Python en un **fitxer JSON** | • Comunicar-se amb el backend mitjançant peticions HTTP |

---

## Funcionalitats avaluables (obligatori)

L’aplicació haurà de permetre:

* Gestió de puntuació per joc i usuari
* Ús de **figures geomètriques complexes** (que no siguen polígons bàsics)
* Autenticació d’usuaris
* Emmagatzematge automàtic de resultats per usuari
* Disseny responsive (adaptat a dispositius mòbils)

## Propostes d’ampliació (no obligatòries)

* Control del temps dedicat a cada joc
* Rànquing de millors puntuacions
* Separació completa frontend / backend

---
