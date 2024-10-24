# ADR: Proposal to Change the Implementation Technology of the Metrics Service from Java to Python

- **Date**: [insert date]
- **Status**: Proposed

## Context

Currently, the **Metrics** service is implemented in **Java**. This service is responsible for collecting, processing, and providing metrics related to the operation of our models apps. As the project has developed, we have encountered several challenges related to maintaining and developing the service in Java:

- **Code Complexity**: Implementation in Java requires writing more extensive code, which translates into difficulties in quickly introducing changes.
- **Performance in Asynchronous Tasks**: Java, although powerful, may be less efficient in simple asynchronous tasks compared to Python using tools like Celery.

A prototype was created and presented. A discussion was held about this code, and since the team expressed optimism, this ADR has been created as a result.

## Proposal

We propose to **port the Metrics service from Java to Python**, utilizing the **Flask** or other framework for API handling and **Celery** for managing asynchronous tasks and scheduling. Additionally, we would use **Redis** as the message broker and result store, and **OracleDB** as the database.

### Detailed Architecture of the Proposed Solution

The proposed architecture consists of the following components:

1. **Flask Application**:
   - Acts as the web server handling HTTP requests.
   - Provides API endpoints for:
     - Receiving requests with `model_id` (UUID) and `cron_expression` (string) to schedule tasks.
     - Retrieving results for a given `model_id`.
   - Interacts with PostgreSQL to store and retrieve scheduling information.

2. **Celery Workers**:
   - Execute asynchronous tasks defined in the application.
   - Tasks include:
     - Fetching the latest data for a given `model_id` from the `results` table in PostgreSQL.
     - Calculating the accuracy metric using scikit-learn based on the retrieved data.
     - Storing the results in Redis for quick access.
   - Celery Beat (or RedBeat) is used for scheduling tasks based on `cron_expression`.

3. **Redis**:
   - Serves as the message broker for Celery, facilitating communication between the Flask application and Celery workers.
   - Acts as a result backend, storing the outputs of the tasks for quick retrieval.

4. **OracleDB Database**:
   - Stores:
     - Task scheduling information in the `metrics_executions` table, containing `model_id` and `cron_expression`.
     - Input data in the `results` table, including `model_id`, `y_true`, `y_pred`, and `timestamp`.
   - Data is accessed directly using SQL scripts (without ORM), ensuring efficiency and simplicity.

5. **Docker and Docker Compose**:
   - Each component (Flask application, Celery workers, Redis, PostgreSQL) runs in its own Docker container.
   - Enables easy scaling of Celery workers by adjusting the number of worker containers.

### Workflow

1. **Task Scheduling**:
   - A user sends a POST request to the Flask API with `model_id` and `cron_expression`.
   - The Flask application:
     - Checks if a task already exists for the given `model_id`; if so, it removes the existing task.
     - Stores the new `model_id` and `cron_expression` in the `metrics_executions` table in PostgreSQL.
     - Schedules a new Celery task based on the provided `cron_expression`.

2. **Task Execution**:
   - At scheduled intervals, Celery workers execute the task:
     - Retrieve the latest entry from the `results` table where `model_id` matches.
     - Calculate the accuracy metric using scikit-learn.
     - Store the result in Redis for quick access.

3. **Result Retrieval**:
   - A user sends a GET request to the Flask API with `model_id` to retrieve the calculated metric.
   - The Flask application fetches the result from Redis and returns it to the user.

### Benefits of the Proposed Architecture

- **Simplified Codebase**: Python's concise syntax reduces code complexity, making it easier to maintain and extend.
- **Efficient Asynchronous Processing**: Celery provides robust support for asynchronous task execution and scheduling.
- **Scalability**: Docker allows for easy scaling of components, especially Celery workers, to handle increased load.
- **Team Expertise**: Leveraging the team's proficiency in Python enhances productivity and code quality.
- **Rich Ecosystem**: Python's extensive libraries (e.g., scikit-learn) facilitate advanced data processing and machine learning tasks.

## Potential Consequences

### Positive

- **Increased Productivity**: Faster development due to simpler language and better-aligned tools.
- **Improved Asynchronous Task Handling**: Efficient management of background tasks with Celery.
- **Better Integration with Analytical Tools**: Easier utilization of Python libraries for data analysis.
- **Resource Optimization**: Ability to deploy lighter containers, potentially reducing infrastructure costs.

### Negative

- **Migration Costs**: Time and resources required to port existing code from Java to Python.
- **Risk of Errors**: Potential introduction of new bugs during the migration process.
- **Training**: Possible need for team training in areas specific to the new technology stack.

## Alternatives

- **Continuing with Java**: Maintain and optimize the existing service in Java.
- **Modernization within Java**: Utilize newer libraries or frameworks in Java to improve asynchronous task handling.
- **Hybrid Approach**: Implement new functionalities in Python while retaining existing Java components.

## Next Steps

- **Team Discussion**: Review the proposal in a team meeting and gather feedback.
- **Feasibility Analysis**: Conduct a detailed cost-benefit analysis of the migration.
- **Prototype Evaluation**: Assess the created prototype to identify potential challenges and validate the proposed architecture.
- **Decision Making**: Based on the collected information, make a final decision on whether to proceed with the migration.

## Summary

We have presented a proposal to change the implementation technology of the Metrics service from Java to Python, motivated by the need to streamline the development process, better align with the team's expertise, and utilize tools more suitable for asynchronous task processing. A prototype has been created and discussed, with optimistic feedback from the team leading to this ADR. Before making a final decision, further analysis and team discussions are necessary to ensure that the benefits outweigh the potential costs and risks.