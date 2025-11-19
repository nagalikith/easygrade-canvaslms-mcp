

def register(server, client):

    @server.tool(
        name="canvas_get_user_profile",
        description="Get current user's profile."
    )
    async def canvas_get_user_profile():
        return await client.getUserProfile()

    @server.tool(
        name="canvas_update_user_profile",
        description="Update the current user's profile."
    )
    async def canvas_update_user_profile(**kwargs):
        return await client.updateUserProfile(kwargs)

    @server.tool(
        name="canvas_enroll_user",
        description="Enroll a user into a course."
    )
    async def canvas_enroll_user(course_id: int, user_id: int, **kwargs):
        args = {"course_id": course_id, "user_id": user_id, **kwargs}
        return await client.enrollUser(args)
