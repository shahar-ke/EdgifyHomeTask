from asyncio import Queue, Lock

from sanic_restful_api import Resource, abort

from execution_server_lib.execution_server_sdk import ExecutionServerSDK
from models.order import Order


class OrderAPI(Resource):
    REQUESTS_BUFFER_SIZE = 10

    @classmethod
    async def post(cls, request):
        try:
            order = Order.from_json(request.json)
            if order is None:
                abort(400, 'could not fetch order from request')
            queue: Queue = request.app.requests_queue
            await queue.put(order)
            if queue.qsize() < cls.REQUESTS_BUFFER_SIZE:
                print(f'{order=}, qzize={queue.qsize()}, waiting')
                await queue.join()
            else:
                await cls.handle_buffer(request, queue)
            return order.to_json()
        except Exception as e:
            abort(500, f'error occurred during execution: {str(e)}')

    @classmethod
    async def handle_buffer(cls, request, queue):
        lock: Lock = request.app.lock
        async with lock:
            orders = list()
            while not queue.empty():
                order = await queue.get()
                orders.append(order)
            ExecutionServerSDK.execute_orders(orders)
            for _ in orders:
                queue.task_done()
