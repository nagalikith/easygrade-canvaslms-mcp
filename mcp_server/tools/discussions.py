

def register(server, client):

    @server.tool(
        name="canvas_list_discussion_topics",
        description="List all discussion topics in a course."
    )
    async def canvas_list_discussion_topics(course_id: int):
        return await client.listDiscussionTopics(course_id)

    @server.tool(
        name="canvas_get_discussion_topic",
        description="Get a specific discussion topic."
    )
    async def canvas_get_discussion_topic(course_id: int, topic_id: int):
        return await client.getDiscussionTopic(course_id, topic_id)

    @server.tool(
        name="canvas_post_to_discussion",
        description="Post a message to a discussion topic."
    )
    async def canvas_post_to_discussion(course_id: int, topic_id: int, message: str):
        return await client.postDiscussionEntry(course_id, topic_id, message)
