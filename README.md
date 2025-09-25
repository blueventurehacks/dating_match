## Project Name

**TODO:** Short summary/description here later --


## Prerequisites

1. **Before running the project, make sure you have the following installed:**

- [Docker](https://docs.docker.com/get-docker/) (version __ or higher)
- [Docker Compose](https://docs.docker.com/compose/install/) (version __ or higher)

    You can verify installation by running:

    ```bash
    docker --version
    docker-compose --version
    ```

2. **Creating PostgreSQL database instructions here**
3. **Setting up the .env files in /backend**
4. **Run Docker command**

```bash
docker compose exec backend flask init-db
```

## Prerequisites without Docker

1. **Before running the project, make sure you have the following installed:**
- [PostgreSQL](https://www.postgresql.org/download/)
- [pgAdmin](https://www.pgadmin.org/download/)
- [Node.js](https://nodejs.org/en/download/)
- [nvm](https://github.com/nvm-sh/nvm)

2. **Creating PostgreSQL database**
```bash
# confirm running
pg_isready -h 127.0.0.1 -p 5432
psql -h 127.0.0.1 -U postgres -d postgres -c "select version();"

# create database
createdb -h 127.0.0.1 -U postgres -O postgres dating_db
```

Step 3 of the instructions with Docker applies here same

Step 4 of the instructions with Docker should be skipped

## Running the Project

1. **Clone the repository:**

```bash
git clone https://github.com/blueventurehacks/dating_match
```

2. **Navigate into the project directory:**
```bash
cd dating_match
```

3. **Start the application using Docker Compose:**
```bash
docker-compose up --build
```

4. **View the web page on:**
```
Local: http://localhost:5173/
```

## Running the Project without Docker

Step 1 and 2 of the instructions with Docker apply here as well

3. **Set up backend**
```bash
# initialize database
uv run flask --app backend.app init-db

# starting server and health check
uv run flask --app backend.app run --host 127.0.0.1 --port 5000
curl http://127.0.0.1:5000/health/db
```

4. **Set up frontend**
```bash
# switch to the frontend directory
cd frontend

# use Node version from .nvmrc (requires nvm or fnm)
nvm install
nvm use

# clean install to avoid optional deps issues
rm -rf node_modules package-lock.json
npm install

# start Vite dev server
npm run dev
# Visit: http://localhost:5173/
```

## Running Agent-to-Agent
1. start the server
```
nohup python3 -m server_a2a.main > server.log 2>&1 &
echo $! > server.pid
tail -f server.log
```
2. test run a client
```
python client_a2a/simple_messaging.py
```
3. stop the server
```
pgrep -af "server_a2a.main" | awk '{print $1}' | xargs -r kill
```
