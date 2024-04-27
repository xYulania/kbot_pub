# importing libraries 
import json # convert and parse JavaScript Object Notation
import base64 # convert image to string
import time # add delay in program
import RPi.GPIO as GPIO # library to handle General Purpose Input/Output Pins in RasberryPi 

from Motor import PWM # to move the 4 wheels (Pulse Width Modulation)
from picamera2 import Picamera2 # to handle camera in RasberryPi
from playsound import playsound # to play the text-to-speach
from openai import OpenAI # OpenAI APIs library
from pathlib import Path # path

from servo import * # servo motor to control the head of the robot
pwm=Servo()

import os

#from Led import * # library to control LED lights
#led=Led()

def turn_robot_toward_angle_and_move(angle):
    if angle == 0:
        print ("kbot does not need to turn")
        PWM.setMotorModel(800,800,800,800)
        time.sleep(2)
        PWM.setMotorModel(0,0,0,0)
    elif angle == 90:
        print ("kbot is turning 90")
        PWM.setMotorModel(-1000,-1000,1500,1500)
        time.sleep(.6)
        PWM.setMotorModel(0,0,0,0)

        PWM.setMotorModel(800,800,800,800)
        time.sleep(2)
        PWM.setMotorModel(0,0,0,0)
    elif angle == 180:
        print ("kbot is turning 180")
        
        PWM.setMotorModel(-1000,-1000,1500,1500)
        time.sleep(.6)
        PWM.setMotorModel(0,0,0,0)
        
        PWM.setMotorModel(-1000,-1000,1500,1500)
        time.sleep(.6)
        PWM.setMotorModel(0,0,0,0)

        PWM.setMotorModel(800,800,800,800)
        time.sleep(2)
        PWM.setMotorModel(0,0,0,0)

    elif angle == 270:
        print ("kbot is turning 270")
        
        PWM.setMotorModel(-1000,-1000,1500,1500)
        time.sleep(.6)
        PWM.setMotorModel(0,0,0,0)
        
        PWM.setMotorModel(-1000,-1000,1500,1500)
        time.sleep(.6)
        PWM.setMotorModel(0,0,0,0)

        PWM.setMotorModel(-1000,-1000,1500,1500)
        time.sleep(.6)
        PWM.setMotorModel(0,0,0,0)

        PWM.setMotorModel(800,800,800,800)
        time.sleep(2)
        PWM.setMotorModel(0,0,0,0)
       

# function to convert image to string
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# function to make the robot speak with OpenAI API
def speak(text):
    parent_path = Path(__file__).parent
    speech_file_path = f"/home/kbot/kbot/Code/Server/speech.mp3"
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="alloy",
        input= text
    ) as response:
        response.stream_to_file(speech_file_path)
        os.system(f"mplayer {speech_file_path}")
        #playsound()

# function to get answer from openAI based on user prompt
def get_open_ai_vision_objects():
    base64_image = encode_image('./image.jpg')
    response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {
            "role": "user",
            "content": [
                {
                   "type": "text", "text": "Please return all objects in the image as JSON array only. Use the following format: [{'name': 'the object'}]"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    },
                },
            ],
            }
        ],
        max_tokens=300,
    )
    oai_res=(response.choices[0].message.content)

    oai_res = oai_res.replace("'",'''"''')

    return json.loads(oai_res)
    
def describe_objects():
    base64_image = encode_image('./image.jpg')
    response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {
            "role": "user",
            "content": [
                {
                   "type": "text", "text": "Please describe the following objects in 20 words for a person with visual impairment"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    },
                },
            ],
            }
        ],
        max_tokens=300,
    )
    oai_res=(response.choices[0].message.content)

    oai_res = oai_res.replace("'",'''"''')

    speak(oai_res)


# function to get the things based on a prompt
def get_open_ai_angle():
    
    response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {
            "role": "user",
            "content": [
                {
                   "type": "text", "text": f"based on this user input: {user_prompt}. which angle in the following json array matches what the user is asking for? reply with only the angle number only. if no angle found, reply with only -1. json array: {captures}"},
            ],
            }
        ],
        max_tokens=1000,
    )
    oai_res=(response.choices[0].message.content)
    
    oai_res = oai_res.replace("'",'''"''')

    return oai_res

# def start_led():
    # try:
        # led.ledIndex(0x01,255,255,255)      # white
        # led.ledIndex(0x02,0,0,255)          # blue
        # led.ledIndex(0x04,255,255,255)      # white
        # led.ledIndex(0x08,0,0,255)          # blue
        # led.ledIndex(0x10,255,255,255)      # white
        # led.ledIndex(0x20,0,0,255)          # blue
        # led.ledIndex(0x40,255,255,255)      # white
        # led.ledIndex(0x80,0,0,255)  
        # time.sleep(3)               
        # led.colorWipe(led.strip, Color(0,0,0))  #turn off the light
        # print ("\nEnd of program")
    # except KeyboardInterrupt:
        # led.colorWipe(led.strip, Color(0,0,0))  #turn off the light
        # print ("\nEnd of program")

def head_look_up():
    try:
        for i in range(50,110,1):
            pwm.setServoPwm('0',i)
            time.sleep(0.01)
    except KeyboardInterrupt:
        pwm.setServoPwm('0',90)
        pwm.setServoPwm('1',90)

def head_look_down():
    try:
        for i in range(110,50,-1):
            pwm.setServoPwm('0',i)
            time.sleep(0.01)
    except KeyboardInterrupt:
        pwm.setServoPwm('0',90)
        pwm.setServoPwm('1',90)
        print ("\nEnd of program")

def head_turn_right():
    try:
        for i in range(80,150,1):
            pwm.setServoPwm('1',i)
            time.sleep(0.01) 
    except KeyboardInterrupt:
        pwm.setServoPwm('0',90)
        pwm.setServoPwm('1',90)
        print ("\nEnd of program")

def head_turn_left():
    try:
        for i in range(150,80,-1):
            pwm.setServoPwm('1',i)
            time.sleep(0.01)   
    except KeyboardInterrupt:
        pwm.setServoPwm('0',90)
        pwm.setServoPwm('1',90)
        print ("\nEnd of program")

def head_reset():
    pwm.setServoPwm('0',90)
    pwm.setServoPwm('1',90)


# create OpenAI client with the API Secret key
client = OpenAI(
    api_key = "",
)

# define the main array to store captured objects or things
captures = [
    {
        "id": 1, # identifier of the angle
        "angle": 0, # the direction of rotation
        "things": [] # the things the AI captured in that direction
    },
    {
        "id": 2,
        "angle": 90,
        "things": []
    },
    {
        "id": 3,
        "angle": 180,
        "things": []
    },
    {
        "id": 4,
        "angle": 270,
        "things": []
    }
]

# prepare the camera
picam2 = Picamera2()

camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
picam2.start()
###################

# wait for user input
# example: find the chair
user_prompt = input('Please ask the robot about an object')
###################

# indicate that the robot started working
# start_led()
###################

for item in captures:
    time.sleep(1)
    # capture image from camera
    picam2.capture_file("./image.jpg")
    
    print("capture done for", item["id"])
    
    # describe objects
    describe_objects()
    
    # send image to open ai
    things = get_open_ai_vision_objects()
    
    # store objects in things
    item['things'] = things
    
    print('things captured', things)
    
    # turn the robot based on the angle
    print ("kbot is turning left")
    PWM.setMotorModel(-1000,-1000,1500,1500)
    time.sleep(.6)
    PWM.setMotorModel(0,0,0,0)

ang = get_open_ai_angle()

ang = int(ang)

if ang == -1:
    speak("Object not found")
else:
    print("angle found", ang)
    # get the response from openai and rotate the robot based on angle and move the robot foward 

    turn_robot_toward_angle_and_move(ang) 




