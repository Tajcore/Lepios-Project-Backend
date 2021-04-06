"""Application definition."""
from bocadillo import App, discover_providers
from . import illnesses, precautions

app = App()
discover_providers("lepios_project_backend.providerconf")

# Create routes here.


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
                if message == "N":
                    asking = False
                    disease_prediction.input_symptoms(confirmed_symptoms)
                    result = disease_prediction.predict()

                    await ws.send(
                        "Chances are you might be suffering from {disease}".format(
                            disease=result
                        )
                    )

                    try:
                        description = illnesses[result]
                        await ws.send(description[0])
                        await ws.send("I suggest you take the following precaution(s)")
                        print(precautions.keys(), result)
                        suggestion = ", ".join(precautions[result])
                        
                        await ws.send(suggestion)
                    except:
                        print("No info on that illness")
                        await ws.send(
                            "Seems I don't have much information on this illness, you can possibly find information regarding it online"
                        )

                    consulting = False
                else:
                    last_question = False
                    await ws.send("Okay what else are you experiencing?")

            elif asking:
                if message == "Y":
                    confirmed_symptoms.append(current_question_pool.pop(0)[0])
                    await ws.send("Feeling anything else?")
                    last_question = True
                else:
                    if len(current_question_pool) == 0:
                        asking = False
                        disease_prediction.input_symptoms(confirmed_symptoms)
                        result = disease_prediction.predict()
                        await ws.send(
                            "Chances are you might be suffering from {disease}".format(
                                disease=result
                            )
                        )
                        consulting = False
                    else:
                        current_question_pool.pop(0)
                        await ws.send(
                            str(
                                "are you experiencing {response}?".format(
                                    response=current_question_pool[0][1]
                                )
                            )
                        )
            else:
                responses = symptom_prediction.response(message, userID="203")
                print(responses)
                asking = True
                current_question_pool = responses
                await ws.send(
                    str(
                        "are you experiencing {response}?".format(
                            response=responses[0][1]
                        )
                    )
                )
        else:
            response = lepios.response(message, userID="203")
            if response[1] == "consultation":
                consulting = True
                await ws.send(str(response[0]))
                await ws.send("Feel free to end this consultation anytime")
            else:
                await ws.send(str(response[0]))
