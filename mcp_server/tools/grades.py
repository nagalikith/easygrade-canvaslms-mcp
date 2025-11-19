

def register(server, client):

    @server.tool(
        name="canvas_get_course_grades",
        description="Get grades for a specific course."
    )
    async def canvas_get_course_grades(course_id: int):
        return await client.getCourseGrades(course_id)

    @server.tool(
        name="canvas_get_user_grades",
        description="Get all grades for current user."
    )
    async def canvas_get_user_grades():
        return await client.getUserGrades()
