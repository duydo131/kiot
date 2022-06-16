from config.settings.dev import PER_CENT_ORDER, CEILING_PRICE


def calculate_fee(total_price=None):
    if total_price is None:
        return 0
    fee = total_price * PER_CENT_ORDER // 100
    fee = fee if fee < CEILING_PRICE else CEILING_PRICE
    fee = fee // 100 * 100
    return fee
