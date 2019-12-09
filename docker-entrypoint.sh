#!/bin/bash
gunicorn --bind=0.0.0.0:8118 --worker-class aiohttp.GunicornWebWorker main:create_app
