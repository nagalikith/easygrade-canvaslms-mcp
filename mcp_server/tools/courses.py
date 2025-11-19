

def register(server, client):

    @server.tool(
        name="canvas_health_check",
        description="Check Canvas API health."
    )
    async def canvas_health_check():
        return await client.healthCheck()

    @server.tool(
        name="canvas_list_courses",
        description="List all Canvas courses."
    )
    async def canvas_list_courses(include_ended: bool = False):
        return await client.listCourses(include_ended)

    @server.tool(
        name="canvas_get_course",
        description="Get details about a specific course."
    )
    async def canvas_get_course(course_id: int):
        return await client.getCourse(course_id)

    
    @server.tool(
    name="canvas_create_course",
    description="Create a new Canvas course."
    )   
    async def canvas_create_course(
        account_id: int,
        name: str,
        course_code: str = None,
        start_at: str = None,
        end_at: str = None
    ):
        args = {
            "account_id": account_id,
            "name": name,
            "course_code": course_code,
            "start_at": start_at,
            "end_at": end_at,
        }
        # remove None values
        args = {k: v for k, v in args.items() if v is not None}
        return await client.createCourse(args)

    @server.tool(
        name="canvas_update_course",
        description="Update an existing Canvas course."
    )
    async def canvas_update_course(course_id: int, **kwargs):
        args = {"course_id": course_id, **kwargs}
        return await client.updateCourse(args)
