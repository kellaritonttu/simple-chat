import asyncio
import json
from typing import List


class MessageBroadcaster:
    def __init__(self):
        self._queues: List[asyncio.Queue] = []

    def subscribe(self) -> asyncio.Queue:
        queue = asyncio.Queue()
        self._queues.append(queue)
        return queue

    def unsubscribe(self, queue: asyncio.Queue) -> None:
        if queue in self._queues:
            self._queues.remove(queue)

    async def publish(self, event: str, data: dict) -> None:
        message = f"event: {event}\ndata: {json.dumps(data)}\n\n"
        dead: List[asyncio.Queue] = []
        for queue in self._queues:
            try:
                queue.put_nowait(message)
            except Exception:
                dead.append(queue)
        for q in dead:
            self.unsubscribe(q)


message_broadcaster = MessageBroadcaster()