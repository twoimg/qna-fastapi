from sqlalchemy import create_engine
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker

from app.core.config import Settings, settings

def build_database_url_from_config(_config: Settings) -> str:
    """
    Build a database URL from the configuration.

    Parameters:
        _config: Config
            The configuration to build the database URL from.

    Returns:
        str: The sqlalchemy database URL.
    """
    pass
    return (
        f"postgresql://{_config.POSTGRES_USER}:{_config.POSTGRES_PASSWORD}"
        f"@{_config.POSTGRES_SERVER}:{_config.POSTGRES_PORT}"
        f"/{_config.POSTGRES_DB}"
    )

def get_engine(database_url: str, echo=False) -> Engine:
    """
    Create and return an sqlalchemy engine.

    Parameters:
        database_url: str
            The database URL to create the engine with.
        echo: bool
            Whether to echo the SQL statements to the console.

    Returns:
        Engine: The sqlalchemy engine.
    """
    engine = create_engine(database_url, echo=echo)
    return engine

def get_local_session(database_url: str):
    """
    Create and return a local session.

    Parameters:
        database_url: str
            The database URL to create the session with.

    Returns:
        Session: The sqlalchemy session.
    """
    engine = get_engine(database_url, echo=True)
    session = sessionmaker(bind=engine)
    return session


SQLALCHEMY_DATABASE_URL = build_database_url_from_config(settings)