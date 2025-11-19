

def register(server, client):

    @server.tool(
        name="canvas_list_modules",
        description="List all modules in a course."
    )
    async def canvas_list_modules(course_id: int):
        return await client.listModules(course_id)

    @server.tool(
        name="canvas_get_module",
        description="Get a specific module."
    )
    async def canvas_get_module(course_id: int, module_id: int):
        return await client.getModule(course_id, module_id)

    @server.tool(
        name="canvas_list_module_items",
        description="List items in a module."
    )
    async def canvas_list_module_items(course_id: int, module_id: int):
        return await client.listModuleItems(course_id, module_id)

    @server.tool(
        name="canvas_get_module_item",
        description="Get a specific module item."
    )
    async def canvas_get_module_item(course_id: int, module_id: int, item_id: int):
        return await client.getModuleItem(course_id, module_id, item_id)

    @server.tool(
        name="canvas_mark_module_item_complete",
        description="Mark a module item as completed."
    )
    async def canvas_mark_module_item_complete(course_id: int, module_id: int, item_id: int):
        return await client.markModuleItemComplete(course_id, module_id, item_id)
