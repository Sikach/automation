import pytest

def test_led_on_off(device):
    assert device.command("SET LED ON")["led"] is True
    assert device.command("SET LED OFF")["led"] is False

def test_reset_restores_safe_state_of_led_on(device):
    device.command("SET LED ON")
    device.command("RESET")
    status = device.command("STATUS")
    assert status["pwm"] == 0
    assert status["led"] is False

# New test TC-10 | Bug 3
def test_pwm_overriding(device):
    bfr = device.command("SET PWM 12")
    assert bfr["pwm"] == 12
    
    device.command("SET PWM 13")
    aft = device.command("STATUS")
    assert aft["pwm"] == 13
   
# New test TC-12    
def test_reset_restores_safe_state_of_led_on(device):
    device.command("SET LED OFF")
    device.command("RESET")
    status = device.command("STATUS")
    assert status["pwm"] == 0
    assert status["led"] is False    

# New test TC-13  | Bug 5
def test_reset_restores_pwm_to_0(device):
    bfr = device.command("SET PWM 12")
    assert bfr["pwm"] == 12
    
    device.command("RESET")
    status = device.command("STATUS")
    assert status["pwm"] == 0
    
# New test TC 14 
def test_reset_should_not_change_state_if_pwm_is_0(device):
   bfr = device.command("STATUS")
   assert bfr["pwm"] == 0
   
   rst = device.command("RESET")
   assert rst["reset"] is True
   
   status = device.command("STATUS")
   assert status["pwm"] == 0
   
# New tests TC-06, TC-07
@pytest.mark.parametrize(
    "command, expected_led",
    [
        ("SET LED ON", True),
        ("SET LED OFF", False),
    ],
)
def test_repeated_led_command_is_idempotent(device, command, expected_led):
    r = device.command(command)
    assert r["status"] == "OK"
    assert r["led"] is expected_led

    r = device.command(command)
    assert r["status"] == "OK"
    assert r["led"] is expected_led

    r = device.command("STATUS")
    assert r["status"] == "OK"
    assert r["led"] is expected_led
