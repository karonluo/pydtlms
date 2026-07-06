#!/bin/bash
python3 -m uvicorn app.main_static:app --host 0.0.0.0 --port 8000