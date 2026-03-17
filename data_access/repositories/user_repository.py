from sqlalchemy.orm import Session
from data_access.models.user import User
from data_access.interfaces.user_repository_interface import UserRepositoryInterface

class UserRepository(UserRepositoryInterface):

    def __init__(self, session: Session):
        self.session = session

    def get_or_create(self, name, email):

        user = self.session.query(User).filter_by(email=email).first()

        if not user:
            user = User(name=name, email=email)
            self.session.add(user)
            self.session.flush()

        return user