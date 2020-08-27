# EdgifyHomeTask

## implemented as a restful app with [sanic](https://github.com/huge-success/sanic), [sanic-restful-api](https://github.com/linzhiming0826/sanic-restful), an async web frameworks


implementation explained:

after app is created it is being:
- associated with rest "order_api" endpoint
- attached with an joinable event queue and lock to be shared with all requests to server
- upon request, the shared queue and lock are fetched from app, request is added to queue, and awaits until queue size will reach buffer limit defined
- when buffer limit reached, one request thread is passing all orders to execution server, and updates requests in place, and clearing the buffer
- after buffer is clear, all awaited requests now have an executed order to return

usage:
- install requirements from requirements.txt to your python 3.8 based interpreter/virtual env
- run: #python ./edify_app.py 

test:
- run: #PYTHONPATH=[path_to_repo] python ./tests/edgify_rest_test.py
