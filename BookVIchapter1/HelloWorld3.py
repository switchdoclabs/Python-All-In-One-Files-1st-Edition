from gpiozero import PWMLED
from signal import pause

led = PWMLED(12)

led.pulse()

pause()
