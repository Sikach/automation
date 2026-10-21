import pytest

# New test TC-15
@pytest.mark.parametrize(
    "command",
    [
        "unknown",
        "foo bar",
        "set xyz 10",
    ],
)
def test_unknown_commands(device, command):
    r = device.command(command)

    assert r["status"] == "ERROR"
    assert r["code"] == "UNKNOWN_COMMAND"
