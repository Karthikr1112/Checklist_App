# Cluster Manager Audit (Django + MySQL)

Web application that digitises the Cluster Manager Store Visit Checklist
(`Cluster_Manager_Checklist_V1.xlsx`).

## Architecture

```
config/                 # split settings (base / dev / prod), urls, wsgi/asgi
apps/
  core/                 # BaseModel (UUID + timestamps + soft-delete), perms
  accounts/             # custom User (email login) + roles
  stores/               # Store catalogue + role-based selectors
  checklists/           # Templates / Sections / Questions + seed command
  visits/               # Visit, VisitResponse, ResponsePhoto, services, signals
  actions/              # ActionItem (owner / due / status / closure)
  dashboard/            # aggregated KPIs (compliance %, open actions, …)
templates/              # Bootstrap 5 server-rendered UI
static/, media/
```

Architectural conventions:

- **Service layer** (`services.py`) holds write/business logic – views stay thin.
- **Selector layer** (`selectors.py`) holds read queries with role-based scoping.
- **`BaseModel`** = UUID PK + `created_at` / `updated_at` + soft delete.
- **Custom user model** (`accounts.User`) with `Role` enum (Admin / ClusterManager / StoreManager / Owner).
- **Signals** auto-recompute Visit compliance when responses change.
- **Settings split**: `config.settings.base|dev|prod`, all secrets via `.env`.
- **Scoring**: Yes = 1, No = 0, NA excluded — matches the Excel spec.

## Setup

```bash
# 1. Create venv
python3 -m venv .venv
source .venv/bin/activate

# 2. Install deps
pip install -r requirements.txt

# 3. Configure env
cp .env.example .env
# edit .env: set DJANGO_SECRET_KEY, DB_NAME/USER/PASSWORD

# 4. Create MySQL database
mysql -uroot -p -e "CREATE DATABASE cluster_audit CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 5. Migrate + seed + create superuser
python manage.py makemigrations
python manage.py migrate
python manage.py seed_checklist
python manage.py createsuperuser

# 6. Run
python manage.py runserver
```

Open http://127.0.0.1:8000/ — log in with the superuser you just created.

## Workflow

1. **Admin** adds users (Cluster Managers, Store Managers) and Stores, assigning a Cluster Manager and Store Manager to each.
2. **Cluster Manager** clicks **Start Visit**, picks a Store + Audit Type + Date.
3. App pre-creates a `VisitResponse` for every CM-001…CM-040 question.
4. CM fills Yes/No/NA, daily-update observations, attaches photos, raises Action items.
5. CM submits the visit → Admin reviews and **Approves**.
6. **Dashboard** shows compliance %, open actions, pending approvals.
7. Action owners log in, see **My Actions**, close them with a note.

## Roles

| Role             | Can do                                                      |
| ---------------- | ----------------------------------------------------------- |
| `ADMIN`          | Everything: CRUD users / stores / templates, approve visits |
| `CLUSTER_MANAGER`| Start / fill / submit visits for stores assigned to them    |
| `STORE_MANAGER`  | View visits + actions for their store                       |
| `OWNER`          | Sees and closes assigned actions                            |

## Production checklist

- Set `DJANGO_SETTINGS_MODULE=config.settings.prod`
- Strong `DJANGO_SECRET_KEY`, real `DJANGO_ALLOWED_HOSTS` & `CSRF_TRUSTED_ORIGINS`
- MySQL behind TLS, daily backups
- Serve via `gunicorn` behind nginx; static files via `whitenoise`/CDN
- Move `MEDIA_ROOT` to S3 (swap the `STORAGES` backend)
