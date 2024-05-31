#!/bin/bash

# Ativar o ambiente Poetry
source /home/rpereira/.cache/pypoetry/virtualenvs/guiafilmestv-iy6lO39t-py3.12/bin/activate

# Iniciar o servidor FastApi com uvicorn
uvicorn app:app --host 0.0.0.0 --port 9000
