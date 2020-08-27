from asyncio import Queue, Lock

from sanic import Sanic
from sanic_restful_api import Api

from api.order_api import OrderAPI

edgify_app = Sanic(name=__name__)


# noinspection PyUnusedLocal
@edgify_app.listener('after_server_start')
async def create_work_queue(app, loop):
    app.requests_queue = Queue()
    app.lock = Lock()


# noinspection PyTypeChecker
def main():
    edgify_api = Api(edgify_app)
    edgify_api.add_resource(OrderAPI, '/order_api')
    edgify_app.run(host='0.0.0.0', port=5000, debug=False, workers=1)


if __name__ == '__main__':
    main()
