from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, event
from sqlalchemy import DDL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from commons.config import POSTGRES_PASSWORD, DB_SCHEMA_NAME

Base = declarative_base()
# todo: pass server address as parameter, not 127.0.0.1


class User(Base):
    __tablename__= 'user'
    # __table_args__ = {"schema": DB_SCHEMA_NAME}
    #columns
    id = Column(Integer, primary_key=True,autoincrement=True)
    uuid = Column(String, unique=True)
    nickname = Column(String, unique=True, nullable=False, comment='also used as login')
    firstname = Column(String)
    lastname = Column(String)
    middlename = Column(String)
    email = Column(String)
    description = Column(String, comment='Any additional info')
    #relations
    projects = relationship('Project', secondary='user_projects')
    roles = relationship('Role', secondary = 'user_roles')
    images = relationship('Image')

class Project(Base):
    __tablename__ = 'project'
    # __table_args__ = {"schema": DB_SCHEMA_NAME}
    #columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, unique=True)
    description = Column(String)
    #relations
    users = relationship('User', secondary = 'user_projects' )
    images = relationship('Image')

class UserProjects(Base):
    __tablename__ = 'user_projects'
    # __table_args__ = {"schema": DB_SCHEMA_NAME}
    #columns
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    project_id = Column(Integer, ForeignKey('project.id'), primary_key=True)

class Role(Base):
    __tablename__ = 'role'
    # __table_args__ = {"schema": DB_SCHEMA_NAME}
    #columns
    id = Column(String, primary_key=True)
    description = Column(String)
    #relations
    user = relationship('User', secondary = 'user_roles' )

class UserRoles(Base):
    __tablename__ = 'user_roles'
    # __table_args__ = {"schema": DB_SCHEMA_NAME}
    #columns
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    role_id = Column(String, ForeignKey('role.id'), primary_key=True)


class Image(Base):
    __tablename__ = 'image'
    # __table_args__ = {"schema": DB_SCHEMA_NAME}
    #columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    hash = Column(String, unique=True)
    filename = Column(String)
    project_id = Column(Integer, ForeignKey('project.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    #relations
    user = relationship(User, back_populates='images')
    project = relationship(Project, back_populates='images')
    annotation = relationship('ImageAnnotation')


class ImageAnnotation(Base): # table is intended to store processing results
    __tablename__ = 'image_annotation'
    # __table_args__ = {"schema": DB_SCHEMA_NAME}
    #columns
    image_id = Column(Integer, ForeignKey('image.id'), primary_key=True) # as it's 1:1, no need for own PK
    processing_start = Column(DateTime) # field says if image is taken for processing
    processing_end = Column(DateTime) # this created when image is processed
    #relations
    objects = relationship('ImageObjects')
    image = relationship('Image')

class ImageObjects(Base):
    __tablename__ = 'image_object'
    # __table_args__ = {"schema": DB_SCHEMA_NAME}
    #columns
    id =  Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(Integer, ForeignKey('image_annotation.image_id'))
    x_min = Column(Integer, nullable=False)
    y_min = Column(Integer, nullable=False)
    x_max = Column(Integer, nullable=False)
    y_max = Column(Integer, nullable=False)
    class_number = Column(Integer, nullable=False)
    class_label = Column(String)
    #relations
    annotation = relationship(ImageAnnotation, back_populates='objects' )

def get_engine():
    return create_engine('postgresql://postgres:%s@127.0.0.1/postgres' % POSTGRES_PASSWORD)

def get_session():
    engine=get_engine()
    # engine.execute("SET search_path to %s"%DB_SCHEMA_NAME)
    session = sessionmaker()
    session.configure(bind=engine)
    return session()


def init_db():
    e = get_engine()
    # e.execute(DDL("CREATE SCHEMA IF NOT EXISTS %s"%DB_SCHEMA_NAME))
    Base.metadata.create_all(e) # docs says will no re-create tables, once exists

def insert_initial_roles(target, connection, **kw):
    connection.execute(target.insert(),
                       {'id': 'user', 'description':'user having access to one or several projects'},
                       {'id': 'admin', 'description': 'have access to all projects'})
event.listen(Role.__table__, 'after_create', insert_initial_roles)

# creating DB (added to global scope, but even called from various places will be executed only once
# on table creation
init_db()

