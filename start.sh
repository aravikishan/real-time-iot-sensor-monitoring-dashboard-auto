#!/bin/bash
set -e
echo "Starting Real-Time IoT Sensor Monitoring Dashboard..."
uvicorn app:app --host 0.0.0.0 --port 9130 --workers 1
