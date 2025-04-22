#!/bin/bash

# Run Flask (on port 5000)
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app &

# Run Streamlit (on port 8080 or $PORT)
streamlit run app/frontend/streamlit_app.py --server.port 8080 --server.address 0.0.0.0