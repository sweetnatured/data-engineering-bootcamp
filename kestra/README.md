# Kestra Setup with Docker

## Overview
This guide provides step-by-step instructions for setting up Kestra with PostgreSQL and pgAdmin using Docker and Docker Compose.

## Prerequisites
- Docker installed on your system
- Docker Compose installed

## Setup Instructions

### Step 1: Start PostgreSQL and pgAdmin Containers
Run the following command to start the PostgreSQL database and pgAdmin containers within the `pg-network`:

```sh
docker-compose up -d
```

Ensure that the network name is `pg-network` as defined in the Docker Compose file.

### Step 2: Run Kestra
Execute the following command to run Kestra within the same network:

```sh
docker run --pull=always --rm -it \
  -p 8080:8080 \
  --network pg-network \
  --user=root \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /tmp:/tmp \
  kestra/kestra:latest server local
```

This will start Kestra and bind it to port `8080`.

### Step 3: Configure Kestra Plugin Defaults
Modify the Kestra configuration to connect to the PostgreSQL database. Update the `pluginDefaults` section as follows:

```yaml
pluginDefaults:
  - type: io.kestra.plugin.jdbc.postgresql
    values:
      url: jdbc:postgresql://pg-database:5432/your_database_name
      username: your_db_username
      password: your_db_password
```

Replace:
- `pg-database` with the actual container name for your PostgreSQL database.
- `your_database_name` with the database name specified in your Docker Compose file.
- `your_db_username` and `your_db_password` with the credentials specified in your Docker Compose file.

### Step 4: Verify the Setup
Once everything is configured, Kestra should be running and connected to your PostgreSQL database. You can access the Kestra UI at:

```
http://localhost:8080
```

## Notes
- Ensure that your PostgreSQL and pgAdmin containers are running before starting Kestra.
- If you encounter connection issues, check the container logs using:
  ```sh
  docker logs <container_name>
  ```
- Update the database credentials accordingly in both the `docker-compose.yml` and Kestra configuration.

Now, everything should be set up correctly!

