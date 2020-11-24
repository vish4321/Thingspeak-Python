#TO ADAPT THIS FOR ANY OBJECT DETECTION APPLICATION, CHANGE ONLY THESE VALUES
#These four values can be found on your Thingspeak profile
channel_ID='1235685'
write_API='TPB1N6LRBAHTXJP1'
read_API='PGD7HSTN6AHXLA8F'
clear_API='FZ49PDSPUD979SE1'

#This is a label map for the Tensorflow Object Detection API. Ensure list index corresponds to class label; if the labels start from 1, add a leading 'null' to this list.
#Warning: make sure the list length is no greater than 98.
label_map = ['null','plane', 'baseball-diamond', 'bridge', 'ground-track-field', 'small-vehicle', 'large-vehicle', 'ship', 'tennis-court', 'basketball-court', 'storage-tank', 'soccer-ball-field', 'roundabout', 'harbor', 'swimming-pool', 'helicopter']
