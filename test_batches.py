from datetime import date
from model import Batch, OrderLine

def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch('batch-001', sku, batch_qty, eta=date.today()),
        OrderLine('order-123', sku, line_qty)
    ) 


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch, line = make_batch_and_line('SMALL-TABLE', 20, 2)
    batch.allocate(line)
    
    assert batch.available_quantity == 18
    

def test_can_allocate_if_available_greater_than_required():
    large_batch, small_line = make_batch_and_line("RED-CHAIR", 20, 2)
    assert large_batch.can_allocate(small_line)

def test_can_allocate_if_available_equal_to_required():
    large_batch, small_line = make_batch_and_line("RED-CHAIR", 2, 2)
    assert large_batch.can_allocate(small_line)

def test_cannot_allocate_if_available_less_than_required():
    large_batch, small_line = make_batch_and_line("RED-CHAIR", 2, 20)
    assert large_batch.can_allocate(small_line) is False

def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch("batch-001", "RED-PILL", 100, eta=None)
    different_sku_line = OrderLine("order-123", "BLUE-PILL", 20)
    assert batch.can_allocate(different_sku_line) is False

def test_can_only_deallocate_allocated_lines():
    batch, line = make_batch_and_line("SOFA", 20, 2)
    batch.allocate(line)
    assert batch.available_quantity == 18
    batch.deallocate(line)
    assert batch.available_quantity == 20