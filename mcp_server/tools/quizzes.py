

def register(server, client):

    @server.tool(
        name="canvas_list_quizzes",
        description="List all quizzes in a course."
    )
    async def canvas_list_quizzes(course_id: int):
        return await client.listQuizzes(course_id)

    @server.tool(
        name="canvas_get_quiz",
        description="Get details of a specific quiz."
    )
    async def canvas_get_quiz(course_id: int, quiz_id: int):
        return await client.getQuiz(course_id, quiz_id)

    @server.tool(
        name="canvas_create_quiz",
        description="Create a new quiz within a course."
    )
    async def canvas_create_quiz(
        course_id: int,
        title: str,
        **kwargs
    ):
        args = {"course_id": course_id, "title": title, **kwargs}
        return await client.createQuiz(args)

    @server.tool(
        name="canvas_start_quiz_attempt",
        description="Start a new quiz attempt."
    )
    async def canvas_start_quiz_attempt(course_id: int, quiz_id: int):
        return await client.startQuizAttempt(course_id, quiz_id)
