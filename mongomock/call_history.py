
from collections import defaultdict
from unittest.mock import call


class CallHistoryAsserter(object):
    def __init__(self, calls) -> None:
        self._calls = calls

    @property
    def calls(self):
        return self._calls

    def assert_called(self) -> None:
        return bool(self._calls)

    def assert_called_once(self) -> None:
        return len(self._calls) == 1

    def assert_called_once_with(self, *args, **kwargs) -> None:
        assert len(self._calls) == 1, f"Expected 1 call, got {len(self._calls)}"
        self.assert_called_with(*args, **kwargs)

    def assert_called_with(self, *args, **kwargs) -> None:
        assert self._calls[-1] == (args,
                                   kwargs), f"Expected call with {args}, {kwargs}, got {self._calls[-1]}"

    def assert_any_call(self, *args, **kwargs) -> None:
        for call in self._calls:
            if call == (args, kwargs):
                return
        assert False, f"Expected call with {args}, {kwargs}, got {self._calls}"

    def assert_has_calls(self, calls, any_order=False) -> None:
        mock_calls = [call(*args, **kwargs) for args, kwargs in self._calls]
        if not any_order:
            assert calls == mock_calls, f"Expected calls {calls}, got {self._calls}"
            return

        for expected in calls:
            try:
                mock_calls.remove(expected)
            except ValueError:
                assert False, f"Expected calls {calls}, got {self._calls}"
        assert not mock_calls, f"Expected calls {calls}, got {self._calls}"

    def assert_not_called(self) -> None:
        assert self._calls == [], f"Expected no calls, got {self._calls}"


class CallHistory(object):
    def __init__(self) -> None:
        super().__init__()
        self._call_store = defaultdict(list)

    def __repr__(self) -> str:
        return f"CallHistory[{repr(self._call_store)}]"

    def __getattr__(self, name) -> CallHistoryAsserter:
        return CallHistoryAsserter(self._call_store[name])

    def add(self, func, *args, **kwargs):
        self._call_store[func.__name__] += [(args, kwargs)]
