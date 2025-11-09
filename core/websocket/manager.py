import logging

from fastapi import WebSocket

logger = logging.Logger(__name__)
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        logger.info(f"Connecting to websocket: {websocket}")
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        logger.info(f"Disconeccting websocket: {websocket}")
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        try:
            await websocket.close()
        except:
            pass

    async def send_personal_message(self, message, websocket: WebSocket):
        logger.info(f"Websocket: {websocket} sending message: {message}")
        try:
            await websocket.send_json(message)
        except:
            await self.disconnect(websocket)