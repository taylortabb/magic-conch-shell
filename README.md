<!-- instructions

1. navigate to Magic-Conch diretory
2. activate virtualenv: $ source env/bin/activate
if you get caugth on grpcio install 1.9.9 or whatevber then run command

once audo works:::::::
googlesamples-assistant-hotword --project-id magic-conch-shell --device-model-id magic-conch-shell-pi 

also..

pip install playsound
 -->

# DO NOT FOLLOW THESE INSTRUCTIONS! THEY'RE TOTALLY INCOMPLETE AND ARE A WORK IN PROGRESS (DECEMBER 31ST 2018)
# A Real Magic Conch Shell

Ever wanted a Magic Conch Shell? Follow these instructions to build a Magic Conch Shell of your own.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine, as well as get the required hardware swt up to support the project.

### Parts

The hardware for this project is pretty simple, you'll just need the parts below:


* [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)
* [Pimorini Speaker pHat](https://shop.pimoroni.com/products/speaker-phat) - This is the compact speaker we'll use to let the shell speak
* USB microphone - This is a microphone. We need a very tiny one so it fits in a Conch shell. I used (https://www.amazon.com/gp/product/B01MQ2AA0X/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1)[this]
*  LiPo Battery - This will power the Pi in the shell, you'll want something with a small physical size, but at least 700mAh capacity. Adafruit has a great selection!
* [Adafruit PowerBoost 500 Charger](https://www.adafruit.com/product/1944) - This board allows us to power the board and charge the battery at the same time.
* A Conch Shell - A conch shell can be bought online, but if you're lucky enough to live near a beach, you might be able to find your own (NEVER collect a shell with a living organism in it! Queen Conch are susceptible to over-fishing, habitat degrdation, and deserve happy long lives. Check with your local laws before taking a shell from the beach.) Or consider 3D printing one yourself.

### Rasperry Pi Wi-Fi & SSH Setup

If your Raspberry Pi is already connected to Wi-Fi with SSH enabled, you can skip this step. Otherwise, your first step is to get your Raspberry Pi set up on wifi with SSH enabled. There's plenty of guides for this online. I think [this](https://learn.adafruit.com/raspberry-pi-zero-creation/install-os-on-to-sd-card) guide from Adafruit does a spectacular job!

## Software Setup

We'll be using Cloud Text-to-Speech API, Assistant SDK, and Snowboy to make this regular conch shell into something magic! Assistant SDK will allow the conch to respond to general inquiries, Cloud Text-to-Speech API will let us program the shell to give specific responses to questions like "what do we need to do to get out of the Kelp Forest?" and Snowboy will let us use "Magic Conch Shell" instead of "Okay Google" as the hotword.

### Google Cloud SDK Installation (Text-to-Speech API)

To use Text-to-Speech API, we'll need to install Google Cloud SDK. Google has a reallyy straightforward quickstart guide you can follow [here](https://cloud.google.com/sdk/docs/quickstart-linux). You just need to do from the start of "Before you begin" to the end of "Initialize the SDK." 

Note that when you're directed to run ```gcloud init``` you'll actually want to run ```gcloud init --console-only``` 

When you're promted to ```Pick cloud project to use:``` you'll most likely want to select the option to create a new project named ```magic-conch-shell```

Once that's all set up, we're ready to move on

### Google Assistant SDK for devices

To get Google Assistant running, you'll want to follow Google's documentation for getting the SDK set up on a Raspberry Pi [here](https://developers.google.com/assistant/sdk/guides/library/python/embed/setup) You'll want to start at "Set Up Hardware and Network Access" and go all the way to "Run the Sample Code." Read the rest of this section first for a few proccess notes.

At the "Configure and Test the Audio" step place the included .asoundrc in your home directory (/home/pi), or just type ```nano /home/pi.asoundrc``` and paste the below text.

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
When you get to the "Configure a Developer Project and Account Settings" step, you'll want to import the magic-conch-shell project we created before.

When you get to the "Install the SDK and Sample Code" step, first creaate a folder called magic-conch-shell in the home directory.

```mkdir Magic-Conch```
navigate into the directory
```cd Magic-Conch```
then follow the instructions for Python 2.7.

Note: If the installer takes more than 5 minutes creating wheels for grpcio (in the "Get the package" step), stop the installation (ctrl+c) and install grpcio independent from the SDK ```pip install grpcio==1.9.1``` then try the "Get the package" steps again.

### Snowboy Set Up

Finally we'll get Snowboy up and running. This is pretty straight forward....

### Break down into end to end tests

## Authors

* **Taylor Tabb** - [tabb.me](https://www.tabb.me/)


## License

This project is licensed under the CMU License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Shout out to OP, AH, EKH, and MR.
* Inspiration
* etc

