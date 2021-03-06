# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
    Builder for ST STM32 Series ARM microcontrollers.
"""

# This page details all the stuff needed to patch this up
# http://www.scons.org/doc/production/HTML/scons-user.html#cv-_LIBFLAGS

from os.path import isfile, join

from SCons.Script import (COMMAND_LINE_TARGETS, AlwaysBuild, Builder, Default,
                          DefaultEnvironment,Environment)

env = DefaultEnvironment()

for keys,values in env.items():
	break;
	if keys=="ENV": continue
	print keys,"== ",values
	# PIOPLATFORM = 1bitsy

	print "What about these ones?"
	print "PIOHOME_DIR=>",env.get("PIOHOME_DIR")

env.Replace(
    AR="arm-none-eabi-ar",
    AS="arm-none-eabi-as",
    CC="arm-none-eabi-gcc",
    CXX="arm-none-eabi-g++",
    OBJCOPY="arm-none-eabi-objcopy",
    RANLIB="arm-none-eabi-ranlib",
    SIZETOOL="arm-none-eabi-size",

    ARFLAGS=["rcs"],

    ASFLAGS=["-x", "assembler-with-cpp"],

    CCFLAGS=[
        "-Os",  # optimize for size
        "-g",   # include debugging info (so errors include line numbers)
	"-Wextra",
	"-Wshadow",
	"-Wimplicit-function-declaration",
	"-Wredundant-decls",
	"-Wmissing-prototypes",
	"-Wstrict-prototypes",
	"-fno-common",
        "-ffunction-sections",  # place each function in its own section
        "-fdata-sections",
        "-Wall",
	"-Wundef",
        "-mthumb",
	"-mfloat-abi=hard",
	"-mfpu=fpv4-sp-d16"
        #"-nostdlib"
    ],

    CXXFLAGS=[
        "-fno-rtti",
        "-fno-exceptions"
    ],

    CPPDEFINES=[
        "F_CPU=$BOARD_F_CPU"
    ],

    LINKFLAGS=[
	"--static",
        "-nostartfiles",
        "-Wl,--gc-sections",
        "-mthumb",
	"-mfloat-abi=hard",
	"-mfpu=fpv4-sp-d16"
	#"-nostdlib",
        #,"-v"
    ],


    #LIBS=["c", "gcc", "m", "stdc++", "nosys"],
    LIBS=["c", "gcc", "m", "nosys"],
    
    UPLOADER="gdb",
    UPLOADERFLAGS=[
        #TODO Probably need stuff here
    ],
    UPLOADCMD='$UPLOADER $UPLOADERFLAGS',

    SIZEPRINTCMD='$SIZETOOL -B -d $SOURCES',

    PROGNAME="firmware",
    PROGSUFFIX=".elf"
)

if "BOARD" in env:
    env.Append(
        CCFLAGS=[
            "-mcpu=%s" % env.BoardConfig().get("build.cpu")
        ],
        CPPDEFINES=[
            env.BoardConfig().get("build.variant", "").upper()
        ],
        
        LINKFLAGS=[
            "-mcpu=%s" % env.BoardConfig().get("build.cpu"),
            "-L$PIOHOME_DIR/platforms/$PIOENV/ldscripts/"
            #vv Example of a working line!
            #"-L /home/tekdemo/.platformio/platforms/onebitsy/ldscripts/"
            #"-T%s" % env.BoardConfig().get("build.ldscript"),
        ],
		#This should work, but doesn't. Overriding the target linkable
		#sdcript in LINKFLAGS works for now
		#LDSCRIPT_PATH="stm32f4-1bitsy.ld",
		#,LIBPATH=["$PROJECT_DIR","$PROJECT_DIR/ldscripts"],
		# By default LIBPATH is set to  ['/home/tekdemo/.platformio/platforms/onebitsy/ldscripts']
		# which is already correct
		
        GDBSCRIPT_PATH=" $PIOHOME_DIR/platforms/$PIOENV/gdbscripts/"
    )

env.Append(
    ASFLAGS=env.get("CCFLAGS", [])[:],

    BUILDERS=dict(
        ElfToBin=Builder(
            action=env.VerboseAction(" ".join([
                "$OBJCOPY",
                "-O",
                "binary",
                "$SOURCES",
                "$TARGET"
            ]), "Building $TARGET"),
            suffix=".bin"
        ),
        ElfToHex=Builder(
            action=env.VerboseAction(" ".join([
                "$OBJCOPY",
                "-O",
                "ihex",
                "-R",
                ".eeprom",
                "$SOURCES",
                "$TARGET"
            ]), "Building $TARGET"),
            suffix=".hex"
        )
    )
)

if env.subst("$UPLOAD_PROTOCOL") == "gdb":

    if not isfile(join(env.subst("$PROJECT_DIR"), "upload.gdb")):
        print "Using default upload script."
        print "Create an `upload.gdb` file in your project directory"
        print "to override upload option"
        gdbscript="%s" % join("$GDBSCRIPT_PATH", "upload.gdb")
    else:
        print "Using project upload script"
        gdbscript="%s" % join("$PROJECT_DIR", "upload.gdb")


    env.Replace(
        UPLOADER="arm-none-eabi-gdb",
        UPLOADERFLAGS=[
            join("$BUILD_DIR", "firmware.elf"),
            "-batch",
            "-x",
            '"%s"' % gdbscript
        ],

        UPLOADCMD='$UPLOADER $UPLOADERFLAGS',
    )
	

#
# Target: Build executable and linkable firmware
#
target_elf = env.BuildProgram()

#
# Target: Build the .bin file
#

if "uploadlazy" in COMMAND_LINE_TARGETS:
    target_firm = join("$BUILD_DIR", "firmware.bin")
else:
    target_firm = env.ElfToBin(join("$BUILD_DIR", "firmware"), target_elf)

#
# Target: Print binary size
#

target_size = env.Alias(
    "size", target_elf,
    env.VerboseAction("$SIZEPRINTCMD", "Calculating size $SOURCE"))
AlwaysBuild(target_size)

#
# Target: Upload by default .bin file
#

# if "mbed" in env.subst("$PIOFRAMEWORK") and not env.subst("$UPLOAD_PROTOCOL"):
#     upload = env.Alias(
#         ["upload", "uploadlazy"], target_firm,
#         [env.VerboseAction(env.AutodetectUploadPort,
#                            "Looking for upload disk..."),
#          env.VerboseAction(env.UploadToDisk, "Uploading $SOURCE")])
# else:
#     upload = env.Alias(["upload", "uploadlazy"], target_firm,
#                        env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE"))


#From the sTM32-GDB directions, see if this works 
#https://gist.github.com/valeros/28d84a7a8f78825e6956
if env.BoardConfig().get("upload.protocol")=="gdb":
	upload = env.Alias(["upload", "uploadlazy"], target_firm, "$UPLOADCMD")
else:
	print "Not supported!"
AlwaysBuild(upload)



#
# Default targets
#

Default([target_firm, target_size])
