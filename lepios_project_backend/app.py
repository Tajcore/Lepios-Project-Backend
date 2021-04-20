"""Application definition."""
from zipfile import ZipExtFile
from bocadillo import App, discover_providers
from . import illnesses, precautions
import json
from datetime import date, datetime

app = App()
discover_providers("lepios_project_backend.providerconf")

# Create routes here.


def sendMessage(message=None, choices=None):
    if message:
        sendingJSON = {
            "type": "message",
            "content": message,
            "sender": "bot",
            "timestamp": str(datetime.now()),
        }
        return json.dumps(sendingJSON)
    if choices:
        sendingJSON = {
            "type": "choices",
            "choices": choices,
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
                    result = disease_prediction.predict()
                    await ws.send(
                        sendMessage(
                            message="Chances are you might be suffering from {disease}".format(
                                disease=result
                            )
                        )
                    )

                    try:
                        description = illnesses[result]
                        await ws.send(sendMessage(message=description[0]))
                        await ws.send(
                            sendMessage(
                                message="I suggest you take the following precaution(s)"
                            )
                        )
                        print(precautions.keys(), result)
                        suggestion = ", ".join(precautions[result])

                        await ws.send(sendMessage(message=suggestion))
                    except:
                        print("No info on that illness")
                        await ws.send(
                            sendMessage(
                                message="Seems I don't have much information on this illness, you can possibly find information regarding it online"
                            )
                        )

                    consulting = False
                else:
                    last_question = False
                    await ws.send("Okay what else are you experiencing?")

            elif asking:
                if lepios.response(message, userID="283")[1] != "disagree":
                    confirmed_symptoms.append(message)
                    await ws.send(sendMessage(message="Feeling anything else?"))
                    last_question = True
                else:
                    await ws.send(sendMessage(message="Please describe clearly what you're experiencing"))

            else:
                responses = symptom_prediction.response(message, userID="203")
                asking = True
                current_question_pool = responses
                current_question_pool.append(["Nope","None of these"])
                await ws.send(
                    sendMessage(message="are you experiencing any of the following?")
                )
                await ws.send(sendMessage(choices=current_question_pool))

        else:
            response = lepios.response(message, userID="203")
            if response:
                if response[1] == "consultation":
                    consulting = True
                    await ws.send(sendMessage(message=response[0]))
                    await ws.send(sendMessage("Feel free to end this consultation anytime"))
                elif response[1] == "agree":
                    await ws.send(sendMessage(message="I do not understand ^_^'"))
                else:
                    await ws.send(str(sendMessage(response[0])))
            else:
                await ws.send(sendMessage(message="I do not understand ^_^'"))