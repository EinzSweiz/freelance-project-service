from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.infrastructure.db.db_session import get_session
from app.infrastructure.db.postgres_project_repository import PostgresqlProjectRepository
from app.infrastructure.logger.logger import get_logger
from app.domain.common.logger import AbstractLogger
from app.services.project_service import ProjectService
from app.infrastructure.kafka.kafka_producer import get_kafka_producer, KafkaProducer


def get_project_service(
    session: AsyncSession = Depends(get_session),
    logger: AbstractLogger = Depends(get_logger),
    kafka_producer: KafkaProducer = Depends(get_kafka_producer),
) -> ProjectService:
    repo = PostgresqlProjectRepository(session=session, logger=logger)
    return ProjectService(project_repo=repo, logger=logger, kafka_producer=kafka_producer)
