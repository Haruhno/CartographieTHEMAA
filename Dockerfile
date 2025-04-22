FROM python:3.12-slim

WORKDIR /app

# Installation optimisée des dépendances
RUN apt-get update && \
    apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Installation groupée des dépendances Python
RUN pip install --no-cache-dir \
    Flask==3.0.2 \
    Flask-SQLAlchemy==3.1.1 \
    pymysql==1.1.0 \
    python-dotenv==1.0.0 \
    mysqlclient==2.2.1 \
    gunicorn==21.2.0  # Pour la production

COPY . /app

EXPOSE 5000

CMD ["python", "app/app.py"]