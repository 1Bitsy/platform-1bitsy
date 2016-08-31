import os

from platformio.platforms.ststm32 import Ststm32Platform


class OnebitsyPlatform(Ststm32Platform):

    """
    ST STM32 using GDB as uploader

    http://www.st.com/web/en/catalog/mmc/FM141/SC1169?sc=stm32
    """

    def get_build_script(self):

        return os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "onebitsy-builder.py"
        )
