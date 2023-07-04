from sqlmodel import Session, create_engine

from models import user, role

engine = create_engine(
    "sqlite:///test.db",
    connect_args={'check_same_thread': False},
    echo=False
)

""" A function which creates all the tables defined in the models if not created"""
def create_db_and_tables():
    user.SQLModel.metadata.create_all(engine)
    role.SQLModel.metadata.create_all(engine)


"""
A reusable function which returns a session for the database. 
This session can be used to execute queries from the functions. 
"""
def get_session() -> Session:
    """Provide a transactional scope around a series of operations."""
    db = None
    try:
        db = Session(autocommit=False, autoflush=False,
                     bind=engine)  # create session from SQLModel session
        return db
    finally:
        db.close()