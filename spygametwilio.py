from time import sleep
from things import *
from twilio.rest import Client
from flask import Flask, Response, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse, Gather
import threading
app = Flask(__name__)
client = Client(account_sid, auth_token)
twilionumber = "+447411115128"
#from pygamelisten import nukeinterrupted, startApp
playername = ""
playernumber = ""
nukeinterrupted = ""
event = threading.Event()
second_task = ""


#THE CODES IN GAME#
interrupt_code = "Bernard"
master_computer_codes = ["Alpha", "Bravo", "Charlie", "Delta"]


def game_demo():
    print("Welcome to the game demo")
    sleep(2)
    welcome_text_message()


def welcome_text_message():
    message = client.messages \
                    .create(
                        body=f"Welcome Agent {playername}",
                        from_=twilionumber,
                        to=playernumber
                    )
    print("Welcome message sent")
    print(message.sid)
    sleep(2)
    first_mission_brief()


def first_mission_brief():
    message = client.messages \
                    .create(
                     body=f"Agent {playername}, terrorists have gained control of the nuclear launch codes and are targeting Gotham. Retrieve the emergency disarm code before the nuclear missiles hit.",
                     from_=twilionumber,
                     to=playernumber
                 )
    print("First mission brief sent")
    print(message.sid)
    sleep(2)
    first_mission_end()

#game level 1

def first_mission_end():
    message = client.messages \
                    .create(
                        body=f"We can see on our satellites that the terrorists are retreating back to their base so you must have caused some good chaos agent {playername}. Send over those interrupt code as soon as you can, the nuclear missiles are still coming this way",
                        from_=twilionumber,
                        to=playernumber
                    )
    print("First mission end sent")
    print(message.sid)
    event.wait()
    event.clear()
    first_mission_result()

#    first_mission_result()


def first_mission_result():
    if nukeinterrupted == 'y':
        sleep(5)
        second_mission_start()
    else:
        game_over()


def second_mission_start():
    message = client.messages \
                    .create(
                        body=f"Agent {playername}, your next mission is to infilrate the enemy base and retrieve the master computer passcodes undetected. Good Luck",
                        from_=twilionumber,
                        to=playernumber,
                    )
    print('second mission brief sent')
    print(message.sid)
    sleep(5)
    callout()

def callout():
    client.calls.create(
                        twiml=f'<Response><Gather input="speech" action="{ngrok_url}/completed"><Say>Agent {playername}, hurry. Please tell me the passcodes now!</Say></Gather></Response>',
                        to=playernumber,
                        from_=twilionumber
                    )
    event.wait()
    sleep(5)
    second_mission_result()


def second_mission_result():
    global second_task
    if second_task == "T":
        client.calls.create(
                        twiml=f'<Response><Say>Congratulations Agent {playername}. You have done well. Stay safe. You will hear from us soon.</Say></Response>',
                        to=playernumber,
                        from_=twilionumber
                    )
    else:
        client.calls.create(
                        twiml=f'<Response><Say>Agent {playername}, you have failed. The master computer was used to take over the world. Your Agent status has been revoked. Goodbye</Say></Response>',
                        to=playernumber,
                        from_=twilionumber
                    )
    game_over()

def game_over():
    print("Ur done")

######################## CODE FOR FLASK ######################################

@app.route("/sms", methods=['GET', 'POST'])
def incoming_nuke_interrupt_codes():
    global nukeinterrupted
    global interrupt_code
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    print(f'body: {body}')
    # Start our TwiML response
    resp = MessagingResponse()
    # Determine the right reply for this message
    if body == interrupt_code:
        nukeinterrupted = "y"
        resp.message(f"Congratulations Agent {playername}. We have used the code you sent us to reroute the nuclear missiles to land safely in the ocean. Stay safe Agent and wait for the next mission brief")
    else:
        resp.message("""This is an automated response. The incoming threat was not prevented. You have failed. Your Agent status has been revoked. Goodbye""")
    print("GOT SMS response")
    event.set()
    return str(resp)

# @app.route("/voice", methods=['GET', 'POST'])
# def voice():
#     response = VoiceResponse()
#     gather = Gather(action="/completed", input='speech', finishOnKey='#')
#     gather.say("Please read the code aloud")
#     response.append(gather)
    
#     print(response)
#     return(str(response))

@app.route("/completed", methods=['GET', 'POST'])
def compeleted():
    global second_task
    count = 0
    words = request.values.get("SpeechResult", None)
    print(words)
    print(request.values.get("Confidence", None))
    response = VoiceResponse()
    response.say(f"Thank you Agent {playername}")
    punc = '''!()-[];:'"\,<>./?@#$%^&*_~'''
    for ele in words:
        if ele in punc:
            words = words.replace(ele, "")
    said_words = words.split(" ")
    said_words = [i.capitalize() for i in said_words]
    for i in said_words:
        if i in master_computer_codes:
            count = count + 1
    if count == 4:
        second_task = "T"
    else:
        second_task = "F"
    print(second_task)
    event.set()
    return(str(response))

def startApp():
    app.run()




x = threading.Thread(target=startApp, daemon=True) 
x.start()
game_demo()
#callout()
x.join()