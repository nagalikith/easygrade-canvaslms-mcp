def register_course_tools(server, client):
    from .courses import register
    register(server, client)

def register_assignment_tools(server, client):
    from .assignments import register
    register(server, client)

def register_assignment_group_tools(server, client):
    from .assignment_groups import register
    register(server, client)

def register_submission_tools(server, client):
    from .submissions import register
    register(server, client)

def register_module_tools(server, client):
    from .modules import register
    register(server, client)

def register_discussion_tools(server, client):
    from .discussions import register
    register(server, client)

def register_announcement_tools(server, client):
    from .announcements import register
    register(server, client)

def register_quiz_tools(server, client):
    from .quizzes import register
    register(server, client)

def register_file_tools(server, client):
    from .files import register
    register(server, client)

def register_page_tools(server, client):
    from .pages import register
    register(server, client)

def register_calendar_tools(server, client):
    from .calendar import register
    register(server, client)

def register_dashboard_tools(server, client):
    from .dashboard import register
    register(server, client)

def register_grade_tools(server, client):
    from .grades import register
    register(server, client)

def register_user_tools(server, client):
    from .users import register
    register(server, client)

def register_account_tools(server, client):
    from .accounts import register
    register(server, client)
