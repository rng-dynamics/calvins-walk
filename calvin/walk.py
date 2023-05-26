SIGNAL_WAIT_TIME = 80


def expected_wait_time_v1(n_signals: int, n_magic: int) -> int:
    if n_signals == 0:
        return 0
    if n_magic >= n_signals:
        return 0

    e_wait_time_for_rest_with_n_magic = expected_wait_time_v1(n_signals - 1, n_magic)

    if n_magic == 0:
        e_assuming_green = e_wait_time_for_rest_with_n_magic
        e_assuming_red = 0.5 * SIGNAL_WAIT_TIME + e_wait_time_for_rest_with_n_magic
        return 0.5 * e_assuming_green + 0.5 * e_assuming_red

    # assuming green
    e_assuming_green = e_wait_time_for_rest_with_n_magic

    # assuming_red
    e_wait_time_using_magic = expected_wait_time_v1(n_signals - 1, n_magic - 1)
    e_assuming_red = 0
    for time in range(SIGNAL_WAIT_TIME):
        # loop variable starts from 0, hence t_displayed needs + 1
        t_displayed = time + 1
        # expected wait time is half a minute less (e.g., between 0 and 1).
        e_wait_time_for_display = t_displayed - 0.5
        # case: not using magic
        e_not_using_magic = e_wait_time_for_display + e_wait_time_for_rest_with_n_magic
        should_use_magic: bool = e_wait_time_using_magic < e_not_using_magic
        e_assuming_red += (
            e_wait_time_using_magic if should_use_magic else e_not_using_magic
        )

    e_assuming_red /= SIGNAL_WAIT_TIME

    return 0.5 * e_assuming_green + 0.5 * e_assuming_red


def expected_wait_time_v2(n_signals: int, n_magic: int) -> int:
    # This is a non-recursive implementation using a loop. We are simulating
    # the call stack with a list for requests and result dict for computation
    # results.
    req_stack = [(n_signals, n_magic)]
    results = dict()

    while len(req_stack) > 0:
        n_signals_curr, n_magic_curr = req_stack.pop()

        if n_signals_curr == 0:
            results[(n_signals_curr, n_magic_curr)] = 0
            continue
        if n_magic_curr >= n_signals_curr:
            results[(n_signals_curr, n_magic_curr)] = 0
            continue

        if (n_signals_curr - 1, n_magic_curr) not in results:
            req_stack.append((n_signals_curr, n_magic_curr))
            req_stack.append((n_signals_curr - 1, n_magic_curr))
            continue

        e_wait_time_for_rest_with_n_magic = results[(n_signals_curr - 1, n_magic_curr)]

        if n_magic_curr == 0:
            e_assuming_green = e_wait_time_for_rest_with_n_magic
            e_assuming_red = 0.5 * SIGNAL_WAIT_TIME + e_wait_time_for_rest_with_n_magic
            e_time = 0.5 * e_assuming_green + 0.5 * e_assuming_red
            results[(n_signals_curr, n_magic_curr)] = e_time
            continue

        if (n_signals_curr - 1, n_magic_curr - 1) not in results:
            req_stack.append((n_signals_curr, n_magic_curr))
            req_stack.append((n_signals_curr - 1, n_magic_curr - 1))
            continue

        e_wait_time_using_magic = results[(n_signals_curr - 1, n_magic_curr - 1)]

        # assuming green
        e_assuming_green = e_wait_time_for_rest_with_n_magic

        # assuming_red
        e_assuming_red = 0
        for time in range(SIGNAL_WAIT_TIME):
            # loop variable starts from 0, hence t_displayed needs + 1
            t_displayed = time + 1
            # expected wait time is half a minute less (e.g., between 0 and 1).
            e_wait_time_for_display = t_displayed - 0.5
            # case: not using magic
            e_not_using_magic = (
                e_wait_time_for_display + e_wait_time_for_rest_with_n_magic
            )
            should_use_magic: bool = e_wait_time_using_magic < e_not_using_magic
            e_assuming_red += (
                e_wait_time_using_magic if should_use_magic else e_not_using_magic
            )

        e_assuming_red /= SIGNAL_WAIT_TIME

        results[(n_signals_curr, n_magic_curr)] = (
            0.5 * e_assuming_green + 0.5 * e_assuming_red
        )

    return results[(n_signals, n_magic)]


def expected_wait_time_v3(n_signals: int, n_magic: int) -> int:
    # This is a non-recursive implementation using a loop. We are simulating
    # the call stack with a list for requests and result dict for computation
    # results.
    req_stack = [(n_signals, n_magic)]
    results = dict()

    while len(req_stack) > 0:
        n_signals_curr, n_magic_curr = req_stack.pop()

        if n_signals_curr == 0:
            results[(n_signals_curr, n_magic_curr)] = 0
            continue
        if n_magic_curr >= n_signals_curr:
            results[(n_signals_curr, n_magic_curr)] = 0
            continue

        if (n_signals_curr - 1, n_magic_curr) not in results:
            req_stack.append((n_signals_curr, n_magic_curr))
            req_stack.append((n_signals_curr - 1, n_magic_curr))
            continue

        e_wait_time_for_rest_with_n_magic = results[(n_signals_curr - 1, n_magic_curr)]

        if n_magic_curr == 0:
            e_assuming_green = e_wait_time_for_rest_with_n_magic
            e_assuming_red = 0.5 * SIGNAL_WAIT_TIME + e_wait_time_for_rest_with_n_magic
            e_time = 0.5 * e_assuming_green + 0.5 * e_assuming_red
            results[(n_signals_curr, n_magic_curr)] = e_time
            continue

        if (n_signals_curr - 1, n_magic_curr - 1) not in results:
            req_stack.append((n_signals_curr, n_magic_curr))
            req_stack.append((n_signals_curr - 1, n_magic_curr - 1))
            continue

        e_wait_time_using_magic = results[(n_signals_curr - 1, n_magic_curr - 1)]

        # assuming green
        e_assuming_green = e_wait_time_for_rest_with_n_magic

        # assuming_red
        delta = e_wait_time_using_magic - e_wait_time_for_rest_with_n_magic
        delta = int(delta)
        # case: using magic
        e_assuming_red = (SIGNAL_WAIT_TIME - delta) * e_wait_time_using_magic
        # case: not using magic, i.e., waiting
        e_assuming_red += (
            delta * (delta + 1) / 2
            - 0.5 * delta
            + delta * e_wait_time_for_rest_with_n_magic
        )
        e_assuming_red /= SIGNAL_WAIT_TIME

        results[(n_signals_curr, n_magic_curr)] = (
            0.5 * e_assuming_green + 0.5 * e_assuming_red
        )

    return results[(n_signals, n_magic)]
