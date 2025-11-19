

def register(server, client):

    @server.tool(
        name="canvas_get_dashboard",
        description="Get a user's Canvas dashboard info."
    )
    async def canvas_get_dashboard():
        return await client.getDashboard()

    @server.tool(
        name="canvas_get_dashboard_cards",
        description="Get dashboard course cards."
    )
    async def canvas_get_dashboard_cards():
        return await client.getDashboardCards()
