# SkyTap
There are many great sensors out there for measuring our environment but many of these only send data to a display for viewing without storing the data or making further use of it. This project uses a raspberry pi and python to intercept 433mHz weather data, store it, and display it on a local web-server. While these programs are set up for a specific sensor, the process can be used for innumerable sensor applications.

### Materials I'm using:
* Raspberry Pi 3 Model B running Raspbian
* Solderless Breadboard + jumper cables + ribbon cable ([Amazon](https://www.amazon.com/gp/product/B01LYN4J3B/ref=oh_aui_detailpage_o04_s00?ie=UTF8&psc=1))
* 433 Mhz Superheterodyne Wireless Receiver Module ([Amazon](https://www.amazon.com/gp/product/B06XHJMC82/ref=oh_aui_detailpage_o07_s00?ie=UTF8&psc=1))
* BME 280 Pressure Temperature Humidity Sensor ([Amazon](https://www.amazon.com/gp/product/B0118XCKTG/ref=oh_aui_detailpage_o05_s00?ie=UTF8&psc=1)) - For indoor measurements
* Acurite Weather Center model #00639W - For outdoor temperature, humidity, and wind speed

![Materials](https://github.com/codagras/SkyTap/blob/master/Images/IMG_1562.JPG)

### Step 1: Set up your Pi
* Download and install the latest version of Raspbian
* I completed everything by remote SSH from my laptop but I suppose you could hook up a monitor and keyboard.
* Many python libraries are required and may need installed as you go.
* Hook up the breadboard and wireless receiver module.  Supply 3V to power the receiver (even though it may say 5V, 5V will damage the GPIO pins).  I connected the data pin to GPIO23.  And finally, ground to ground.
* Download the SkyTap folder and put it in /home/pi

### Step 2: Test the receiver and find your wireless sensor
* Turn on your wireless sensor and make sure it's working (it helps to check the original display it's sending to).
* Use the simple python program Sniffer.py to record and plot a period of 433 Mhz signal.  If it's working your plot will be really messy looking with values going between 0 and 1 (I adapted this from someone else, once I remember I will reference them; I'm also working on a new version to search out the sensor's signal)
* Once your receiver is working and you can plot a signal you need to locate the part of the signal you are interested in, the sensors signal.  Compared to the rest of the signal it should be pretty consistent, with regular periods of low or high (0 or 1). [RaysHobby.net](https://rayshobby.net/reverse-engineer-wireless-temperature-humidity-rain-sensors-part-1/) has some useful insight.  The signal from my acurite signal looks like this (it's repeated twice):

![Signal Example](https://github.com/codagras/SkyTap/blob/master/Images/SignalEx.png)

### Step 3: Decode signal
* This is the tricky part.  If you happen to be using the same sensor as me, congrats, I've already done the decoding for you and you can skip this section. Otherwise, you'll need to determine how your sensor transmits the data.  Again, I found [RaysHobby.net](https://rayshobby.net/reverse-engineer-wireless-temperature-humidity-rain-sensors-part-1/) very helpful with this.  I'll describe my process for doing this to help. First, you will need to write out the signal in 1's and 0's. For my station, the first 4 'high' signals are for syncing (recognizing the sensor) and the actual transmission starts after that. 1's are usually a long 'high' followed by a short 'low'. 0's are the opposite.  See my example:

![Signal to Binary](https://github.com/codagras/SkyTap/blob/master/Images/SignalToBinary.jpg)

So the 'transmission' section of the signal lends 8 bytes of binary. Next, I recorded a good number of signals and compared the different bytes to the temperature, humidity and wind that was actually displayed.  This allowed me to figure out which bytes corresponded to the different variables (note: there are parity bits at the beginning of each byte for error checking. The humidity byte did not use a parity bit so that humidity could go up to 100).

![Decode Signal](https://github.com/codagras/SkyTap/blob/master/Images/Signal_Decode.jpg)

As you can see, humidity and wind were pretty simple.  Converting binary to base 10 gave the relative humidity (%) and wind speed (mph).   For temperature, I plotted the base 10 value against the actual temperature value in excel and found the relationship.  You can see that 180 corresponds to about 74.9 F using tempF = 0.1x + 56.891.

![decode temperature](https://github.com/codagras/SkyTap/blob/master/Images/decode_temp.png)

### Step 4: Edit SkyTap.py
Here I list sections of code in SkyTap.py that you may or may not need to edit. Look for these commented headings:
* Search for sync signal (usually a long high) - This is my first pass through the recorded signals to locate the sync signal.  In my case I search for a high signal that is longer than 90 (printing dx gives the length of of each high signal, my first value was usually around 100)
* Confirm sync - In this second pass, I check the rest of the sync signal which is 3 high signals between 15 and 30 in length.  Then I make sure the entire length of the signal (65 bits) has no big gaps by ignoring transmissions where low signal lengths (dy) that surpasses 35.
*  Convert confirmed signals to Binary - By displaying high signal lengths (dx) I picked a length that was between the length of a 1 and 0.  In my case 10 so that any high signal length less than 10 becomes a 0 and a signal length longer than 10 becomes a 1.  As another check, I point to the location of the sensor id and manually enter the correct id into the code at `if check == [1, 1, 0, . . . . ]`
* This section identifies the bits for temp, hum and wspd - Last, you need to point to the binary values of relative humidity, temperature (two parts in my case), and wspd (or whatever you sensor measures).
* Given humidity, temperature, and wind speed, the rest of the code calculates derived variables, saves the data into the data folder and displays data at http://localhost:8000 (using SimpleServer.py).  You can change specific behaviors by editing values within the settings section.  SkyTap will continue to listen and decode any received signal until it finds a good signal then will rest until the log interval has passed.  Each time data is logged, indoor temperature, humidity, and pressure is retrieved from the BME280 chip.  When SkyTap does not successfully retrieve one or more variables, they are logged as -999.
