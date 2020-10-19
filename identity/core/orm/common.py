from sqlalchemy import Column, String, Enum, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from uuid import UUID, uuid4
from core.orm.db import Base
from core.api_models.common import RoleEnum, TaskStatusEnum
from datetime import datetime

user_roles = Table('user_roles', Base.metadata,
    Column('user_id', UUID, ForeignKey('user.id')),
    Column('role_id', Enum, ForeignKey('role.role'))
)
user_projects = Table('user_projects', Base.metadata,
    Column('user_id', UUID, ForeignKey('user.id')),
    Column('project_id', UUID, ForeignKey('project.id'))
)

class UserORM(Base):
    __tablename__ = "user"
    id = Column(UUID, primary_key=True, index=True, default=uuid4())
    nick_name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    sur_name = Column(String)
    roles = relationship(
        "RoleORM",
        secondary=user_roles,
        back_populates="users")
    projects = relationship(
        "ProjectORM",
        secondary=user_roles,
        back_populates="users")

class RoleORM(Base):
    __tablename__ = "role"
    role = Column(Enum(RoleEnum), primary_key=True)
    users = relationship(
        "UserORM",
        secondary=user_roles,
        back_populates="roles")

class ProjectORM(Base):
    __tablename__ = "project"
    id = Column(UUID, primary_key=True, index=True, default=uuid4())
    date = Column(DateTime, default=datetime.now())
    description = Column(String)
    users = relationship(
        "UserORM",
        secondary=user_projects,
        back_populates="projects")
    files = relationship("FileORM", cascade="all, delete")
    tasks = relationship("TaskORM", cascade="all, delete")

class FileORM(Base):
    id = Column(UUID, primary_key=True, index=True, default=uuid4())
    project_id = Column(Integer, ForeignKey('project.id'))

class TaskORM(Base):
    id = Column(UUID, primary_key=True, index=True, default=uuid4())
    status = Column(Enum(TaskStatusEnum))
    project_id = Column(Integer, ForeignKey('project.id'))


