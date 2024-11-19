#Inteprete  = control+p > Python Selected 

# FastAPI Project Setup

## 1. Activar el entorno de conda llamado 'fastapi'
```bash
conda activate fastapi
```
#2. Instalar los paquetes FastAPI y Uvicorn usando pip en el entorno de conda
```bash
pip install fastapi
pip install uvicorn

``` 
#Instalar el paquete 
```bash
pip install pymysql
pip install sqlalchemy
pip install cryptography

```


#Ejecutar la aplicación FastAPI usando Uvicorn
```bash
uvicorn main:app --reload
```
#3. Abrir el navegador y visitar la URL http://
```bash
http://127.0.0.1:8000/docs
```


#configuracion de requirements.txt
```
fastapi
uvicorn[standard]
pymysql
sqlalchemy
cryptography
psycopg2-binary
bcrypt
```