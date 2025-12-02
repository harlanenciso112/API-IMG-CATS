# API Gatos

Servicio backend que obtiene imagenes aleatorias de gatos desde [cataas.com](https://cataas.com) y las almacena en una base de datos SQLite.

## Ejecutar con Docker Compose

1. Clona el repositorio:
```bash
git clone https://github.com/harlanenciso/api-gatos.git
cd api-gatos
```

2. Ejecuta el script:

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

**Windows (Git Bash o WSL):**
```bash
bash run.sh
```

La aplicación estará disponible en `http://localhost:5000`

## Endpoints

| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `/api/cat` | Obtiene una imagen aleatoria de gato y la guarda en formato binario en la base de datos |
| GET | `/api/count` | Devuelve el total de imagenes unicas almacenadas |
| GET | `/api/image/<id>` | Devuelve los datos de una imagen por ID |
| GET | `/api/images` | Lista todas las imagenes guardadas |
| DELETE | `/api/delete/<id>` | Elimina una imagen por ID |

## Ejemplos de uso

Obtener imagen de gato:
```
http://localhost:5000/api/cat
```

Ver cantidad de imagenes:
```
http://localhost:5000/api/count
```

## Docker Hub

Imagen disponible en: [harlanenciso/api-gatos](https://hub.docker.com/r/harlanenciso/api-gatos)

```bash
docker pull harlanenciso/api-gatos:latest
```

## Ejecutar pruebas

```bash
pip install -r requirements.txt
python -m unittest discover -s tests
```