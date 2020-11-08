from commons.lacmusDB.db_definition import User, Role, Project
from commons.lacmusDB.db_definition import get_session
from sqlalchemy.exc import IntegrityError


def create_user_entity(user: User, user_roles_str):
    s = get_session()
    try:
        # https://github.com/sqlalchemy/sqlalchemy/wiki/UniqueObjectValidatedOnPending
        # todo: this way of creating ref is weird, but what's offered by SQLAlchemy seems even more weird (link above) :/
        existing_roles = s.query(Role).filter(Role.id.in_(user_roles_str)).all()
        if (len(existing_roles)!=len(user_roles_str)):
            raise ValueError("Some roles are invalid")
        user.roles=existing_roles
        s.add(user)
        s.commit()
        return
    except IntegrityError as err:
        return #todo: handle duplicate record properly (now swallowed, to pass to ftp_creation for debug)



def create_project_entity(project: Project, users_str):
    s = get_session()
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