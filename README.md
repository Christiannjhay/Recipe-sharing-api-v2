# Recipe Sharing Platform API V2

## Overview
This repository contains the implementation of a Recipe Sharing Platform API using Python and Flask, backed by an MSSQL database. The application is containerized using Docker for easy deployment.

## Quick Start

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/recipe-sharing-api.git
    cd recipe-sharing-api
    ```

2. **Build and Run Docker Containers:**
    ```bash
    docker-compose up --build
    ```

3. **Access the API:**
    Open your browser and navigate to [http://localhost:5000](http://localhost:5000)
## API Endpoints
- **POST /recipes/:** Add a new recipe.
- **GET /recipes/:** Retrieve a list of all recipes, sorted by most recent.
- **GET /recipes/<id>/:** Retrieve details of a specific recipe by its ID.
- **PUT /recipes/<id>/:** Update a specific recipe by its ID.
- **DELETE /recipes/<id>/:** Delete a specific recipe by its ID.
- **POST /recipes/<id>/ratings/:** Rate a specific recipe.
- **POST /recipes/<id>/comments/:** Comment on a specific recipe.
- **GET /recipes/<id>/comments/:** Retrieve all comments for a specific recipe.
