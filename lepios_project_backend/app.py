"""Application definition."""
from bocadillo import App, discover_providers

app = App()
discover_providers("lepios_project_backend.providerconf")

# Create routes here.


@app.websocket_route("/conversation")
async def converse(ws, lepios, symptom_prediction):
    consulting = False
    confirmed_symptoms = []
    current_question_pool = []
    asking = False
    async for message in ws:

        if consulting:
            if asking:
                if message == "Y":
                    confirmed_symptoms.append(current_question_pool.pop(0)[0])
                    
                    asking = False
                else:
                    if len(current_question_pool) == 0:
                        asking = False
                    else:
                        current_question_pool.pop(0)
                        await ws.send(str('are you experiencing {response}?'.format(
                            response=current_question_pool[0][1])))
            else:
                responses = symptom_prediction.response(message, userID='203')
                print(responses)
                asking = True
                current_question_pool = responses
                await ws.send(str('are you experiencing {response}?'.format(response=responses[0][1])))
        else:
            response = lepios.response(message, userID='203')
            if response[1] == 'consultation':
                consulting = True
                await ws.send(str(response[0]))
                await ws.send("Feel free to end this consultation anytime")
            else:
                await ws.send(str(response[0]))
