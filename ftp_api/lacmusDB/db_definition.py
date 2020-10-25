from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import POSTGRES_PASSWORD, DB_SCHEMA_NAME

Base = declarative_base()


class User(Base):
    __tablename__= 'user'
#    __table_args__ = {"schema": DB_SCHEMA_NAME}
    id = Column(Integer, primary_key=True,autoincrement=True)
    nickname = Column(String, unique=True,comment='also used as login')
    projects = relationship('Project', secondary='users_projects')

class Project(Base):
    __tablename__ = 'project'
#    __table_args__ = {"schema": DB_SCHEMA_NAME}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String,  unique=True)
    description = Column(String)
    users = relationship('User', secondary = 'users_projects' )

class UserProjects(Base):
    __tablename__ = 'users_projects'
#    __table_args__ = {"schema": DB_SCHEMA_NAME}
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    project_id = Column(Integer, ForeignKey('project.id'), primary_key=True)

class Image(Base):
    __tablename__ = 'image'
    #    __table_args__ = {"schema": DB_SCHEMA_NAME}
    id = Column(Integer, primary_key=True, autoincrement=True)
    hash = Column(String, unique=True)
    filename = Column(String)
    project_id = Column(Integer, ForeignKey('project.id'))
    project = relationship(Project, backref=backref('project', uselist=True))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref=backref('user',uselist=True))


def init_db():
    engine = create_engine('postgresql://postgres:%s@127.0.0.1/postgres'%POSTGRES_PASSWORD)
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine) # docs says will no re-create tables, once exists

def create_file_entity(image:Image):
    engine = create_engine('postgresql://postgres:%s@127.0.0.1/postgres' % POSTGRES_PASSWORD)
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()
    s.add(image)
    s.commit()

