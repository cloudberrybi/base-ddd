import pytest
import dramatiq

from dramatiq import Worker
from dramatiq.brokers.stub import StubBroker 
from dramatiq.results.backends import StubBackend
from dramatiq.results import Results


@pytest.fixture()
def stub_broker():
    broker = StubBroker()
    broker.emit_after("process_boot")

    backend = StubBackend(
        encoder=dramatiq.PickleEncoder(),
    )
    broker.add_middleware(Results(backend=backend))

    dramatiq.set_broker(broker)
    dramatiq.set_encoder(dramatiq.PickleEncoder())

    yield broker
    broker.flush_all()
    broker.close()

@pytest.fixture()
def stub_worker(stub_broker):
    worker = Worker(stub_broker, worker_timeout=100, worker_threads=32)
    worker.start()
    yield worker
    worker.stop()
