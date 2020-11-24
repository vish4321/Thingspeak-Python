# Thingspeak-Python

Module for sending label-encoded data over a Thingspeak channel. Read/write implemented in a channel handler object.

Usage:
- Client: Send data by invoking the thingspeak.send() and thingspeak.transmit(). Send label or index as parameter to thingspeak.send(), index gets stored in a buffer (594 max values) and thingspeak.transmit() sends the buffer as one entry.
- Server: thingspeak.get() returns a dictionary - keys are labels, values are number of occurrences in across all entries in the channel. thingspeak.get_img() plots a bar graph.
