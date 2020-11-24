import urllib.request
import urllib.parse
import json
import collections
import matplotlib.pyplot as plt
import requests
import time
import thingspeak_params

'''
Put "import thingspeak" or "from Thingspeak import channel" near the top of your python file.
This module gives you a few functions to communicate over a specific Thingspeak channel.
The channel is an object; which means it must be declared as one and methods must be called as members of the declared object.

METHODS:
X =channel(): 	Constructor
X.send(item):  	Buffer for data that need to be sent over the channel.
                Either send the index or the label, either way only index is sent across the channel.
X.transmit(): 	Transmits everything in the buffer sequentially.
X.get():	Returns a dictionary that maps labels to the number of occurrences across all entries in the channel.
X.get_table():	Calls the get() method, and presents the items as a table.
X.get_img():	Calls the get() method, and then plots the key-value pairs on a bar graph
X.clear():	Clears all messages in the channel.

USEFUL MEMBERS:
X.read_url:	    Copy-paste the result of this (when you run it in python3 interpreter) to see all JSON objects added in the
                    channel.
X.numberOfMessages: Number of messages (not entries; 1 entry takes up to 594 messages) in the channel. Gets synced each time a
                    transmit() method is called, or at the time of instantiation.
X.itemlist:         Current unsent buffer
'''

class channel:

    def __init__(self):
        self.channel_ID = thingspeak_params.channel_ID
        self.write_API = thingspeak_params.write_API
        self.read_API = thingspeak_params.read_API
        self.clear_API = thingspeak_params.clear_API
        self.label_map = thingspeak_params.label_map

        self.itemlist = []	#Buffer for sending messages
        self.read_url = 'https://api.thingspeak.com/channels/' + self.channel_ID + '/feeds.json?api_key=' + self.read_API

	#Retrieve the last entry made, and convert the returned JSON object to dictionary
        url = 'https://api.thingspeak.com/channels/' + self.channel_ID + '/feeds/last?api_key=' + self.read_API
        f = urllib.request.urlopen(url)
        if f.getcode() is 200:
            print('Connection successful...')
        else:
            print('Connection unsuccessful. Aborting.')
		
        data = json.load(f)
        if data is -1:
            print('Channel opened')
            self.numberOfMessages = 0
            return

        try:
            if data is -1:
                self.numberOfMessages = 0
            if int(data.get('field8')) > 0:
                self.numberOfMessages = int(data.get('field8'))
            else:
                self.numberOfMessages = data.get('field8')
        except:
            print('Number not recognised')
            print('Unrecognised pre-existing data. Clearing channel...')
            self.clear()
            self.numberOfMessages = 0

        print('Channel opened')


    #function to return last entry. Useful for debug purposes, so let it remain.
    def get_last_entry(self):
        url = 'https://api.thingspeak.com/channels/' + self.channel_ID + '/feeds/last?api_key=' + self.read_API
        f = urllib.request.urlopen(url)
        data = json.load(f)
        return data

    #Add object to buffer
    def send(self,item):
        try:
            if item > len(self.label_map):
                print('No corresponding label for index '+str(item)+'. Invalid input.')
                return
        except:
            if item in self.label_map:
                item = self.label_map.index(item)
            else:
                print('Invalid input.')
                return

        #Append to a list. Note: one entry can only send 91 objects at a time, so we send 90 objects in one time.
        self.itemlist.append(str(item))
        print(self.label_map[item] +' added to buffer')
        if len(self.itemlist) >= 594:
            print('Buffer full! Transmitting data...')
            self.transmit()



    def transmit(self):
        #Get the length of the item array
        #string = 2 characters; word = 85 strings; block = 7 words; 1 block = 1 entry.
        length = len(self.itemlist)
        i = 0
        itemwords = [None]*7

	#Split up the items in the buffer into words (i.e, lists of 85 strings).
	#buffer can be expressed as 85x+y (if less than 91). x will be number of words; y also forms a word, managed by the part outside the while loop.
        while(i < length//85):
            itemwords[i] = ','.join(self.itemlist[i*85:(i+1)*85])
            i += 1

        if length%85 is not 0:
            itemwords[i] = ','.join(self.itemlist[-(length%85):])
        url_end = ''
        k = 0
        while k<=i and  itemwords[k] is not None:
            url_end += '&field'+str(k+1)+'='+itemwords[k]
            k += 1

        last_data = self.get_last_entry()
        self.numberOfMessages = int(last_data.get('field8'))
        

        #The last field is for cumulative total of objects, not regular data.
        url_end += '&field8=' + str(length + self.numberOfMessages)

        #Create the URL from the processing done above, and send it using HTTPS GET.
        url = 'https://api.thingspeak.com/update.json?api_key=' + self.write_API + url_end
        f = urllib.request.urlopen(url)

	#On the offhand chance that you call the transmit() twice within 15 seconds of each other.
        returndata = json.load(f)
        if returndata is 0:
            while(returndata is 0):
                print('15 second delay between messages for free Thingspeak account.\nRetrying...')
                time.sleep(15)
                f = urllib.request.urlopen(url)
                returndata = json.load(f)

        self.numberOfMessages += length

        self.itemlist = []
	
        if f.getcode() is 200:
            print('Transmission successful...')
        else:
            print('Transmission unsuccessful. Aborting...')
            return

    def get(self):
        #Read all entries made in the last 24 hours. Returns a JSON.
        f = urllib.request.urlopen(self.read_url)
        data = json.load(f)
        c = collections.Counter()
        itemwords = [None]*7
        for feed in data.get('feeds'):
            for i in range(7):
                if feed.get('field'+str(i+1)) is not None:
                    itemwords[i] = feed.get('field'+str(i+1)).split(',')
                    c.update(itemwords[i])

        finaldict = {}
        for i,j in c.items():
            finaldict[str(self.label_map[int(i)])] = j

        return finaldict

    def get_table(self):
        if self.numberOfMessages <= 0:
            print('No entries. Aborting...')
            return

        print("Count".rjust(9), "Name")
        print("\n".join(f'{v:9,} {k}' for k,v in self.get().items()))

    def get_img(self):
        if self.numberOfMessages <= 0:
            print('No entries. Aborting...')
            return

        print('Opening bar graph...')
        keys, values = zip(*self.get().items())
        fig=plt.figure(figsize=(10,5))

        plt.bar(keys, values, color='maroon', width=0.4)
        plt.xlabel('Objects')
        plt.ylabel('Occurrences')
        plt.title('Representation of object occurrence')
        plt.show()
        print('Bar graph closed.')
    
    def clear(self):
        url = 'https://api.thingspeak.com/channels/'+self.channel_ID+'/feeds.json?api_key='+self.clear_API
        response = requests.delete(url)
        self.numberOfMessages = 0
        if response.status_code is 200:
            print('Channel cleared.')
        else:
            print('Error in clearing the channel. Aborting.')



















