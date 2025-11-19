

def register(server, client):

    @server.tool(
        name="canvas_list_files",
        description="List all files in a course or folder."
    )
    async def canvas_list_files(course_id: int, folder_id: int = None):
        return await client.listFiles(course_id, folder_id)

    @server.tool(
        name="canvas_get_file",
        description="Get metadata for a specific file."
    )
    async def canvas_get_file(file_id: int):
        return await client.getFile(file_id)

    @server.tool(
        name="canvas_list_folders",
        description="List folders within a course."
    )
    async def canvas_list_folders(course_id: int):
        return await client.listFolders(course_id)
