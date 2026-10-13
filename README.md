# Rocky

**An interactive robot version of Rocky from *Project Hail Mary*: he sees you, hears you, greets you, and works out the room he's in.**

Rocky is the alien engineer from the film: curious, loyal, and clever with whatever tools he has. This project is my attempt to build him for real, as a robot that exists in the room with you rather than a chatbot in a window. He should feel like the character (same personality as the movie) while also being a proper engineering platform for vision, speech, sensing and walking.

> **Status: work in progress.** The brain (hearing, seeing, speaking) runs as separate working modules. I'm now joining them into one loop and prototyping the body.

## The goal

Walk into the room and Rocky notices you, turns to look, and says hi. Over time he should recognise people, make sense of his surroundings, and react like Rocky would. Eventually he walks around on his own legs.

## What's built so far

| Part | File | What it does |
|---|---|---|
| Ears | `audio.py` | Listens through the microphone, detects when someone is speaking, turns it into text with Whisper, and checks for the wake word "rocky". |
| Eyes | `vision.py` | Reads a live camera stream with OpenCV, finds faces, and shows what Rocky hears on screen. Includes a function that sends a camera frame and a question to a local vision model. |
| Voice | `voice.py` | Speaks out loud with text-to-speech. |

### How the pieces talk

```
 microphone                                camera stream
     |                                          |
  audio.py                                  vision.py
  - voice activity detection (webrtcvad)    - OpenCV face detection
  - Whisper speech-to-text                  - "Rocky Eyes" display window
  - wake word "rocky"                       - Llama 3.2 Vision via Ollama
     |                                          ^
     |   local TCP socket (localhost:9999)      |
     +------------------------------------------+

 voice.py  ->  speaker
```

- **Only listens when someone speaks.** `webrtcvad` spots real speech, so Whisper isn't running on background noise.
- **Filters Whisper's made-up phrases.** Whisper tends to invent things like "thank you" on near-silence, so those are thrown away.
- **Separate modules joined by sockets.** Each part runs on its own and can be restarted or swapped without breaking the rest.
- **Runs locally.** The language and vision models run through [Ollama](https://ollama.com) on my laptop, with no cloud needed.

## The body

Still being designed and prototyped. The parts I'm working with:

- **ESP32 boards:** several, including camera boards and ones able to run small models, so some of Rocky's senses can live on the robot itself
- **Servos** for the legs and head
- **Sensors** for finding his way around
- **Laptop for now, Raspberry Pi later:** the software runs on my laptop today and will move onto the robot once it's solid

Rocky walks on multiple legs rather than wheels, so the gait is one of the main design challenges.

## Roadmap

- [x] Wake word listening with Whisper and voice activity detection
- [x] Live camera feed with face detection
- [x] Text-to-speech output
- [x] Socket link between modules (receiving side working, sending call switched off while I debug)
- [ ] One loop: hear, look, think, answer, speak
- [ ] Rocky's personality from the film, with memory of who he's met
- [ ] Rocky's speech style and his musical, whale-like sounds
- [ ] Face-tracking head movement
- [ ] Obstacle and surroundings sensing
- [ ] Multi-leg walking gait
- [ ] Move the software onto the robot (Raspberry Pi / ESP32)

## Setup

Tested with Python 3 on a MacBook.

```bash
pip install openai-whisper sounddevice numpy webrtcvad ollama opencv-python pyttsx3
ollama pull llama3.2-vision
```

1. In `vision.py`, set the camera address to your own stream URL.
2. Copy `haarcascade_frontalface_default.xml` into the project folder (it ships with OpenCV).
3. In `audio.py`, set `device=` to your microphone (`python -m sounddevice` lists them).

## Running

Start the vision script first, because it hosts the socket the others connect to:

```bash
python vision.py     # opens the "Rocky Eyes" window (press q to quit)
python audio.py      # prints "Rocky listening..." and what it hears
python voice.py      # test the voice
```

## Known issues

- `vision.py` has a placeholder camera address.
- The call that sends speech from `audio.py` to `vision.py` is commented out while I fix the connection handling.
- The vision model function exists but isn't yet called from the main loop.
- The text-to-speech voice name needs to match a voice installed on the machine.

## Why Rocky?

I take a lot of my project ideas from films and cartoons. Before Rocky I built a WALL-E rover and turrets based on Killjoy from Valorant. Rocky is the hardest one yet: a character with a real personality who has to see, hear, talk and walk. That's what makes it a good challenge, and it pulls together everything I'm learning in robotics.

## Related projects

- **KochuTV:** live webcam video streamed over UDP to an ESP32 and OLED display
- **WALL-E rover** and **turret** (Arduino)

## Author

Aman Shooja, BEng Robotics Engineering, University of Plymouth.
