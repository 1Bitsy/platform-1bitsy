# Shut up stupid prompt
#y

# Connect to Black magic probe
target extended-remote /dev/ttyACM0

# Print BMPM version
mon version

# To make sure the target is not in a "strange" mode we tell BMPM to reset the
# target using the reset pin.
mon connect_srst enable

#supply power to the target device
monitor tpwr enable

# Find the target
monitor jtag_scan

# Attach to the first device
attach 1

# Load the binary
load

# Check if the flash matches the binary
compare-sections

# Reset and exit
kill
