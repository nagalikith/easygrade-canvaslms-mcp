

def register(server, client):

    @server.tool(
        name="canvas_list_announcements",
        description="List announcements for a course."
    )
    async def canvas_list_announcements(course_id: int):
        return await client.listAnnouncements(course_id)
