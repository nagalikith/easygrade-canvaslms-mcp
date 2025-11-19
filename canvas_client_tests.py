from mcp_server.client import CanvasClient
import os

client = CanvasClient(
    token=os.getenv("CANVAS_API_TOKEN"),
    domain="canvas.docker",
    scheme="http"
)

courses = client.get_courses()  # method depends on your client
print(courses)
