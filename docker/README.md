
This repository contains a `docker-compose.yml` file to set up a PostgreSQL database and a pgAdmin instance using Docker Compose. Additionally, it includes a Python script to ingest data into the PostgreSQL database. Below is a brief explanation of the services and configurations provided.

## Docker Compose File

### Version

The `version` used in this file is `3.8`, which is compatible with modern Docker Compose features.

### Services

#### 1. **PostgreSQL**

- **Image**: Uses the official `postgres:13` image.
- **Container Name**: `pg-database`.
- **Environment Variables**:
  - `POSTGRES_USER`: The username for the PostgreSQL database, set to `root`.
  - `POSTGRES_PASSWORD`: The password for the PostgreSQL database, set to `root`.
  - `POSTGRES_DB`: The name of the default database, set to `ny_taxi`.
- **Volumes**: Maps the local directory `./ny_taxi_postgres_data` to the container directory `/var/lib/postgresql/data` for persistent storage.
- **Ports**: Exposes PostgreSQL on port `5432` of the host machine.
- **Networks**: Connected to the custom bridge network `pg-network`.

#### 2. **pgAdmin**

- **Image**: Uses the official `dpage/pgadmin4` image.
- **Container Name**: `pgadmin-2`.
- **Environment Variables**:
  - `PGADMIN_DEFAULT_EMAIL`: The default email for pgAdmin login, set to `admin@admin.com`.
  - `PGADMIN_DEFAULT_PASSWORD`: The default password for pgAdmin login, set to `root`.
- **Ports**: Exposes pgAdmin on port `8080` of the host machine.
- **Networks**: Connected to the custom bridge network `pg-network`.

### Networks

- **pg-network**: A custom bridge network to enable communication between the PostgreSQL and pgAdmin containers.

## Python Script for Data Ingestion

The project also includes a Python script, `ingest_data.py`, which automates the ingestion of CSV data into the PostgreSQL database. Below is an overview of its functionality:

- **Purpose**: Downloads a CSV file from a specified URL and ingests its content into a PostgreSQL database.
- **Features**:
  - Downloads the file using `wget`.
  - Parses the CSV file into a Pandas DataFrame.
  - Adjusts datetime fields to ensure proper data types.
  - Creates a table in the PostgreSQL database using SQLAlchemy if it doesn't already exist.
  - Inserts the data into the specified table, replacing existing data if necessary.
- **Usage**: The script accepts command-line arguments. Build the image and run the container with following parameters.

    ```bash
    docker build -t taxi_ingest:v001 .
    URL=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2021-01.csv.gz
    docker run -it --network=pg-network taxi_ingest:v001 --user=root   --password=root   --host=pg-database   --port=5432   --db=ny_taxi   --table_name=green_taxi_data   --url=${URL}

## How to Use

1. **Clone the Repository**:

   ```bash
   docker-compose up -d  # to start containers
   docker-compose down # to stop containers