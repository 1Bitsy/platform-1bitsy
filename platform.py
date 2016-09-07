import os
from platformio.managers.platform import PlatformBase


class OnebitsyPlatform(PlatformBase):

    """
    Install tooling for 1bitSquared 1Bitsy
    """

    def get_build_script(self):

        return os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "onebitsy-builder.py"
        )

    def configure_default_packages(self, variables, targets):
        if variables.get("board"):
            board_config = self.board_config(variables.get("board"))
            toolchain = "toolchain-gccarmnoneeabi"
            self.packages[toolchain]['optional'] = False

        return PlatformBase.configure_default_packages(
            self, variables, targets)
