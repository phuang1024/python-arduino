Setup
=====

First, install the Python module.

``pip install python-arduino``

Next, plug in an Arduino board. Locate the device file that corresponds to it:

.. code-block:: bash

    user@comp:~$ cd /dev

    user@comp:/dev$ ll | grep ttyACM
    crw-rw----   1 root    dialout 166,    0 Nov  6 00:00 ttyACM0   # This is the device file
 
    user@comp:/dev$ sudo chmod 666 ttyACM0   # Allow all users to control it

Before you can control the board, compile and upload the Firmata program to it. Open the
Arduino IDE and open ``File >> Examples >> Firmata >> StandardFirmata``, and compile and upload.
