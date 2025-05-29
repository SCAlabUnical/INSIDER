# ECC Workflow API Server

A Django-based API server for executing workflow mappings using different solving strategies.

## Prerequisites

-   [Docker](https://docs.docker.com/get-docker/)
-   [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

### Clone the Repository

```bash
git https://github.com/AleandroPresta/ecc-workflow-api-server
cd ecc-workflow-api-server
```

### Build and Run with Docker Compose

Create the network:

```bash
docker network create ecc-workflow-network
```

Build and start the application:

```bash
docker compose up --build
```

The server will be available at `http://localhost:8000`

To run it in detached mode:

```bash
docker compose up --build -d
```

To stop the server:

```bash
docker compose down
```

## API Endpoints

The API provides the following endpoints:

-   `GET /api/v1/` - Basic health check endpoint
-   `POST /api/v1/solve/linear` - Solve workflows using the linear strategy
-   `POST /api/v1/solve/llm/<model_id>` - Solve workflows using LLM-based strategy
