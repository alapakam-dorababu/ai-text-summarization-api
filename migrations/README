# Alembic Setup Guide for SQLModel

This guide will help you set up and configure Alembic for handling database migrations in your SQLModel-based project.

## Step 1: Setting Up Your Environment

First, create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

Then install the required dependencies:

```bash
pip install sqlmodel alembic
```

---

## Step 2: Defining Your SQLModel Models

Define your database models using SQLModel. For example:

```python
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    email: str
```

---

## Step 3: Initializing Alembic

Initialize Alembic in your project directory:

```bash
alembic init migrations
```

This creates a `migrations/` folder with the necessary Alembic configuration files.

---

## Step 4: Configuring Alembic

### 4.1 Update `alembic.ini`

Edit `alembic.ini` to set your database connection string:

```
sqlalchemy.url = sqlite:///database.db  # Change this based on your database
```

For PostgreSQL:

```
sqlalchemy.url = postgresql://user:password@localhost/dbname
```

For MySQL:

```
sqlalchemy.url = mysql+pymysql://user:password@localhost/dbname
```

### 4.2 Modify `migrations/env.py`

Edit `migrations/env.py` to include SQLModel:

```python
from sqlmodel import SQLModel
from alembic import context
from models import *  # Import your SQLModel models here

target_metadata = SQLModel.metadata
```

---

## Step 5: Modifying the Migration Script Template

Edit `migrations/script.py.mako` and add the following import at the top:

```python
import sqlmodel
```

This ensures that SQLModel types are correctly recognized during migrations.

---

## Step 6: Creating and Applying Migrations

### 6.1 Generate a Migration Script

Whenever you modify your models, create a migration script:

```bash
alembic revision --autogenerate -m "Initial migration"
```

### 6.2 Apply Migrations to the Database

Run the following command to apply the migration:

```bash
alembic upgrade head
```

---

## Step 7: Rolling Back Migrations

If needed, you can revert a migration using:

```bash
alembic downgrade -1
```

---

## Additional Notes

- Make sure all models are imported in `migrations/env.py`.
- Always review the generated migration scripts before running them.
- Keep `alembic.ini` updated with the correct database URL.

With this setup, you can now manage database migrations effectively in your SQLModel-based project!

