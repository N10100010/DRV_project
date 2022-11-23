import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

# logging stuff
import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

# In-memory
# engine = create_engine("sqlite:///:memory:", echo=True)

# sqlite file relative path
engine = create_engine("sqlite:///foo.sqlite", echo=True)
Session = sessionmaker(bind=engine)

# connect will actually establish a connection or create/load the sqlite file
# engine.connect()

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
        return f"<User(name={self.name}, fullname={self.fullname}, nickname={self.nickname})>"

# create all tables (init) if they don't exist
Base.metadata.create_all(engine, checkfirst=True)

# instantiate a User
ed_user = User(name="ed", fullname="Ed Jones", nickname="edsnickname")
ed_user.name
ed_user.nickname
str(ed_user.id)

session = Session()
session.add(ed_user)

session.commit()


# queries ...
for instance in session.query(User).order_by(User.id):
    print(instance.name, instance.fullname)

ed_user = session.query(User).filter(User.name == "ed").first()

# edit data
ed_user.nickname = "ed-1337"

# commit (see https://stackoverflow.com/a/26920108)
# avoid race conditions (when incrementing numbers) with this approach: https://stackoverflow.com/a/2334917
session.commit()

if __name__ == '__main__':
    print("-"*100, "Init DB")