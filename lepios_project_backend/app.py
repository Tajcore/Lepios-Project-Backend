"""Application definition."""
from bocadillo import App, discover_providers

app = App()
discover_providers("lepios_project_backend.providerconf")

# Create routes here.


@app.websocket_route("/conversation")
async def converse(ws, lepios):
    async for message in ws:
        response = lepios.response(message, userID='203')
        await ws.send(str(response))
