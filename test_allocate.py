import pytest
from datetime import date, timedelta
from model import Batch, OrderLine, allocate, OutOfStock

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)

def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch("in_stock_batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment_batch", "RETRO-CLOCK", 100, eta=tomorrow)
    line = OrderLine("oref", "RETRO-CLOCK", 10)

    allocate(line, [shipment_batch, in_stock_batch])
    
    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    earliest = Batch("speedy-batch", "RETRO-CLOCK", 100, eta=None)
    medium = Batch("normal-batch", "RETRO-CLOCK", 100, eta=tomorrow)
    slow = Batch("slow-batch", "RETRO-CLOCK", 100, eta=later)
    line = OrderLine("oref", "RETRO-CLOCK", 10)

    allocate(line, [medium, earliest, slow])
    
    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert slow.available_quantity == 100


def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch('batch1', "FORK", 10, eta=today)
    allocate(OrderLine('order-1', 'FORK', 9), [batch])

    with pytest.raises(OutOfStock, match='FORK'):
        allocate(OrderLine('order-2', 'FORK', 2), [batch])