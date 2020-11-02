from sqlalchemy import Column, String, Integer, ForeignKey, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from commons.config import POSTGRES_PASSWORD, DB_SCHEMA_NAME

Base = declarative_base()
# todo: pass server address as parameter, not 127.0.0.1


class User(Base):
    __tablename__= 'user'
#    __table_args__ = {"schema": DB_SCHEMA_NAME}
    id = Column(Integer, primary_key=True,autoincrement=True)
    uuid = Column(String, unique=True)
    nickname = Column(String, unique=True, nullable=False, comment='also used as login')
    firstname = Column(String)
    lastname = Column(String)
    middlename = Column(String)
    email = Column(String)
    description = Column(String, comment='Any additional info')

    projects = relationship('Project', secondary='user_projects')
    roles = relationship('Role', secondary = 'user_roles')

class Project(Base):
    __tablename__ = 'project'
#    __table_args__ = {"schema": DB_SCHEMA_NAME}
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, unique=True)
    description = Column(String)
    users = relationship('User', secondary = 'user_projects' )

class UserProjects(Base):
    __tablename__ = 'user_projects'
#    __table_args__ = {"schema": DB_SCHEMA_NAME}
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    project_id = Column(Integer, ForeignKey('project.id'), primary_key=True)

class Role(Base):
    __tablename__ = 'role'
    id = Column(String, primary_key=True)
    description = Column(String)
    user = relationship('User', secondary = 'user_roles' )

class UserRoles(Base):
    __tablename__ = 'user_roles'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    role_id = Column(String, ForeignKey('role.id'), primary_key=True)


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

# todo: remove duplications of code
def create_file_entity(image:Image):
    engine = create_engine('postgresql://postgres:%s@127.0.0.1/postgres' % POSTGRES_PASSWORD)
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()
    s.add(image)
    s.commit()

def create_user_entity(user: User, user_roles_str):
    engine = create_engine('postgresql://postgres:%s@127.0.0.1/postgres' % POSTGRES_PASSWORD)
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()
    try:
        # https://github.com/sqlalchemy/sqlalchemy/wiki/UniqueObjectValidatedOnPending
        # todo: this way of creating ref is weird, but what's offered by SQLAlchemy seems even more weird (link above) :/
        existing_roles = s.query(Role).filter(Role.id.in_(user_roles_str)).all()
        if (len(existing_roles)!=len(user_roles_str)):
            return
        user.roles=existing_roles
        s.add(user)
        s.commit()
        return
    except IntegrityError as err:
        return #todo: handle duplicate record properly (now swallowed, to pass to ftp_creation for debug)

def create_project_entity(project: Project, users_str):
    engine = create_engine('postgresql://postgres:%s@127.0.0.1/postgres' % POSTGRES_PASSWORD)
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()
    user_str = users_str
    existing_users = s.query(User).filter(User.nickname.in_(user_str)).all()
    if len(existing_users)!=len(user_str):
        return -1
    project.users=existing_users
    try:
        s.add(project)
        s.commit()
    except IntegrityError as err:
        pass #todo: handle duplicate record properly (now swallowed, to pass to ftp_creation for debug)
    new_record = s.query(Project).filter(Project.uuid==project.uuid).all()[0]
    return new_record.id

# creating DB (added to global scope, but even called from various places will be executed only once
# on table creation
def insert_initial_roles(target, connection, **kw):
    connection.execute(target.insert(),
                       {'id': 'user', 'description':'user having access to one or several projects'},
                       {'id': 'admin', 'description': 'have access to all projects'})
event.listen(Role.__table__, 'after_create', insert_initial_roles)