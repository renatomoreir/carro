start cmd /k "python -m src.server.server"
timeout /t 2
start cmd /k "python src/app/agent.py"
