from sqlalchemy.orm import registry

# Создаем registry для императивного маппинга
mapper_registry = registry()
metadata = mapper_registry.metadata 