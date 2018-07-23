from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    engine = create_engine('sqlite:///users.db', pool_recycle=3600)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
