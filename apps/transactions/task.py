from datetime import timedelta
from typing import Optional
from uuid import UUID

from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

from apps.carts.models import CartProduct
from apps.orders.models import Order
from apps.terminals.models.terminal import TerminalStatus
from apps.terminals.models.terminal_payment import TypeTerminalPayment
from apps.users.models import User
from apps.orders.models.order import OrderType
from apps.terminals.models import Product, WareHouse, Terminal, TerminalPayment
from apps.transactions.models import Transaction
from apps.transactions.models.transaction import TransactionType
from config.celery import app
from django.db import transaction as tran


@app.task
@tran.atomic()
def handler_success(transaction_id: UUID, **kwargs):
    print(f'start handle payment success with transaction_id: {transaction_id}')
    transaction = None
    try:
        user_id: UUID = kwargs.get('user_id')
        user = User.objects.get(pk=user_id)
        kwargs['user'] = user

        transaction = Transaction.objects.get(pk=transaction_id)
        if not transaction.status:
            return
        transaction_type = transaction.type
        handler_id = transaction.handler_id
        if transaction_type == TransactionType.ORDER:
            order_handler(handler_id=handler_id, is_success=True, transaction=transaction, **kwargs)
        elif transaction_type == TransactionType.REGISTER_TERMINAL:
            register_terminal_handler(handler_id=handler_id, is_success=True, transaction=transaction, **kwargs)
        elif transaction_type == TransactionType.EXTEND_TERMINAL:
            extend_terminal_handler(handler_id=handler_id, is_success=True, transaction=transaction, **kwargs)
        else:
            return
        transaction.status = False
        transaction.save()
    except Exception as e:
        print(e)
        if isinstance(transaction, Transaction):
            transaction.status = False
            transaction.save()


@app.task
@tran.atomic()
def handler_fail(transaction_type: str, handler_id: UUID, **kwargs):
    print(f'start handle payment fail with handler_id: {handler_id}')
    try:
        user_id: UUID = kwargs.get('user_id')
        user = User.objects.get(pk=user_id)
        kwargs['user'] = user
        if transaction_type == TransactionType.ORDER:
            order_handler(handler_id=handler_id, is_success=False, **kwargs)
        if transaction_type == TransactionType.REGISTER_TERMINAL:
            register_terminal_handler(handler_id=handler_id, is_success=False, **kwargs)
        if transaction_type == TransactionType.EXTEND_TERMINAL:
            extend_terminal_handler(handler_id=handler_id, is_success=False, **kwargs)
    except Exception as e:
        print(e)


@tran.atomic()
def order_handler(handler_id, is_success=True, **kwargs):
    orders = Order.objects.prefetch_related('details')\
        .filter(pk=handler_id, type__in=[OrderType.CREATE, OrderType.FAIL])
    user: Optional[User, AnonymousUser] = kwargs.get('user')
    if len(orders) != 1 or user is None or isinstance(user, AnonymousUser):
        return
    order = orders.first()
    details = order.details.all()
    product_ids = [d.product_id for d in details]
    if is_success:
        transaction: Optional[Transaction] = kwargs.get('transaction')
        if transaction is None:
            return

        order.type = OrderType.PAID
        order.transaction = transaction
        CartProduct.objects.filter(product_id__in=product_ids, cart__user_id=user.id).delete()
    else:
        order.type = OrderType.FAIL
        warehouses = []
        products = Product.objects.select_related('warehouse').filter(id__in=product_ids)
        id_to_warehouse = {p.id: p.warehouse for p in products}
        for item in details:
            warehouse = id_to_warehouse.get(item.product_id)
            warehouse.quantity += item.quantity
            warehouses.append(warehouse)
        if len(warehouses) > 0:
            WareHouse.objects.bulk_update(warehouses, fields=['quantity'], batch_size=5)
    order.save()


@tran.atomic()
def register_terminal_handler(handler_id, is_success=True, **kwargs):
    now = timezone.now()
    user: Optional[User, AnonymousUser] = kwargs.get('user')
    if user is None or isinstance(user, AnonymousUser):
        return
    terminals = Terminal.objects.filter(
        pk=handler_id,
        type=TerminalStatus.REGISTER,
        seller_id=user.id,
        status=False
    )

    if len(terminals) != 1:
        return
    terminal = terminals.first()

    if is_success:
        terminal.type = TerminalStatus.PAID
        terminal.status = terminal.time_open < now
        if terminal.time_open < now:
            terminal.time_open = now
        terminal.expired_at = terminal.time_open + timedelta(terminal.time_selling)

        transaction: Optional[Transaction] = kwargs.get('transaction')
        if transaction is None:
            return

        TerminalPayment(
            transaction=transaction,
            terminal=terminal,
            type=TypeTerminalPayment.REGISTER,
        ).save()
    else:
        terminal.type = TerminalStatus.FAIL
    terminal.save()


@tran.atomic()
def extend_terminal_handler(handler_id, is_success=True, **kwargs):
    now = timezone.now()
    user: Optional[User, AnonymousUser] = kwargs.get('user')
    if user is None or isinstance(user, AnonymousUser):
        return
    terminals = Terminal.objects.filter(
        pk=handler_id,
        type=TerminalStatus.EXTEND,
        seller_id=user.id
    )

    if len(terminals) != 1:
        return
    terminal = terminals.first()

    if is_success:
        terminal.type = TerminalStatus.PAID
        terminal.max_quantity_product = terminal.extend_max_quantity_product
        if terminal.expired_at < now:
            terminal.time_open = now
            terminal.time_selling = terminal.extend_time_selling
            terminal.status = True
        else:
            terminal.time_selling += terminal.extend_time_selling

        terminal.expired_at = terminal.time_open + timedelta(terminal.time_selling)
        terminal.extend_max_quantity_product = 0
        terminal.extend_time_selling = 0

        transaction: Optional[Transaction] = kwargs.get('transaction')
        if transaction is None:
            return

        TerminalPayment(
            transaction=transaction,
            terminal=terminal,
            type=TypeTerminalPayment.EXTEND,
        ).save()
    else:
        terminal.type = TerminalStatus.EXTEND_FAIL
        # terminal.extend_max_quantity_product = 0
        # terminal.extend_time_selling = 0
    terminal.save()
