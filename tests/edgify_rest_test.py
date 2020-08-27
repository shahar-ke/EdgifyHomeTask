import concurrent.futures

import requests

from models.order import Order
from models.order_status import OrderStatus


def make_request(request_data):
    return requests.post('http://localhost:5000/order_api/', json=request_data)


def generate_data(amount: int = 100):
    data_list = list()
    for i in range(amount):
        data_list.append({'order': f'order_{i}',
                          'price': i})
    return data_list


def main():
    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        # Start the load operations and mark each future with its URL
        request_data_list = generate_data()
        future_to_req_data = {executor.submit(make_request, request_data): request_data
                              for request_data in request_data_list}
        for future in concurrent.futures.as_completed(future_to_req_data):
            req_data = future_to_req_data[future]
            try:
                response = future.result()
            except Exception as e:
                print(f'{req_data} generated an exception: {e}')
            else:
                assert response.status_code == 200, response.status_code
                resp_data = response.json()
                print(f'{req_data} response: {resp_data}')
                order_status = resp_data[Order.STATUS_ATTR]
                assert response != OrderStatus.UNPROCESSED
                assert order_status in {OrderStatus.APPROVED, OrderStatus.REJECTED}


if __name__ == '__main__':
    main()
    print('done')
