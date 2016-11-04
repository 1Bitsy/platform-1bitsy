# 1bitsy for Platform.io 


This requires the 3.0 version of Platform.io. If the About page indicates version 2.x.x, then update to V3.x.x from the PlatformIO start page. 

# Installing the OneBitsy toolchain.

Run 
```
platformio install platforms https://github.com/tekdemo/platform-onebitsy.git
```

For development, install the git repository by itself. 
```
cd ~/.platformio/platforms/
git clone https://github.com/tekdemo/platform-onebitsy.git -o onebitsy
```

#TODO
- [ ] Need to automatically run make on the `libopencm3` before attempting to build the project
- [X] Still has a linker config issue. Have leads, pretty close to figuring this out methinks. 
	- Useful: http://www.scons.org/doc/production/HTML/scons-user.html
	- http://docs.platformio.org/en/stable/platforms/creating_platform.html
	- https://github.com/platformio/platformio/blob/8a379d2db26ff0deb37be83e82d1abe72e5439f8/platformio/builder/tools/platformio.py#L68
- [ ] Upload
	- [ ] JTAG
	- [ ] SWDIO
	- [ ] Uart?
	- [ ] USB without BMP? 

## Basics of the build system

Most of it is in `builder/main.py`. For the most part, everything is just setting up flags, which are appropriately named. 

The "build recipes" start ~L#121 at `BUILDERS=dict(...`. These very closely match the Makefile for the system. 
	
Conspicuously missing is any sort of a .map file at this time. 

Upload stuff is currently left in from the stock STM32 project, pending the build process working right. 