# Imatge base lleugera i compatible oficialment amb Linux/ARM64
FROM python:3.11-slim

# Evita escriure arxius bytecode i buffer log a stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Creem i asseguem directori de treball
WORKDIR /app

# Copiem requeriments i instal·lem depenències
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiem la resta del projecte (respectant el config del .dockerignore)
COPY . .

# Exposem port
EXPOSE 5000

# Executem Gunicorn en lloc de Flask Development Server per a producció
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "app:app"]
