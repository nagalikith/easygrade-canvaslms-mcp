import json

# ---------------------------------------------------------
# URI parsing
# ---------------------------------------------------------
def parse_uri(uri: str):
    if "://" not in uri:
        raise ValueError(f"Invalid resource URI: {uri}")
    prefix, id_part = uri.split("://", 1)
    return prefix, id_part


# ---------------------------------------------------------
# Resource registry
# ---------------------------------------------------------
RESOURCE_HANDLERS = {}


def register(prefix: str, handler):
    RESOURCE_HANDLERS[prefix] = handler


def get_handler(prefix: str):
    return RESOURCE_HANDLERS.get(prefix)


# ---------------------------------------------------------
# Handlers (mirror of your TS ReadResourceRequest logic)
# ---------------------------------------------------------
async def handle_health(_id, client):
    return await client.health_check()


async def handle_courses(_id, client):
    return await client.list_courses()


async def handle_course(id_str, client):
    return await client.get_course(int(id_str))


async def handle_assignments(id_str, client):
    return await client.list_assignments(int(id_str), include_submissions=True)


async def handle_modules(id_str, client):
    return await client.list_modules(int(id_str))


async def handle_discussions(id_str, client):
    return await client.list_discussion_topics(int(id_str))


async def handle_announcements(id_str, client):
    return await client.list_announcements(int(id_str))


async def handle_quizzes(id_str, client):
    return await client.list_quizzes(int(id_str))


async def handle_pages(id_str, client):
    return await client.list_pages(int(id_str))


async def handle_files(id_str, client):
    return await client.list_files(int(id_str))


async def handle_dashboard(_id, client):
    return await client.get_dashboard()


async def handle_profile(_id, client):
    return await client.get_user_profile()


async def handle_upcoming(_id, client):
    return await client.get_upcoming_assignments()


# ---------------------------------------------------------
# Register them all in one shot
# ---------------------------------------------------------
def register_resources():
    register("canvas", handle_health)
    register("courses", handle_courses)
    register("course", handle_course)
    register("assignments", handle_assignments)
    register("modules", handle_modules)
    register("discussions", handle_discussions)
    register("announcements", handle_announcements)
    register("quizzes", handle_quizzes)
    register("pages", handle_pages)
    register("files", handle_files)
    register("dashboard", handle_dashboard)
    register("profile", handle_profile)
    register("calendar", handle_upcoming)


# ---------------------------------------------------------
# attach to MCP server
# ---------------------------------------------------------
def attach_resource_handlers(server, client):
    register_resources()

    @server.resource("canvas://{uri}")
    async def read_resource(uri: str):
        try:
            prefix, id_part = parse_uri(uri)
            handler = get_handler(prefix)

            if handler is None:
                return {
                    "uri": uri,
                    "mimeType": "application/json",
                    "text": json.dumps(
                        {"error": f"unknown prefix {prefix}"}, indent=2
                    )
                }

            data = await handler(id_part, client)

            return {
                "uri": uri,
                "mimeType": "application/json",
                "text": json.dumps(data, indent=2)
            }

        except Exception as e:
            return {
                "uri": uri,
                "mimeType": "application/json",
                "text": json.dumps({"error": str(e)}, indent=2)
            }
