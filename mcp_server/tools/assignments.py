

def register(server, client):

    @server.tool(
        name="canvas_list_assignments",
        description="List assignments for a course."
    )
    async def canvas_list_assignments(course_id: int, include_submissions: bool = False):
        return await client.listAssignments(course_id, include_submissions)

    @server.tool(
        name="canvas_get_assignment",
        description="Get a specific assignment with optional submission data."
    )
    async def canvas_get_assignment(course_id: int, assignment_id: int, include_submission: bool = False):
        return await client.getAssignment(course_id, assignment_id, include_submission)

    @server.tool(
        name="canvas_create_assignment",
        description="Create a new assignment in a course."
    )
    async def canvas_create_assignment(
        course_id: int,
        name: str,
        **kwargs
    ):
        args = {"course_id": course_id, "name": name, **kwargs}
        return await client.createAssignment(args)

    @server.tool(
        name="canvas_update_assignment",
        description="Update an existing assignment."
    )
    async def canvas_update_assignment(course_id: int, assignment_id: int, **kwargs):
        args = {"course_id": course_id, "assignment_id": assignment_id, **kwargs}
        return await client.updateAssignment(args)
