from __future__ import annotations
import importlib.util, sys
from pathlib import Path
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# ────────────────────────────────────────────────────────────────
# Ścieżka do katalogu projektu i pliku z modelami
PROJECT_DIR = Path(__file__).resolve().parents[1]  # → .../Intro/2
MODELS_PATH = PROJECT_DIR / "V.py"
MODULE_NAME = MODELS_PATH.stem  # czyli "V"

# Dynamiczny import V.py z rejestracją w sys.modules (ważne!)
spec = importlib.util.spec_from_file_location(MODULE_NAME, str(MODELS_PATH))
if spec is None or spec.loader is None:
    raise RuntimeError(f"Nie mogę załadować spec dla {MODELS_PATH}")
V = importlib.util.module_from_spec(spec)
sys.modules[MODULE_NAME] = V
spec.loader.exec_module(V)  # type: ignore

Base = V.Base
# ────────────────────────────────────────────────────────────────

config = context.config
db_path = (PROJECT_DIR / "experiments.db").as_posix()
config.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# ────────────────────────────────────────────────────────────────
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
        render_as_batch=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            render_as_batch=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
