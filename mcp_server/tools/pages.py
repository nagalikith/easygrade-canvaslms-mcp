

def register(server, client):

    @server.tool(
        name="canvas_list_pages",
        description="List all pages in a course."
    )
    async def canvas_list_pages(course_id: int):
        return await client.listPages(course_id)

    @server.tool(
        name="canvas_get_page",
        description="Retrieve a specific page by its slug."
    )
    async def canvas_get_page(course_id: int, page_url: str):
        return await client.getPage(course_id, page_url)
