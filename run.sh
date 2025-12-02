#!/bin/bash

echo "Descargando imagen de Docker Hub..."
docker pull harlanenciso/api-gatos:latest

echo "Iniciando contenedor..."
docker-compose up -d

echo "Aplicacion corriendo en http://localhost:5000"