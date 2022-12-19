import time


def display_info(msg):
    print(f"[INFO] {msg}")


def display_error(msg):
    print(f"[ERROR] {msg}")


def exit_error(msg):
    display_error(msg)
    exit(-1)


def display_results(counters, start_time):
    print(f"{'=' * 20}\nTime of work: {int(time.time() - start_time)} sec\n")
    endpoints_total = 0
    for status_code in counters:
        endpoints_cnt = counters[status_code]
        endpoints_total += endpoints_cnt
        # 0 is default request status code value for fuzzing endpoints
        print(f"{status_code or 'Need Fuzzing'} Endpoints: {endpoints_cnt}")
    print(f"\nTotal number of endpoints: {endpoints_total}")


def _get_ep_prefix(ep):
    return ep.node_depth * ' '


def display_endpoint(ep):
    display_info(f"Found endpoint: {_get_ep_prefix(ep)}{ep}")


def display_endpoint_node(ep):
    display_info(f"Found endpoints node {_get_ep_prefix(ep)}{ep}")
