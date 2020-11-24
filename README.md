# Thingspeak-Python

Python3 Module for sending label-encoded data over a Thingspeak channel. Read/write implemented in a channel handler object, for both client side and server side.
Note: Thingspeak works on a publish-subscribe model, so there can be multiple channel handler objects (i.e, multiple clients and servers).

### Installation ###
thingspeak.py and thingspeak_params.py must be in your project folder, the same one you invoke the module from.
The module only uses two non-inbuilt python packages - `matplotlib` and `requests`. Install by running `pip3 install <package>` on terminal.

### Usage ###
- Server side: Send data by invoking the thingspeak.send() and thingspeak.transmit(). Send label or index as parameter to thingspeak.send(), index gets stored in a buffer (594 max values) and thingspeak.transmit() sends the buffer as one entry.
- Client side: thingspeak.get() returns a dictionary - keys are labels, values are number of occurrences in across all entries in the channel. thingspeak.get_img() plots a bar graph.

#### Run the demo for quickstart ###
