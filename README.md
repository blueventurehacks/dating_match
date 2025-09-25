## Project Name

**TODO:** Short summary/description here later --


## Prerequisites

**1. Before running the project, make sure you have the following installed:**

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

You can verify installation by running:

```bash
docker --version
docker-compose --version
```

**2. Create a local PostgreSQL database through Docker if you don't have an existing one**

Pull the latest PostgreSQL Docker image
```bash
docker pull postgres
```

Run PostgreSQL container (update with your own values):
```bash
docker run --name container_name \
-e POSTGRES_DB=database_name \
-e POSTGRES_USER=username \
-e POSTGRES_PASSWORD=password \
-p 5432:5432 \
-d postgres
```

## Running the Project

**1. Clone the repository:**

```bash
git clone https://github.com/blueventurehacks/dating_match
cd dating_match
```

**2. Configure the Backend**

In the `backend/` folder, create a `.env` file and add:

```
DATABASE_URL=postgresql+psycopg://username:password@host.docker.internal:5432/database_name
FLASK_ENV=development
GEMINI_API_KEY=your_api_key_here
```

- Replace the placeholders with your actual values
- Use `host.docker.internal` to allow backend container to connect to local PostgreSQL instance.

**3. Configure the Frontend**

In the `frontend/` folder, create a `.env` file and add:

```env
VITE_API_URL=http://localhost:5000
```

- Change the port number at the end if you manually chose a different one.

**4. Start the application with Docker Compose:**

From the root project directory, run:
```bash
docker-compose up --build
```

**5. Initialize the tables in your Docker PostgreSQL database**

After your containers are running, initialize the database tables:
```bash
docker compose exec backend flask init-db
```

**6. View the web page on:**
```
Local: http://localhost:5173/
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
