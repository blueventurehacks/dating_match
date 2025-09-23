## How to Run
1. start the server
```
nohup python3 -m server_a2a.main > server.log 2>&1 &
echo $! > server.pid
```
2. test run a client
```
python client_a2a/simple_messaging.py
```
3. stop the server
```
kill $(cat server.pid) && rm server.pid server.log
```
