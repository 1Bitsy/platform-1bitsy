# 1Bitsy for PlatformIO

This requires the 3.0 version of [PlatformIO](http://platformio.org). If the About page indicates version 2.x.x, then update to V3.x.x from the PlatformIO start page. 

# Installing the 1Bitsy toolchain.

Run 
```
platformio install platforms https://github.com/1bitsy/platform-1bitsy.git
```

For development, install the git repository by itself.
```
cd ~/.platformio/platforms/
git clone https://github.com/1bitsy/platform-1bitsy.git -o 1bitsy
```

## Basics of the build system

Most of it is in `builder/main.py`. For the most part, everything is just setting up flags, which are appropriately named. 

The "build recipes" start ~L#121 at `BUILDERS=dict(...`. These very closely match the Makefile for the system. 
	
Conspicuously missing is any sort of a .map file at this time. 

Upload stuff is currently left in from the stock STM32 project, pending the build process working right. 
