from app.application.entities import User, UserScore
from app.application.interfaces import IUserRepository, IUserScoreRepository
from app.application.exceptions import UserNotFoundError, UserScoreNotFoundError, ValidationError


class UserService:
    """Сервис для работы с пользователями"""
    
    def __init__(
        self,
        user_repo: IUserRepository,
        user_score_repo: IUserScoreRepository
    ):
        self.user_repo = user_repo
        self.user_score_repo = user_score_repo
    
    async def get_user_by_id(self, user_id: int) -> User:
        """Получить пользователя по ID"""
        try:
            user = await self.user_repo.get_by_id(user_id)
            if not user:
                raise UserNotFoundError(user_id=user_id)
            return user
        except Exception as e:
            if isinstance(e, UserNotFoundError):
                raise
            raise ValidationError(field="user_id", error=str(e))
    
    async def get_user_by_username(self, username: str) -> User:
        """Получить пользователя по username"""
        try:
            user = await self.user_repo.get_by_username(username)
            if not user:
                raise UserNotFoundError(message=f"Пользователь {username} не найден")
            return user
        except Exception as e:
            if isinstance(e, UserNotFoundError):
                raise
            raise ValidationError(field="username", error=str(e))
    
    async def create_user(self, username: str, email: str) -> User:
        """Создать нового пользователя"""
        try:
            user = User(username=username, email=email)
            return await self.user_repo.create(user)
        except Exception as e:
            raise ValidationError(field="user_data", error=str(e))
    
    async def get_user_score(self, user_id: int) -> UserScore:
        """Получить счет пользователя"""
        try:
            # Сначала проверяем, что пользователь существует
            await self.get_user_by_id(user_id)
            
            user_score = await self.user_score_repo.get_by_user_id(user_id)
            if not user_score:
                raise UserScoreNotFoundError(user_id=user_id)
            return user_score
        except Exception as e:
            if isinstance(e, (UserNotFoundError, UserScoreNotFoundError)):
                raise
            raise ValidationError(field="user_score", error=str(e)) 