from app.core.database.session import get_local_session
from app.core.database.session import SQLALCHEMY_DATABASE_URL

from typing import Generator
#from typing import Annotated
#from sqlalchemy.orm import Session

#from fastapi import Depends

def get_db() -> Generator:
    """
    Returns a generator that yields a database session.

    Yields:
        Generator: A generator that yields a database session.
    
    Raises:
        Exception: If an error occurs while getting the database session.
    """
    db = get_local_session(SQLALCHEMY_DATABASE_URL)()
    try:
        yield db
    finally:
        db.close()

##SessionDep = Annotated[Session, Depends(get_db)]