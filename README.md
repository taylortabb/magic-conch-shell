<!-- instructions

1. navigate to Magic-Conch diretory
2. activate virtualenv: $ source env/bin/activate
if you get caugth on grpcio install 1.9.9 or whatevber then run command

once audo works:::::::
googlesamples-assistant-hotword --project-id magic-conch-shell --device-model-id magic-conch-shell-pi 

also..

pip install playsound
 -->

DO NOT FOLLOW THESE INSTRUCTIONS! THEY'RE TOTALLY INCOMPLETE AND ARE A WORK IN PROGRESS (JANUARY 23RD 2018)

# A Real Magic Conch Shell

Ever wanted a Magic Conch Shell? Follow these instructions to build a Magic Conch Shell of your own.

My goal for this project was to create a real life version of a Magic Conch Shell, made famous in Spongebob Squarepants. The steps below will get you going with conch shell just like mine. 

Magic Conch Shell 2.0 has all the same functionality of a regular conch shell, but has all the power of Google Assistant. Ask magic conch shell about the weather, sports scores, to controll your smart home, or almost anything else you would ask your Assistant enabled smartphone or Google Home to do.


And, just like the Conch shell from Spongebob Squarepants, this conch responds to all the questions asked of it in the episode [Club Spongebob](http://spongebob.wikia.com/wiki/Club_SpongeBob/transcript). 



Using Google Assistant, the conch shell has essentially all the 

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

### Rasperry Pi Image, Wi-Fi, & SSH Setup

To start, you'll want to download the latest AIY image for your Pi from [here](https://github.com/google/aiyprojects-raspbian/releases). You're looking for a .img.xz file. Then you'll want to flash the image to the microSD card for the Pi-- I like using the free application [BalenaEtcher](https://www.balena.io/etcher/) for this.

If you know how to get your Raspberry Pi is connected to Wi-Fi with SSH enabled, you can skip the rest of this step. 

Otherwise, your next step is to get your Raspberry Pi set up on wifi with SSH enabled. 

Mount your microSD card, and in a Terminal, navigate to the directory. Most likely, you can just type
```
$ cd /Volumes/boot
```
create the file wpa_supplicant.conf (this will replace the RPi wifi config on boot)
```
$ nano wpa_supplicant.conf
```
past the following into the file
```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
       ssid="ssid"
       psk="password"
       key_mgmt=WPA-PSK
    }
```
but adjust "US" to your country code, and the psk, ssid, and key_mgmt variables to match your network. For a network without a password use this set up:
```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
       ssid="ssid"
       key_mgmt=NONE
    }
```
save this file, close it, and then enable ssh with the following command
```
$ touch ssh
```
Now, on boot, your Pi will connect to the specified netwwork with SSH enabled! 

# Hardware Setup

With the power off (unplugged) we'll want to first connect the components in the following way:

|image|

Note that you can leave the Conch Shell on and plugged in, or unplugged for a short duration and running on battery power.


# Software Setup

We'll be using Google AIY, Snowboy, Cloud Text-to-Speech API, and a couple Python libraries to make this regular conch shell into magic! AIY will allow the conch to respond to general inquiries with Google Assistant, Cloud Text-to-Speech API will let us generate the audio the shell will speak for specific responses to questions like "what do we need to do to get out of the Kelp Forest?" and Snowboy will let us use "Magic Conch Shell" instead of "Okay Google" as the hotword.

From now on, all steps assume you are SSH into your Pi.

<!-- ### Google Assistant SDK for devices

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

Note: If the installer takes more than 5 minutes creating wheels for grpcio (in the "Get the package" step), stop the installation (ctrl+c) and install grpcio independent from the SDK ```pip3 install grpcio==1.9.1``` then ```python -m pip install google-assistant-sdk[samples]```  -->
### AIY Set-up 

Head to google's AIY site and follow the instrucitons to [Get Credentials](https://aiyprojects.withgoogle.com/voice/#google-assistant--get-credential).

Then run
```
voice/assistant_grpc_demo.py
 ```
and follow the prompts to give permission and confirm your account. At this point, we don't expect assistant to work, so don't worry that it can't hear you. Exit the script with ```ctl+c```


### Google Cloud SDK Installation (Optional)


**This step is very very optional-- I've already included the synthesized audio files from Cloud Text-To-Speech API, so you only need to do this step if you want to play around with TTS API yourself, or if you want to experiment with other GCP tools.**

To use Text-to-Speech API, we'll need to install Google Cloud SDK. Google has a reallyy straightforward quickstart guide you can follow [here](https://cloud.google.com/sdk/docs/quickstart-linux). You just need to do from the start of "Before you begin" to the end of "Initialize the SDK." 

Note that when you're directed to run ```gcloud init``` you'll actually want to run ```gcloud init --console-only``` 

When you're promted to ```Pick cloud project to use:``` you'll most likely want to select the option to create a new project- name this project whatever you want, I named mine ```magic-conch-shell```

Once that's all set up, we're ready to move on

### Speaker pHAT + Microphone Configuration

Pimorini has a simple one-line installer for the speaker pHAT! Just enter:
```
curl -sS https://get.pimoroni.com/speakerphat | bash
```
And you're ready to bump some audio. Test your speaker pHat with the following command

```
aplay /home/pi/Pimoroni/speakerphat/test/test.wav
```

AIY is expecting us to be using Google's Voice Bonnet for sound, so we need to make a few changes to the Pi's audio configuration. 
```
sudo nano /boot/config.txt
```
and near the bottom of the file, change the line
```#dtparam=audio=on``` to ```dtparam=audio=on```

It's possible your file may already have this configuration.

Now we modify asound.conf
```
sudo nano /etc/asound.conf
```

and replace the content of this file with the following (Which i found thanks to [Circuit Beard](https://circuitbeard.co.uk/)!)

```
pcm.!default {
  type asym
  capture.pcm "mic"
  playback.pcm "speaker"
}

ctl.!default {
    type hw
    card 0
}

pcm.mic {
  type plug
  slave.pcm "hw:1,0"
}

pcm.speaker {
  type plug
  slave.pcm "softvol"
}

pcm.dmixer {
    type dmix
    ipc_key 1024
    ipc_perm 0666
    slave.pcm 'hw:0,0'
    slave {
        period_time 0
        period_size 1024
        buffer_size 8192
    }
    bindings {
        0 0
        1 1
    }
}

ctl.dmixer {
    type hw
    card 0
}

pcm.softvol {
    type softvol
    slave.pcm "dmixer"
    control {
        name "PCM"
        card 0
    }    
}
```

### Snowboy Set Up

Finally we'll need to get Snowboy up and running. Snowboy is an awesome tool for adding custom hotword detection. In our case, we want to replace "Okay Google..." and "Hey Google..." with "Magic Conch Shell..." 

We'll be using [Snowboy API for AIY Voice Kit](https://github.com/senyoltw/custom-hotword-for-aiy-voicekit#diff-original-programaiy-voice-kit-press-button-snowboy-wakeword-program)

Follow Senyoltw's steps entering each line as shown below
```
cd /home/pi/
sudo apt-get install libatlas-base-dev
git clone https://github.com/senyoltw/custom-hotword-for-aiy-voiceki
cp -ipr custom-hotword-for-aiy-voicekit/mod AIY-projects-python/src/
cp -ip custom-hotword-for-aiy-voicekit/assistant_grpc_demo_snowboy.py AIY-projects-python/src/examples/voice/
cd AIY-voice-kit-python
chmod a+x src/examples/voice/assistant_grpc_demo_snowboy.py
```
To create your custom "Magic Conch Shell" wake word, head to [snowboy.kitt.ai](https://snowboy.kitt.ai), make an account and.....

## Starting the Conch Shell.

And we're ready to speak to the magic conch! Download the contents of this repo to you home directory:

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

