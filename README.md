# Cyclic Metric Calculation Demo

## Project Description

This project is a web application based on Flask that allows for cyclic execution of tasks calculating the **accuracy** metric for machine learning models. Tasks are scheduled based on a cron expression provided by the user and executed using Celery. Results are stored in Redis, while information about schedules and input data is kept in a PostgreSQL database. The entire application is run and managed using Docker Compose.

## Features

- **Task Scheduling:** Enables adding, updating, and deleting cyclic tasks based on `model_id` and `cron_expression`.
- **Accuracy Metric Calculation:** The task fetches the latest data for a given `model_id` and calculates the accuracy metric using the scikit-learn library.
- **Result Storage:** Calculation results are stored in Redis and accessible via an API.
- **Scalability:** Utilizing Celery and Docker allows for easy scaling of the application.

## Architecture

- **Flask (`main.py`):** The application server handling HTTP requests.
- **Celery Workers (`tasks.py`):** Execute asynchronous computational tasks.
- **Redis:** Serves as a broker for Celery and as a result store.
- **PostgreSQL:** The database storing information about schedules and input data.
- **Docker Compose:** A tool for orchestrating Docker containers.

## Running the Project

**Run Docker Compose:**

```bash
docker-compose up --build
```

This command will build the Docker images and start all services.

## Usage

### API Endpoints

1. **Add or Update a Task:**

   ```
   POST /schedule
   ```

   **Body (JSON):**

   - `model_id` (string, UUID): The model identifier.
   - `cron_expression` (string): The cron expression defining the schedule.

2. **Retrieve Result:**

   ```
   GET /results/<model_id>
   ```

   **Parameters:**

   - `model_id` (string, UUID): The model identifier.

### Examples

**Adding a Task:**

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "model_id": "550e8400-e29b-41d4-a716-446655440000",
  "cron_expression": "*/1 * * * *"
}' http://localhost:5000/schedule
```

**Retrieving a Result:**

```bash
curl http://localhost:5000/results/550e8400-e29b-41d4-a716-446655440000
```

## Library Descriptions

- **Flask:**

  A micro web framework for Python. Used to create the API handling HTTP requests.

- **Celery:**

  An asynchronous task queue/job queue system. Enables background task execution and scheduling.

- **Redis:**

  An in-memory key-value store. Used in the project as a broker for Celery and for storing results.

- **psycopg2-binary:**

  A PostgreSQL database adapter for Python. Allows connecting to the database and executing SQL queries.

- **scikit-learn:**

  A machine learning library for Python. Used in the project for calculating metrics.

- **RedBeat:**

  A Celery scheduler based on Redis. Allows for persistent and distributed task scheduling.

## Additional Information

- **PostgreSQL Database:**

  - Tables:

    - `metrics_executions`:
      - `id`: Primary key.
      - `model_id`: Model UUID.
      - `cron_expression`: Cron expression for the schedule.
    - `results`:
      - `id`: Primary key.
      - `model_id`: Model UUID.
      - `y_true`: Actual values data (JSON).
      - `y_pred`: Predicted values data (JSON).
      - `timestamp`: Timestamp of data insertion.

- **Inter-service Communication:**

  Services communicate with each other via the Docker Compose network, using service names as hosts (e.g., `postgres`, `redis`).

- **Task Scheduling:**

  Tasks are scheduled using cron expressions provided by the user. RedBeat is used as the scheduler, storing task information in Redis.

## Original Project Requirements

Write project code that:
1. Receives a request with `model_id` (type UUID) and `cron_expression` (type string) - (use Flask)
2. Starts cyclically running a Celery task (according to the received `cron_expression`)
3. `cron_expression` and `model_id` will be saved in a PostgreSQL database in the 'metrics_executions' table
4. If a cyclic task already exists for a given `model_id`, delete it and create a new one.
5. Results can be queried through a separate endpoint of the Flask service
6. The task will extract the latest row from the 'results' table where the 'model_id' from the request equals the 'model_id' in the table.
7. Then it will calculate the accuracy metric (using the scikit-learn library) based on the retrieved data from the database.
8. The task saves the results in Redis.
9. Use Redis as the broker for Celery
10. Use PostgreSQL as the database
11. Use Docker Compose to run all services
12. Celery should be configured to execute tasks in a separate Docker container.
13. Do not use SQLAlchemy; only use SQL scripts
14. Additionally, generate SQL scripts to create tables and test data
15. In the database, both predictions and actual values should be columns of type JSON