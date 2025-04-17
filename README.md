# Reseptipankki

## Toiminnot
- Sovelluksessa käyttäjät pystyvät jakamaan ruokareseptejään. Reseptissä lukee tarvittavat ainekset ja valmistusohje.
- Resepteille voi lisätä yhden kuvan. Kuvan voi vaihtaa toiseen tai poistaa.
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään reseptejä ja muokkaamaan ja poistamaan niitä.
- Käyttäjä näkee sovellukseen lisätyt reseptit.
- Käyttäjä pystyy etsimään reseptejä hakusanalla.
- Käyttäjäsivu näyttää, montako reseptiä käyttäjä on lisännyt ja listan käyttäjän lisäämistä resepteistä.
- Käyttäjä pystyy valitsemaan reseptille yhden tai useamman luokittelun (esim. alkuruoka, pääruoka, vegaaninen).
- Käyttäjä pystyy antamaan reseptille kommentin. Reseptistä näytetään kommentit.

## Sovelluksen testaus suurella tietomäärällä
- Loin sovellukseen 1 000 käyttäjää, 1 000 000 reseptiä ja 10 000 000 kommenttia
- Etusivu latasi käytännössä heti, eikä sivujen vaihdossa ole viivettä
- Reseptien haku toimii hitaammin jos haulla on todella paljon tuloksia (yli 50 000)
- Kaikki muut toiminnot toimivat viiveittä

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Voit käynnistää sovelluksen näin:

```
$ flask run
```
