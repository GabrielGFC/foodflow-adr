#!/bin/bash
# Deploy manual via SSH — estado atual da FoodFlow (IaaS manual).
# Roda no VPS após `ssh foodflow@vps`.
# Tempo médio: ~30 min de downtime/semana (problema documentado no ADR-01).

set -e

APP_DIR=/opt/foodflow
VENV=$APP_DIR/venv

echo "[1/6] Parando gunicorn..."
sudo systemctl stop foodflow

echo "[2/6] git pull..."
cd $APP_DIR && git pull origin main

echo "[3/6] Atualizando dependências..."
$VENV/bin/pip install -r requirements.txt

echo "[4/6] Migrando banco..."
$VENV/bin/python manage.py migrate --noinput

echo "[5/6] Coletando estáticos..."
$VENV/bin/python manage.py collectstatic --noinput

echo "[6/6] Reiniciando gunicorn..."
sudo systemctl start foodflow

echo "Deploy concluído."
