

def register(server, client):

    @server.tool(
        name="canvas_get_account",
        description="Get details for a Canvas account."
    )
    async def canvas_get_account(account_id: int):
        return await client.getAccount(account_id)

    @server.tool(
        name="canvas_list_account_courses",
        description="List courses in an account."
    )
    async def canvas_list_account_courses(account_id: int, **kwargs):
        args = {"account_id": account_id, **kwargs}
        return await client.listAccountCourses(args)

    @server.tool(
        name="canvas_list_account_users",
        description="List all users in an account."
    )
    async def canvas_list_account_users(account_id: int, **kwargs):
        args = {"account_id": account_id, **kwargs}
        return await client.listAccountUsers(args)

    @server.tool(
        name="canvas_create_user",
        description="Create a user in an account."
    )
    async def canvas_create_user(account_id: int, user: dict, pseudonym: dict, **kwargs):
        args = {
            "account_id": account_id,
            "user": user,
            "pseudonym": pseudonym,
            **kwargs,
        }
        return await client.createUser(args)

    @server.tool(
        name="canvas_list_sub_accounts",
        description="List sub-accounts for an account."
    )
    async def canvas_list_sub_accounts(account_id: int):
        return await client.listSubAccounts(account_id)

    @server.tool(
        name="canvas_get_account_reports",
        description="List available reports."
    )
    async def canvas_get_account_reports(account_id: int):
        return await client.getAccountReports(account_id)

    @server.tool(
        name="canvas_create_account_report",
        description="Generate an account-level report."
    )
    async def canvas_create_account_report(account_id: int, report: str, parameters: dict = None):
        args = {
            "account_id": account_id,
            "report": report,
            "parameters": parameters or {},
        }
        return await client.createAccountReport(args)
