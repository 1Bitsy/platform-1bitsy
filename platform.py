import os
from platformio.managers.platform import PlatformBase


class OnebitsyPlatform(PlatformBase):

    """
    Install tooling for 1BitSquared 1Bitsy
    """

    def configure_default_packages(self, variables, targets):
        if variables.get("board"):
            board_config = self.board_config(variables.get("board"))
            toolchain = "toolchain-gccarmnoneeabi"
            self.packages[toolchain]['optional'] = False

            #https://github.com/platformio/platform-atmelsam/blob/a0797d485d01d2c5b4afa55d2c314458f4d49020/platform.py
            # upload_protocol = self.board_config(variables.get("board")).get(
            #     "upload.protocol", "")
            # upload_tool = None
            # if upload_protocol == "openocd":
            #     upload_tool = "tool-openocd"
            # elif upload_protocol == "sam-ba":
            #     upload_tool = "tool-bossac"
            # elif upload_protocol == "stk500v2":
            #     upload_tool = "tool-avrdude"
			# 
            # if upload_tool:
            #     for name, opts in self.packages.items():
            #         if "type" not in opts or opts['type'] != "uploader":
            #             continue
            #         if name != upload_tool:
            #             del self.packages[name]



        return PlatformBase.configure_default_packages(
            self, variables, targets)
