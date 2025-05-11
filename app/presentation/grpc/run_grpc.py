from app.presentation.grpc.grpc_server import serve_grpc_forever
import logging

logging.basicConfig(level=logging.INFO)
if __name__ == "__main__":
    serve_grpc_forever()
