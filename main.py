from housekeeping import checkactivation
from activate import *


if checkactivation():
    home()
else:
    activationscreen()
