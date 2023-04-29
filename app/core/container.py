from dependency_injector import containers, providers

from app import repository, service
from app.core.config import config
from app.core.database import Database


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1.endpoint.auth",
        ]
    )
    db = providers.Singleton(Database, db_url=config.DB_URL)

    # Base repositories
    user_repository = providers.Factory(repository.UserRepository, session_factory=db.provided.session_factory)

    # Base services
    auth_service = providers.Factory(service.AuthService, user_repository=user_repository)
    user_service = providers.Factory(service.UserService, user_repository=user_repository)

    # Integrated services
