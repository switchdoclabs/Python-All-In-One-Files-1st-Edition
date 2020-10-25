Python All In One For Dummies, 2nd Edition


These are the install directions for the PiCar-B Python Testing software.  These instructions are necessary to get the 12 programmable RGB LEDs to work on the Raspberry Pi.



First we will need some developer libraries which will allow us to compile the software. This is
installed using the normal Raspberry Pi installer as below:

sudo apt-get install build-essential python3-dev git scons swig

Next download the neopixel code from github using the clone command, which copies all the
source code to your local computer.

git clone https://github.com/jgarff/rpi_ws281x.git

Change to that directory and run scons to compile the software.

cd rpi_ws281x
scons

We then need to change to the python directory and install the Python module from there:

cd python

Next install the Python 3 library file using

sudo python3 setup.py install



