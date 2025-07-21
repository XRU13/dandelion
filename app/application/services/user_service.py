from sqlalchemy.exc import IntegrityError
from app.application.entities import User, UserScore
from app.application.interfaces import IUserRepository, IUserScoreRepository
from app.application.exceptions import UserNotFoundError, UserScoreNotFoundError
from app.application.exceptions import UserAlreadyExistsError

class UserService:
    """Сервис для работы с пользователями"""
    
    def __init__(
        self,
        user_repo: IUserRepository,
        user_score_repo: IUserScoreRepository
    ):
        self.user_repo = user_repo
        self.user_score_repo = user_score_repo

    async def create_user(self, username: str, email: str) -> User:
        """Создать нового пользователя"""
        try:
            new_user = User(username=username, email=email)
            return await self.user_repo.create(new_user)
        except IntegrityError:
            raise UserAlreadyExistsError(email=email)

    async def get_all_users(self) -> list[User]:
        """Получить всех пользователей"""
        return await self.user_repo.get_all()
    
    async def get_user_by_id(self, user_id: int) -> User:
        """Получить пользователя по ID"""
        user = await self.user_repo.get_by_id(user_id=user_id)
        if not user:
            raise UserNotFoundError(user_id=user_id)
        return user
    
    async def get_user_score(self, user_id: int) -> UserScore:
        """Получить счет пользователя"""
        user_score = await self.user_score_repo.get_by_user_id(user_id=user_id)
        if not user_score:
            raise UserScoreNotFoundError(user_id=user_id)
        return user_score 