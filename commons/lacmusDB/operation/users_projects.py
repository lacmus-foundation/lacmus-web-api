from commons.lacmusDB.db_definition import User, Role, Project
from commons.lacmusDB.db_definition import get_session
import logging

def create_user_entity(user: User, user_roles_str):
    s = get_session()
    try:
        logging.info("Creating user %s with roles %s"%(user.nickname,','.join(user_roles_str)))
        existing_roles = s.query(Role).filter(Role.id.in_(user_roles_str)).all()
        if (len(existing_roles)!=len(user_roles_str)):
            logging.error("Cann't create user, as some roles are not in DB. ")
            logging.error("Request roles:[%s] DB roles:[%s]" % (', '.join(user_roles_str),
            ', '.join([r.id for r in existing_roles])))
            raise ValueError("Invalid roles")
        user.roles=existing_roles
        s.add(user)
        s.commit()
        return
    except Exception as err:
        logging.error("Exception while creating user", exc_info=True)
        raise

def check_user_exists(login: str):
    s=get_session()
    return s.query(User).filter(User.nickname == login).all()


def create_project_entity(project: Project, users_str):
    logging.info("Creating project")
    s = get_session()
    user_str = users_str
    existing_users = s.query(User).filter(User.nickname.in_(user_str)).all()
    if len(existing_users)!=len(user_str):
        logging.error("Cann't create project, as some user are not in DB. ")
        logging.error("Request users:[%s] DB users:[%s]"%(', '.join(users_str),
            ', '.join([u.nickname for u in existing_users])))
        return -1
    project.users=existing_users
    try:
        s.add(project)
        s.commit()
        new_record = s.query(Project).filter(Project.uuid == project.uuid).all()[0]
        logging.info("project created with id=%i" % new_record.id)
        return new_record.id
    except Exception as err:
        logging.error("Exception while creating project", exc_info=True)
        return -1


def get_active_projects() -> [Project]:
    try:
        logging.info("Getting project list from DB")
        s = get_session()
        return s.query(Project).filter(Project.end_date == None).all()
    except Exception as e:
        logging.error("Exception while getting projects", exc_info=True)