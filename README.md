
# Cyclic Metric Calculation Demo


## Opis projektu

Projekt to aplikacja webowa oparta na Flask, która pozwala na cykliczne uruchamianie zadań obliczających metrykę **accuracy** dla modeli machine learning. Zadania są harmonogramowane na podstawie wyrażenia cron dostarczonego przez użytkownika i wykonywane za pomocą Celery. Wyniki są przechowywane w Redis, a informacje o harmonogramach i danych wejściowych w bazie danych PostgreSQL. Całość jest uruchamiana i zarządzana za pomocą Docker Compose.

## Funkcjonalności

- **Harmonogramowanie zadań:** Umożliwia dodawanie, aktualizowanie i usuwanie cyklicznych zadań na podstawie `model_id` i `cron_expression`.
- **Obliczanie metryki accuracy:** Zadanie pobiera najnowsze dane dla danego `model_id` i oblicza metrykę accuracy przy użyciu biblioteki scikit-learn.
- **Przechowywanie wyników:** Wyniki obliczeń są przechowywane w Redis i dostępne poprzez API.
- **Skalowalność:** Wykorzystanie Celery i Docker pozwala na łatwe skalowanie aplikacji.

## Architektura

- **Flask (`main.py`):** Serwer aplikacji obsługujący żądania HTTP.
- **Celery Workers (`tasks.py`):** Wykonują asynchroniczne zadania obliczeniowe.
- **Redis:** Służy jako broker dla Celery i magazyn wyników.
- **PostgreSQL:** Baza danych przechowująca informacje o harmonogramach i danych wejściowych.
- **Docker Compose:** Narzędzie do orkiestracji kontenerów Dockerowych.

## Uruchomienie projektu

**Uruchom Docker Compose:**

   ```bash
   docker-compose up --build
   ```

   To polecenie zbuduje obrazy Dockerowe i uruchomi wszystkie serwisy.

## Użycie

### Endpointy API

1. **Dodanie lub aktualizacja zadania:**

   ```
   POST /schedule
   ```

   **Body (JSON):**

   - `model_id` (string, UUID): Identyfikator modelu.
   - `cron_expression` (string): Wyrażenie cron określające harmonogram.

2. **Pobranie wyniku:**

   ```
   GET /results/<model_id>
   ```

   **Parametry:**

   - `model_id` (string, UUID): Identyfikator modelu.

### Przykłady

**Dodanie zadania:**

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "model_id": "550e8400-e29b-41d4-a716-446655440000",
  "cron_expression": "*/1 * * * *"
}' http://localhost:5000/schedule
```

**Pobranie wyniku:**

```bash
curl http://localhost:5000/results/550e8400-e29b-41d4-a716-446655440000
```


## Opis bibliotek

- **Flask:**

  Mikroframework webowy dla Pythona. Używany do tworzenia API obsługującego żądania HTTP.

- **Celery:**

  System kolejkowania zadań asynchronicznych. Umożliwia wykonywanie zadań w tle oraz ich harmonogramowanie.

- **Redis:**

  Magazyn klucz-wartość działający w pamięci. W projekcie używany jako broker dla Celery oraz do przechowywania wyników.

- **psycopg2-binary:**

  Adapter bazy danych PostgreSQL dla Pythona. Pozwala na łączenie się z bazą danych i wykonywanie zapytań SQL.

- **scikit-learn:**

  Biblioteka do uczenia maszynowego w Pythonie. W projekcie używana do obliczania metryk.

- **redbeat:**

  Harmonogram zadań dla Celery oparty na Redis. Pozwala na harmonogramowanie zadań w sposób trwały i rozproszony.

## Dodatkowe informacje

- **Baza danych PostgreSQL:**

  - Tabele:

    - `metrics_executions`:
      - `id`: Klucz główny.
      - `model_id`: UUID modelu.
      - `cron_expression`: Wyrażenie cron dla harmonogramu.
    - `results`:
      - `id`: Klucz główny.
      - `model_id`: UUID modelu.
      - `y_true`: Dane rzeczywistych wartości (JSON).
      - `y_pred`: Dane przewidywane (JSON).
      - `timestamp`: Znacznik czasu wstawienia danych.

- **Komunikacja między serwisami:**

  Serwisy komunikują się ze sobą poprzez sieć Docker Compose, używając nazw serwisów jako hostów (np. `postgres`, `redis`).

- **Harmonogramowanie zadań:**

  Zadania są harmonogramowane za pomocą wyrażeń cron dostarczonych przez użytkownika. Używany jest RedBeat jako scheduler, który przechowuje informacje o zadaniach w Redis.

## Pierwotne wymagania projektu

Napisz kod projektu który:
1. Odbierze request z model_id (typ to uuid) oraz cron_expression (typ to string) - (użyj Flask)
2. Zacznie cyklicznie odpalać task celery (zgodnie z odebranym cron_expression) 
3. cron_expression i model_id będą zapisywane w bazie dancyh postgres w tabeli 'metrics_executions' 
4. Jeżeli dla danego model_id będzie już istniał cykliczny task to usuń go i stwórz nowy.
5. Będzie można zapytać o rezultaty w osobnym endpointcie serwisu flask
6. Task ten będzie wyciągał z tabeli 'results' najnowszy wiersz gdzie 'model_id' z requestu będzie równy 'model_id' z tabeli.
7. Następnie policzy metryke accuracy (biblioteka scikit-learn) na podstawie odebranych danych z bazy.
8. Task zapisuje rezultaty w redis.
9. Jako broker dla celery użyj redis 
10. Jako bazę danych uzyj postgres 
11. Użyj docker compose do uruchomienia wszystkich serwisów
12. Celery ma być tak skonfigurowane aby wykonywać zadania w osobnym kontenerze dockerowym.
13. Nie używaj SQLAlchemy a jedynie skryptów SQL 
14. Dodatkowo wygeneruj skrypty sql do stworzenia tabel oraz testowych danych 
15. W bazie danych zarówno predykcje jak i rzeczywiste wartości mają być kolumnami typu json