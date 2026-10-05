# Hospital Management Microservices

Three Flask microservices run with Docker Compose.

Client -> appointment-service (5000) -> patient-service (5001) / doctor-service (5002)

## Run
    docker compose up --build -d
    docker ps
    curl http://127.0.0.1:5000/book/1/1

## Load test
    pip install requests matplotlib
    python load-test/loadtest.py
    python load-test/plot.py

Results are written to the results folder. Run the load test on your own machine to get your own measured values.
