

def register(server, client):

    @server.tool(
        name="canvas_list_assignment_groups",
        description="List all assignment groups for a course."
    )
    async def canvas_list_assignment_groups(course_id: int):
        return await client.listAssignmentGroups(course_id)
