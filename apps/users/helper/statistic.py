from typing import List

from config.settings.dev import LIMIT_STATISTIC_ORDER, LIMIT_TERMINAL_OF_STATISTIC_ORDER


def get_dates(results: List):
    date_of_orders_object = {}
    date_of_orders = []
    for rs in results:
        date = rs['date']
        if date_of_orders_object.get(date) is None:
            date_of_orders.append(date)
            date_of_orders_object[date] = True
        if len(date_of_orders) >= LIMIT_STATISTIC_ORDER:
            break
    return date_of_orders


def get_total_order_by_date(results: List):
    date_to_terminal = {}
    for rs in results:
        date = rs['date']
        name = rs.get('name')
        total_order = rs.get('total_order', 0)
        if date_to_terminal.get(date) is None:
            date_to_terminal[date] = {}
        terminal_to_total_order = date_to_terminal.get(date)
        if name is not None:
            terminal_to_total_order[name] = total_order

    return date_to_terminal


def get_terminal_of_order(results: List):
    terminals_object = {}
    terminals = []
    for rs in results:
        name = rs.get('name')
        if name is None:
            continue
        if terminals_object.get(name) is None:
            terminals.append(name)
            terminals_object[name] = True
        if len(terminals) >= LIMIT_TERMINAL_OF_STATISTIC_ORDER:
            break
    return terminals


def extract_data_order_statistic(results: List):
    date_of_orders = get_dates(results)
    date_to_terminal = get_total_order_by_date(results)
    terminals = get_terminal_of_order(results)

    terminal_to_list_total_order = {terminal: [] for terminal in terminals}

    for date in date_of_orders:
        terminal_to_total_order = date_to_terminal.get(date)
        for terminal in terminals:
            terminal_order = terminal_to_list_total_order.get(terminal, [])
            total_order = terminal_to_total_order.get(terminal)
            if total_order is None:
                terminal_order.append(0)
            else:
                terminal_order.append(total_order)

    return {
        'date_of_orders': date_of_orders,
        'terminal_to_list_total_order': [
            {
                'name': t,
                'total_orders': terminal_to_list_total_order[t]
            }
            for t in terminal_to_list_total_order
        ]
    }


def extract_data_revenue_by_user_statistic(results: List):
    dates = []
    revenues = []
    for rs in results:
        dates.append(rs['date'])
        revenues.append(rs.get('total_amount') or 0)
        if len(dates) >= LIMIT_STATISTIC_ORDER:
            break

    return {
        'dates': dates,
        'revenues': revenues
    }


def extract_data_revenue_by_time_statistic(results: List):
    dates = []
    revenues = []
    for rs in results:
        dates.append(rs['date'])
        revenue_order = rs.get('total_amount_order') or 0
        revenue_terminal = rs.get('total_amount_terminal') or 0
        revenues.append(revenue_order + revenue_terminal)
        if len(dates) >= LIMIT_STATISTIC_ORDER:
            break

    return {
        'dates': dates,
        'revenues': revenues
    }
