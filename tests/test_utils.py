from model_w.env_manager._utils import loose_call  # noqa


def test_loose_call():
    def foo(bar=42):
        return bar

    assert loose_call(foo) == 42
    assert loose_call(foo, 10) == 10
    assert loose_call(foo, bar=10)
    assert loose_call(foo, bar=10, yolo=True) == 10
    assert loose_call(foo, yolo=True) == 42
