# Thingspeak-Python
A module to store and retrieve Object Detection data on a Thingspeak channel.

Change the data in thingspeak_params.py; you will need the API keys that Thingspeak gives you, as well as the label map.
The module works by encoding strings using numbers and sending the numbers over the channel. At the receiver side, while reading, the module counts occurrences of each type of encoded data stored. The encoding-decoding relationship is stored in a label map list in thingspeak_params.py. Though this was developed particularly for object detection applications, it can also be used for any application where there are a predefined, finite set of strings/data that need to be encoded and stored efficiently (one Thingspeak entry stores 594 encoded entries). 

If the output needs to be processed some other way (other than counting the instances and returning a dict object), then everything after the JSON parsing line in the get() method needs to be modified.

Run the demo to see how to use it.
