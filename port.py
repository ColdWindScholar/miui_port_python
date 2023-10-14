# miui_port project

# Only For V-A/B Device

# Based on Android 13

# Test Base ROM: Mi 10S (V14.0.6)

# Test Port ROM: Mi13、Mi13Pro、Mi13Ultra

# 底包和移植包为外部参数传入

import sys
from log import Error, Yellow, Green
BASEROM = sys.argv[1]
PORTROM = sys.argv[2]

