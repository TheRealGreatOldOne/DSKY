import storage
import board, digitalio

# enable / disable USB storage mode dependant on GP22 being pulled Up or Down
# inital state is pulled up, so will not mount and will be a HID only device
# grounding GP22 during boot will allow USB storage mode.
storeOff = digitalio.DigitalInOut(board.GP22)
storeOff.direction = digitalio.Direction.INPUT
storeOff.pull = digitalio.Pull.UP

# Disable devices only if button is not pressed.
if storeOff.value:
    print(f"boot: GP22 high, disabling drive")
    storage.disable_usb_drive()