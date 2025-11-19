

def register(server, client):

    @server.tool(
        name="canvas_get_submission",
        description="Get a submission for an assignment."
    )
    async def canvas_get_submission(course_id: int, assignment_id: int, user_id: int = None):
        uid = user_id if user_id else "self"
        return await client.getSubmission(course_id, assignment_id, uid)

    @server.tool(
        name="canvas_submit_assignment",
        description="Submit work for an assignment."
    )
    async def canvas_submit_assignment(
        course_id: int,
        assignment_id: int,
        submission_type: str,
        **kwargs
    ):
        args = {
            "course_id": course_id,
            "assignment_id": assignment_id,
            "submission_type": submission_type,
            **kwargs
        }
        return await client.submitAssignment(args)

    @server.tool(
        name="canvas_submit_grade",
        description="Submit a grade for a student's assignment."
    )
    async def canvas_submit_grade(
        course_id: int,
        assignment_id: int,
        user_id: int,
        grade,
        **kwargs
    ):
        args = {
            "course_id": course_id,
            "assignment_id": assignment_id,
            "user_id": user_id,
            "grade": grade,
            **kwargs
        }
        return await client.submitGrade(args)
