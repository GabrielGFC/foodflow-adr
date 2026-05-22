# FoodFlow — Monolito Django (estado atual)

Representação do **estado atual** da FoodFlow descrito no [ADR-01](../adrs/ADR-01-migracao-cloud.md): monolito Python/Django rodando em **1 VPS alugado (IaaS manual)** com PostgreSQL no mesmo servidor e deploy manual via SSH.

## Arquitetura atual

```
┌──────────────────────────────────────────┐
│  VPS único (IaaS manual — ~R$ 600/mês)   │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │  Django (monolito)                 │  │
│  │  ├── orders/      (app pedidos)    │  │
│  │  ├── restaurants/ (app restaurantes)│ │
│  │  └── customers/   (app clientes)   │  │
│  │  Servido por gunicorn + nginx      │  │
│  └────────────────────────────────────┘  │
│              ↕                            │
│  ┌────────────────────────────────────┐  │
│  │  PostgreSQL 14 (mesmo servidor)    │  │
│  └────────────────────────────────────┘  │
│                                          │
│  Deploy: SSH manual (~30 min downtime)   │
└──────────────────────────────────────────┘
```

## Stack

- Python 3.11 + Django 4.2
- PostgreSQL 14
- Gunicorn + Nginx (no VPS)
- Deploy via `deploy.sh` por SSH

## Apps

| App | Responsabilidade |
|-----|------------------|
| `customers` | Cadastro de clientes |
| `restaurants` | Restaurantes e itens de cardápio |
| `orders` | Pedidos e itens de pedido |

## Endpoints

```
GET  /api/customers/         → lista clientes
GET  /api/restaurants/       → lista restaurantes abertos
GET  /api/orders/            → lista pedidos
POST /api/orders/create/     → cria pedido
/admin/                      → Django admin
```

## Rodar localmente

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # ajustar DB_PASSWORD
python manage.py migrate
python manage.py runserver
```

## Deploy atual (problema documentado no ADR)

```bash
ssh foodflow@vps "cd /opt/foodflow && bash deploy.sh"
```

**Problemas:**
- 30 min de downtime semanal
- 80% CPU nos picos de fim de semana
- Sem auto-scaling
- Sem alta disponibilidade (servidor único)

→ **Migração proposta:** ver [ADR-01](../adrs/ADR-01-migracao-cloud.md) (PaaS Railway + Supabase).
