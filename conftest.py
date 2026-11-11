import os
from collections.abc import Iterator

import pytest

from avl import Root

# pytest only tells fixtures whether the test passed through this hook: it
# stashes each phase's report ("setup", "call", "teardown") on the test item.
phase_report_key = pytest.StashKey[dict[str, pytest.TestReport]]()


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]):
    report = yield
    item.stash.setdefault(phase_report_key, {})[report.when] = report
    return report


@pytest.fixture
def t(request: pytest.FixtureRequest) -> Iterator[Root]:
    """An empty AVL tree, drawn to debug/<test name>.png if the test fails."""
    tree = Root()
    yield tree

    report = request.node.stash.get(phase_report_key, {}).get("call")
    if report is not None and report.failed:
        os.makedirs("debug", exist_ok=True)
        tree.debug_tree(f"debug/{request.node.name}.png")
