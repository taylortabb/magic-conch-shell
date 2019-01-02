<!-- instructions

1. navigate to Magic-Conch diretory
2. activate virtualenv: $ source env/bin/activate
if you get caugth on grpcio install 1.9.9 or whatevber then run command

once audo works:::::::
googlesamples-assistant-hotword --project-id magic-conch-shell --device-model-id magic-conch-shell-pi 

also..

pip install playsound
 -->

DO NOT FOLLOW THESE INSTRUCTIONS! THEY'RE TOTALLY INCOMPLETE AND ARE A WORK IN PROGRESS (DECEMBER 31ST 2018)


Assistant first, then GCP

export GOOGLE_APPLICATION_CREDENTIALS="magic-conch-shell-f53082ab5098.json" each session

# A Real Magic Conch Shell

Ever wanted a Magic Conch Shell? Follow these instructions to build a Magic Conch Shell of your own.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine, as well as get the required hardware swt up to support the project.

### Parts

The hardware for this project is pretty simple, you'll just need the parts below:


* [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)
* [Pimorini Speaker pHat](https://shop.pimoroni.com/products/speaker-phat) - This is the compact speaker we'll use to let the shell speak
* USB microphone - This is a microphone. We need a very tiny one so it fits in a Conch shell. I used [this](https://www.amazon.com/gp/product/B01MQ2AA0X/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1)
*  LiPo Battery - This will power the Pi in the shell, you'll want something with a small physical size, but at least 700mAh capacity. Adafruit has a great selection!
* [Adafruit PowerBoost 500 Charger](https://www.adafruit.com/product/1944) - This board allows us to power the board and charge the battery at the same time.
* A Conch Shell - There's a bunch of options for a Conch shell. You can 3D print one, buy one online, or if you're lucky enough to live near a beach, you might be able to find your own! If you find your own, NEVER collect a shell with a living organism in it! Queen Conch are susceptible to over-fishing, habitat degrdation, and deserve happy long lives. Check with your local laws before taking a shell from the beach.

### Rasperry Pi Wi-Fi & SSH Setup

If your Raspberry Pi is already connected to Wi-Fi with SSH enabled, you can skip this step. 

Otherwise, your first step is to get your Raspberry Pi set up on wifi with SSH enabled. There's plenty of guides for this online. I think [this](https://learn.adafruit.com/raspberry-pi-zero-creation/install-os-on-to-sd-card) guide from Adafruit does a spectacular job!

From this point on, we'll assume you have access to your Pi through SSH.


# Hardware Setup

With the power off (unplugged) we'll want to first connect the components in the following way:

|image|

Note that you can leave the Conch Shell on and plugged in, or unplugged for a short duration and running on battery power.


# Software Setup

We'll be using Assistant SDK, Snowboy, Cloud Text-to-Speech API, and a couple Python modules to make this regular conch shell into magic! Assistant SDK will allow the conch to respond to general inquiries, Cloud Text-to-Speech API will let us program the shell to give specific responses to questions like "what do we need to do to get out of the Kelp Forest?" and Snowboy will let us use "Magic Conch Shell" instead of "Okay Google" as the hotword.


### Google Assistant SDK for devices

To get Google Assistant running, you'll want to follow Google's documentation for installing the SDK on a Raspberry Pi [here](https://developers.google.com/assistant/sdk/guides/library/python/embed/setup) 

Start at "Set Up Hardware and Network Access" and go all the way to "Run the Sample Code." *Read the rest of this section first for a few proccess notes.*

* At the "Configure and Test the Audio" step place the included .asoundrc in your home directory (/home/pi), or just type ```nano /home/pi.asoundrc``` and paste the below text.

	```
	pcm.!default {
	  type asym
	  capture.pcm "mic"
	  playback.pcm "speaker"
	}
	pcm.mic {
	  type plug
	  slave {
	    pcm "hw:<card number>,<device number>"
	  }
	}
	pcm.speaker {
	  type plug
	  slave {
	    pcm "hw:<card number>,<device number>"
	  }
	}
	```
* When you get to the "Configure a Developer Project and Account Settings" step, you'll want to import the magic-conch-shell project we created before. Ideally, follow the instructions for Python 3.

Note: If the installer takes more than 5 minutes creating wheels for grpcio (in the "Get the package" step), stop the installation (ctrl+c) and install grpcio independent from the SDK ```pip3 install grpcio==1.9.1``` then ```python -m pip install google-assistant-sdk[samples]``` 

### Google Cloud SDK Installation (Optional)


**This step is optional-- I've already included the synthesized audio files from Cloud Text-To-Speech API, so you only need to do this step if you want to play around with TTS API yourself, or if you want to experiment with other GCP tools.**

To use Text-to-Speech API, we'll need to install Google Cloud SDK. Google has a reallyy straightforward quickstart guide you can follow [here](https://cloud.google.com/sdk/docs/quickstart-linux). You just need to do from the start of "Before you begin" to the end of "Initialize the SDK." 

Note that when you're directed to run ```gcloud init``` you'll actually want to run ```gcloud init --console-only``` 

When you're promted to ```Pick cloud project to use:``` you'll most likely want to select the option to create a new project- name this project whatever you want, I named mine ```magic-conch-shell```

Once that's all set up, we're ready to move on

### Snowboy Set Up

Finally we'll get Snowboy up and running. Snowboy is an awesome tool for adding custom hotword detection. In our case, we want to replace "Okay Google..." and "Hey Google..." with "Magic Conch Shell..." 

This is pretty straight forward....


## Starting the Conch Shell.

Finally, we're ready to speak to the magic conch. Download the contents of this repo to you home directory:

``` cd /home/pi
git clone https://github.com/taylortabb/magic-conch-shell.git
```

Then make magic_conch.py executable:
``` 
cd magic-conch-shell
sudo chmod +x magic_conch.py
``` 
At this point, we can test it out! Just enter ```./magic_conch.py``` to run the script.

### Test out some commands 
Try saying these out loud:

**"Magic Conch Shell, what's the weather like in Los Angeles?"**
The expected outuput should be a description of the weather in LA.

**"Magic Conch Shell, will we ever get out of this kelp forest?"**
The expected outuput should be "maybe someday."

Assuming these both work, we know Assistant SDK and Snowboy are both working!

Now let's shut down the system and get all the hardware in it's final assembly.
``` sudo shutdown now``` 

## Putting it in the shell...

So now that it's all together, we've got to get it **in** the conch shell. The easiest way i've found is with double sided tape (I like 3M™ VHB™) and tweezers.

Once it's in, you're good to go! Your very own Magic Conch Shell. 

## Powering On

To get everyhing going... 

1. Plug in power (the Pi may already be on if the battery is charged). 
2. SSH into your Pi. If you've lost track of the IP address, you can use a tool like (LanScan)[LanScan] to find the Pi on your network.
3. Activate the virtual environment
```source env/bin/activate``` 
4. Navigate to the correct directory: ```cd /home/pi/magic-conch-shell``` 
4. Start magic-conch.py: ``` ./magic-conch.py```

At this point, try asking you Magic Conch Shell a question! If all seems good, you can close your SSH session. **Your Magic Conch is ready to use :)**

## Authors

* **Taylor Tabb** - [tabb.me](https://www.tabb.me/)


## License

This project is licensed under the CMU License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Shout out to OP, AH, EKH, and MR.
* Inspiration
* etc

