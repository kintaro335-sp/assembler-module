#!/usr/bin/bash
uvicorn --host 0.0.0.0 --port 5050 --reload "main_server:app"
