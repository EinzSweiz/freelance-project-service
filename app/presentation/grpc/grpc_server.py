# app/presentation/grpc/grpc_server.py
import grpc
import asyncio
from app.infrastructure.db.db_session import AsyncSessionLocal
from app.infrastructure.db.postgres_project_repository import PostgresqlProjectRepository
from app.infrastructure.logger.logger import get_logger
from app.generated.project import project_pb2_grpc
from app.infrastructure.grpc.project_server import ProjectServiceHandler
import asyncpg
async def wait_for_db():
    while True:
        try:
            conn = await asyncpg.connect(dsn="postgresql://postgres:postgres@db:5432/projects_db")
            await conn.close()
            print("✅ Database is ready!")
            break
        except Exception as e:
            print("⏳ Waiting for DB...", str(e))
            await asyncio.sleep(1)
            
async def grpc_main():
    await wait_for_db()
    server = grpc.aio.server()
    logger = get_logger("grpc")

    async with AsyncSessionLocal() as session:
        repo = PostgresqlProjectRepository(session=session, logger=logger)
        service = ProjectServiceHandler(repo, logger)

        project_pb2_grpc.add_ProjectServiceServicer_to_server(service, server)
        server.add_insecure_port("[::]:50051")

        await server.start()
        logger.info("🔥 gRPC server started on port 50051")
        await server.wait_for_termination()


def serve_grpc_forever():
    asyncio.run(grpc_main())
