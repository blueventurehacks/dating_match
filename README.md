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
