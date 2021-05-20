"""Application definition."""
from zipfile import ZipExtFile
from bocadillo import App, discover_providers
from . import illnesses, precautions
import json
from datetime import date, datetime
from random import choice

app = App()
discover_providers("lepios_project_backend.providerconf")

# Create routes here.

feedback = [
    "Okay what else are you experiencing? It helps when you describe it a bit clear",
    "Interesting, what might you be feeling?",
    "Oh I see, so what else are you feeling?",
    "Do tell if you have more symptoms",
]


def sendMessage(message=None, choices=None, information=None):
    if message:
        sendingJSON = {
            "type": "message",
            "content": message,
            "sender": "bot",
            "timestamp": str(datetime.now()),
        }
        return json.dumps(sendingJSON)
    elif choices:
        sendingJSON = {
            "type": "choices",
            "choices": choices,
            "sender": "bot",
            "timestamp": str(datetime.now()),
            "active": True,
        }
        return json.dumps(sendingJSON)
    elif information:
        sendingJSON = {
            "type": "information",
            "choices": information,
            "sender": "bot",
            "timestamp": str(datetime.now()),
            "active": True,
        }
        return json.dumps(sendingJSON)


@app.websocket_route("test")
async def talker(ws, disease_prediction):
    async for message in ws:
        disease_prediction.input_symptoms([message])
        response = disease_prediction.predict()
        print(response)
        await ws.send(response)


@app.websocket_route("/conversation")
async def converse(ws, lepios, symptom_prediction, disease_prediction):
    consulting = False
    confirmed_symptoms = []
    current_question_pool = []
    last_question = False
    asking = False

    async for message in ws:

        if consulting:
            if last_question:
                if lepios.response(message, userID="283")[1] == "disagree":
                    asking = False
                    disease_prediction.input_symptoms(confirmed_symptoms)
                    diseases = disease_prediction.predict_top3()
                    results = []
                    for disease, accuracy in diseases:
                        try:
                            result = {
                                "name": disease,
                                "accuracy": accuracy,
                                "description": illnesses[disease],
                                "precautions": precautions[disease],
                            }
                            results.append(result)
                        except:
                            result = {
                                "name": disease,
                                "accuracy": accuracy,
                                "description": False,
                                "precautions": False,
                            }
                            results.append(result)
                    await ws.send(
                        sendMessage(
                            message="Based on our conversation these are the following illnesses that I picked up from my analysis, try clicking on one to get further information (Please note that my analysis are limited to the scope of information you've given me in our conversation)"
                        )
                    )

                    await ws.send(sendMessage(information=results))

                    await ws.send(
                        sendMessage(
                            message="Feel free to initiate another consultation with me 😄"
                        )
                    )

                    consulting = False
                elif lepios.response(message, userID="283")[1] == "agree":
                    last_question = False
                    asking = False
                    await ws.send(sendMessage(message=choice(feedback)))
                else:
                    response = lepios.response(message, userID="283")[0]
                    await ws.send(sendMessage(message=response))

            elif asking:
                if lepios.response(message, userID="283")[1] != "disagree":
                    confirmed_symptoms.append(message)
                    await ws.send(sendMessage(message="Feeling anything else? Y/N"))
                    last_question = True
                    asking = False
                else:
                    await ws.send(sendMessage(message=choice(feedback)))
                    asking = False

            else:
                responses = symptom_prediction.response(message, userID="203")
                asking = True
                current_question_pool = responses
                current_question_pool.append(["No", "None of these"])
                await ws.send(
                    sendMessage(message="Are you experiencing any of the following?")
                )
                await ws.send(sendMessage(choices=current_question_pool))

        else:
            response = lepios.response(message, userID="203")
            if response:
                if response[1] == "consultation":
                    consulting = True
                    await ws.send(sendMessage(message=response[0]))
                    await ws.send(
                        sendMessage("Feel free to end this consultation anytime")
                    )
                    await ws.send(
                        sendMessage(
                            "Let me know what you have been experiencing lately"
                        )
                    )
                elif response[1] == "agree":
                    await ws.send(sendMessage(message="I do not understand 😅"))
                else:
                    await ws.send(str(sendMessage(response[0])))
            else:
                await ws.send(sendMessage(message="I do not understand 😅"))