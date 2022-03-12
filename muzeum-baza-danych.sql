CREATE TYPE TYP AS ENUM ('obraz', 'rzezba', 'inny');
CREATE TYPE STAN AS ENUM ('w ekspozycji', 'wypozyczony', 'w magazynie');

CREATE TABLE Instytucja (
  id NUMERIC PRIMARY KEY, 
  nazwa VARCHAR NOT NULL,
  miasto VARCHAR NOT NULL
);

CREATE TABLE Artysta (
  id NUMERIC PRIMARY KEY, 
  imie VARCHAR NOT NULL,
  nazwisko VARCHAR NOT NULL,
  rok_urodzenia NUMERIC NOT NULL,
  rok_smierci NUMERIC
);

CREATE TABLE Eksponat (
  id NUMERIC PRIMARY KEY,
  autor NUMERIC REFERENCES Artysta,
  tytul VARCHAR NOT NULL,
  typ_eksponatu TYP NOT NULL,
  wypozyczalny BOOLEAN NOT NULL,
  stan STAN NOT NULL,
  CONSTRAINT wypozyczalnosc_check CHECK (wypozyczalny OR stan != 'wypozyczony'),
  id_wypozyczenia NUMERIC,
  id_ekspozycji NUMERIC,
  CONSTRAINT stan_check CHECK (
    (stan = 'w magazynie' AND id_wypozyczenia IS NULL AND id_ekspozycji IS NULL) OR
    (stan = 'w ekspozycji' AND id_wypozyczenia IS NULL AND id_ekspozycji IS NOT NULL) OR
    (stan = 'wypozyczony' AND id_wypozyczenia IS NOT NULL AND id_ekspozycji IS NULL)),
  szerokosc NUMERIC NOT NULL,
  wysokosc NUMERIC NOT NULL,
  waga NUMERIC NOT NULL
);

CREATE TABLE Wypozyczenie (
  id NUMERIC PRIMARY KEY,
  id_eksponatu NUMERIC NOT NULL REFERENCES Eksponat,
  id_instytucji NUMERIC NOT NULL REFERENCES Instytucja,
  poczatek DATE NOT NULL, 
  koniec DATE NOT NULL,
  CONSTRAINT prawidlowe_daty_wypozyczenia CHECK (poczatek <= koniec)
);

CREATE TABLE Ekspozycja (
  id NUMERIC PRIMARY KEY,
  id_eksponatu NUMERIC NOT NULL REFERENCES Eksponat,
  galeria VARCHAR NOT NULL,
  sala NUMERIC NOT NULL,
  poczatek DATE,
  koniec DATE
);

ALTER TABLE Eksponat
ADD CONSTRAINT fk_wypozyczenie 
FOREIGN KEY(id_wypozyczenia) REFERENCES Wypozyczenie;
ALTER TABLE Eksponat
ADD CONSTRAINT fk_ekspozycja
FOREIGN KEY(id_ekspozycji) REFERENCES Ekspozycja;

CREATE OR REPLACE FUNCTION artysta_nie_posiada_eksponatu() RETURNS TRIGGER AS $$
BEGIN
  RAISE NOTICE 'Dodałeś nowego artystę, który na razie nie jest autorem żadnego eksponatu. Dodaj nowy eksponat tego autora lub usuń go.';
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER artysta_posiada_eksponat
  AFTER INSERT ON Artysta
  FOR EACH ROW EXECUTE PROCEDURE artysta_nie_posiada_eksponatu();

-- Sprawdza czy po zmienie stanu eksponatu nadal w muzeum znajduje się przynajmniej jeden
-- eksponat jego autora.
CREATE OR REPLACE FUNCTION czy_eksponat_artysty_w_muzeum() RETURNS TRIGGER AS $$
BEGIN
  IF NOT EXISTS
    (SELECT id FROM Eksponat
     WHERE autor = NEW.id AND (stan = 'w ekspozycji' OR stan = 'w magazynie'))
  THEN
    RAISE EXCEPTION 'Przynajmniej jeden eksponat każdego artysty musi znajdować się w muzeum.';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER  eksponat_artysty_w_muzeum
  AFTER UPDATE OF stan ON Eksponat
  FOR EACH ROW EXECUTE PROCEDURE czy_eksponat_artysty_w_muzeum();

-- Sprawdza czy po dodaniu lub zmienieniu wypożyczenia eksponatu nadal jest spełniony warunek, 
-- że ten eksponat nie przebywa poza muzeum dłużej niż 30 dni w danym roku kalendarzowym.
CREATE OR REPLACE FUNCTION sprawdz_limit_wypozyczen() RETURNS TRIGGER AS $$
DECLARE 
  rok_poczatek NUMERIC := EXTRACT(YEAR FROM NEW.poczatek);
  rok_koniec NUMERIC := EXTRACT(YEAR FROM NEW.koniec);
  rok NUMERIC := rok_poczatek;
BEGIN
  IF rok_koniec - rok_poczatek >= 2 THEN
    RAISE EXCEPTION 'Eksponat nie może przebywać poza muzeum dłużej niż 30 dni rocznie';
  ELSE
    LOOP 
      IF (
        (WITH wypozyczenia_eksponatu AS (
          SELECT CASE
            WHEN EXTRACT(YEAR FROM poczatek) < rok THEN
              koniec - MAKE_DATE(rok::INTEGER, 01, 01) + 1
            WHEN EXTRACT(YEAR FROM koniec) > rok THEN
              MAKE_DATE(rok::INTEGER, 12, 31) - poczatek + 1
            ELSE
              koniec - poczatek
            END AS liczba_dni
          FROM Wypozyczenie
          WHERE id_eksponatu = NEW.id_eksponatu
            AND EXTRACT(YEAR FROM poczatek) <= rok
            AND EXTRACT(YEAR FROM koniec) >= rok
        )
        SELECT SUM(liczba_dni) FROM wypozyczenia_eksponatu) > 30 )
      THEN
        RAISE EXCEPTION 'Eksponat nie może przebywać poza muzeum dłużej niż 30 dni rocznie';
      END IF;
    
    rok := rok + 1;
    EXIT WHEN rok > rok_koniec;
    
    END LOOP;  
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER  limit_wypozyczen
  AFTER INSERT OR UPDATE OF poczatek, koniec ON Wypozyczenie
  FOR EACH ROW EXECUTE PROCEDURE sprawdz_limit_wypozyczen();

