# Bux
Run experiments locally on a Raspberry Pi

# Description
Bux aims at simplicity. At its core it serves the purpose to enable video recording and logging environmental data seamlessly.

Bux will come with a graphical user interface (GUI) as well as command-line control. That means that the Pi can be accessed and controlled remotely both via SSH (accessing the command line) and VNC (virtual network control, access the user interface).

The idea is to get the size compressed, and now that MicroSD cards are getting sufficiently cheap and with greater capacity it is now feasible to save large amounts of data locally.

To make Bux as customizable as possible, it is provided both as a python script (PyPi +package at some point?) and as a Raspberry Pi OS Lite disk image, ready to be flashed onto your SD card for immediate use. It currently uses Buster, but will transition to Bullseye once Python bindings are ready for the new image library.

# Camera control

# Environmental data
To allow users the maximal control of their environmental sensing, Bux uses serial input - form any microcontroller (Arduino, Raspberry Pi Pico, you name it). Just ensure that your device prints the data, then Bux will read it.
