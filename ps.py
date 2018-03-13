#!/usr/bin/env python

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import rospy
from std_msgs.msg import String
import sys
import time
import os

# obtain audio from the microphone
r = sr.Recognizer()

#ROS declarations

pub = rospy.Publisher('/speech/string', String, queue_size=10)
rospy.init_node('speech_recognizer', anonymous=True)

def start():
    # recognize speech using Google Speech Recognition
    while True:
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            recognizedString = r.recognize_google(audio)
            print("Google Speech Recognition thinks you said " + recognizedString)
            speechMessage = String()
            speechMessage.data = recognizedString
            pub.publish(speechMessage)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        if(recognizedString == 'salir'):
            sys.exit('saliendo!')
            break

        time.sleep(2)

if __name__ == '__main__':
    try:
        start()
    except rospy.ROSInterruptException:
        pass
