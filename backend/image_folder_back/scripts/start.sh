#!/bin/sh

uvicorn main:app --workers $UVICORN_WORKERS --host 0.0.0.0 --port $SERVER_PORT
