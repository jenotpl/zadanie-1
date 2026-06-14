# OpenPsychology Journal Scraper

Skrypt do pobierania listy peer-reviewed badań z rejestru OpenPsychology Journal.

## Opis

Ten skrypt pobiera **10 peer-reviewed artykułów naukowych** z rejestru https://openpsychologyjournal.com/.

## Wymagania

- Python 3.7+
- requests
- beautifulsoup4

## Instalacja

```bash
pip install -r requirements.txt
```

## Użycie

```bash
python scraper.py
```

## Funkcjonalności

- ✅ Pobieranie 10 peer-reviewed badań
- ✅ Wyciąganie metadanych (tytuł, autorzy, data publikacji, DOI, keywords)
- ✅ Wyświetlanie wyników w konsoli
- ✅ Zapis do pliku JSON
- ✅ Fallback na scraping HTML w przypadku niedostępności API
- ✅ Obsługa błędów i timeoutów

## Wyjście

Skrypt generuje:
1. **Wysyłka na stdout** - wyświetlenie badań w czytelnym formacie
2. **Plik JSON** - `openpsychology_studies.json` z kompletną listą

## Struktura danych

Każde badanie zawiera:
- `id` - unikalny identyfikator
- `title` - tytuł artykułu
- `authors` - lista autorów
- `abstract` - streszczenie (jeśli dostępne)
- `publication_date` - data publikacji
- `peer_reviewed` - status peer review (zawsze true)
- `url` - link do artykułu
- `doi` - Digital Object Identifier
- `keywords` - słowa kluczowe
- `citation_count` - liczba cytowań

## Autor

Wygenerowano automatycznie
