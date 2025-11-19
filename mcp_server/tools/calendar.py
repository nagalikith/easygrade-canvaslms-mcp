

def register(server, client):

    @server.tool(
        name="canvas_list_calendar_events",
        description="List calendar events in a date range."
    )
    async def canvas_list_calendar_events(start_date: str = None, end_date: str = None):
        return await client.listCalendarEvents(start_date, end_date)

    @server.tool(
        name="canvas_get_upcoming_assignments",
        description="Get upcoming assignments (sorted by due date)."
    )
    async def canvas_get_upcoming_assignments(limit: int = 10):
        return await client.getUpcomingAssignments(limit)
