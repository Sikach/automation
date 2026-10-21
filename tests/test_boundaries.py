import pytest

@pytest.mark.parametrize("value", [0, 1, 50, 99, 100])
def test_pwm_valid_boundaries(device, value):
    r = device.command(f"SET PWM {value}")
    assert r["status"] == "OK"
    assert r["pwm"] == value

@pytest.mark.parametrize("value", [-1, 101, 999])
def test_pwm_invalid_boundaries(device, value):
    r = device.command(f"SET PWM {value}")
    assert r["status"] == "ERROR"
    assert r["code"] == "INVALID_VALUE"


# New test TC-09
@pytest.mark.parametrize("value", [-0.1, 99.99, 999.999])
def test_pwm_invalid_values(device, value):
    bfr = device.command("STATUS")

    if bfr["led"] is False:
        assert bfr["pwm"] == 0
        expected_pwm = 0
    else:
        expected_pwm = bfr["pwm"]

    r = device.command(f"SET PWM {value}")
    assert r["status"] == "ERROR"
    assert r["code"] == "INVALID_VALUE"

    aft = device.command("STATUS")
    assert aft["pwm"] == expected_pwm