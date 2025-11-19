import httpx
import asyncio
from typing import Any, Dict, Optional, List, Union

from .errors import CanvasAPIError, CanvasValidationError


class CanvasClient:
    def __init__(
        self,
        token: str,
        domain: str,
        max_retries: int = 3,
        retry_delay: int = 1000,
        timeout: int = 30000,
    ):
        self.base_url = f"http://{domain}/api/v1"
        self.max_retries = max_retries
        self.retry_delay = retry_delay / 1000
        self.timeout = timeout / 1000

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=self.timeout,
        )

    async def _request(self, method: str, path: str, **kwargs):
        url = f"{self.base_url}{path}"

        for attempt in range(self.max_retries):
            try:
                response = await self.client.request(method, url, **kwargs)
                if response.status_code >= 400:
                    raise CanvasAPIError(
                        message=f"{method} {path} failed",
                        status_code=response.status_code,
                        response=response.text,
                    )
                return response.json()

            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                await asyncio.sleep(self.retry_delay)

    async def _paginate(self, method: str, path: str, **kwargs):
        results: List[Any] = []
        url = f"{self.base_url}{path}"

        while url:
            r = await self.client.request(method, url, **kwargs)
            if r.status_code >= 400:
                raise CanvasAPIError(
                    message=f"Pagination error on {path}",
                    status_code=r.status_code,
                    response=r.text,
                )

            results.extend(r.json())

            next_link = self._parse_next_link(r.headers.get("Link"))
            url = next_link

        return results

    def _parse_next_link(self, header: Optional[str]):
        if not header:
            return None
        parts = header.split(",")
        for part in parts:
            if 'rel="next"' in part:
                start = part.find("<") + 1
                end = part.find(">")
                return part[start:end]
        return None

    # ----------------------------------------------------
    # Core API groups mapped from your TS client
    # ----------------------------------------------------

    # ---------- Health ----------
    async def healthCheck(self):
        return {"status": "ok", "reachable": True}

    # ---------- Courses ----------
    async def listCourses(self, include_ended: bool = False):
        params = {
            "include[]": [
                "total_students",
                "teachers",
                "term",
                "course_progress",
            ]
        }
        if not include_ended:
            params["state[]"] = ["available", "completed"]

        return await self._paginate("GET", "/courses", params=params)

    async def getCourse(self, course_id: int):
        return await self._request("GET", f"/courses/{course_id}")

    async def createCourse(self, args: Dict[str, Any]):
        return await self._request("POST", f"/accounts/{args['account_id']}/courses", json={"course": args})

    async def updateCourse(self, args: Dict[str, Any]):
        cid = args["course_id"]
        body = {k: v for k, v in args.items() if k != "course_id"}
        return await self._request("PUT", f"/courses/{cid}", json={"course": body})

    # ---------- Assignments ----------
    async def listAssignments(self, course_id: int, include_submissions: bool = False):
        params = {}
        if include_submissions:
            params["include[]"] = ["submission"]
        return await self._paginate("GET", f"/courses/{course_id}/assignments", params=params)

    async def getAssignment(self, course_id: int, assignment_id: int, include_submission: bool = False):
        params = {}
        if include_submission:
            params["include[]"] = ["submission"]
        return await self._request("GET", f"/courses/{course_id}/assignments/{assignment_id}", params=params)

    async def createAssignment(self, args: Dict[str, Any]):
        cid = args["course_id"]
        body = {k: v for k, v in args.items() if k != "course_id"}
        return await self._request("POST", f"/courses/{cid}/assignments", json={"assignment": body})

    async def updateAssignment(self, args: Dict[str, Any]):
        cid = args["course_id"]
        aid = args["assignment_id"]
        body = {k: v for k, v in args.items() if k not in ("course_id", "assignment_id")}
        return await self._request("PUT", f"/courses/{cid}/assignments/{aid}", json={"assignment": body})

    # ---------- Assignment Groups ----------
    async def listAssignmentGroups(self, course_id: int):
        return await self._request("GET", f"/courses/{course_id}/assignment_groups")

    # ---------- Submissions ----------
    async def getSubmission(self, cid: int, aid: int, user_id: Union[int, str]):
        if user_id == "self":
            return await self._request("GET", f"/courses/{cid}/assignments/{aid}/submissions/self")
        return await self._request("GET", f"/courses/{cid}/assignments/{aid}/submissions/{user_id}")

    async def submitAssignment(self, args: Dict[str, Any]):
        cid = args["course_id"]
        aid = args["assignment_id"]
        body = {
            "submission": {
                "submission_type": args["submission_type"],
                "body": args.get("body"),
                "url": args.get("url"),
                "file_ids": args.get("file_ids"),
            }
        }
        return await self._request("POST", f"/courses/{cid}/assignments/{aid}/submissions", json=body)

    async def submitGrade(self, args: Dict[str, Any]):
        cid, aid, uid = args["course_id"], args["assignment_id"], args["user_id"]
        body = {
            "submission": {
                "posted_grade": args["grade"],
                "comment": {"text_comment": args.get("comment")},
            }
        }
        return await self._request("PUT", f"/courses/{cid}/assignments/{aid}/submissions/{uid}", json=body)

    # ---------- Files ----------
    async def listFiles(self, course_id: int, folder_id: Optional[int] = None):
        if folder_id:
            return await self._paginate("GET", f"/folders/{folder_id}/files")
        return await self._paginate("GET", f"/courses/{course_id}/files")

    async def getFile(self, file_id: int):
        return await self._request("GET", f"/files/{file_id}")

    async def listFolders(self, course_id: int):
        return await self._paginate("GET", f"/courses/{course_id}/folders")

    # ---------- Pages ----------
    async def listPages(self, course_id: int):
        return await self._paginate("GET", f"/courses/{course_id}/pages")

    async def getPage(self, course_id: int, page_url: str):
        return await self._request("GET", f"/courses/{course_id}/pages/{page_url}")

    # ---------- Calendar ----------
    async def listCalendarEvents(self, start_date: Optional[str], end_date: Optional[str]):
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return await self._paginate("GET", "/calendar_events", params=params)

    async def getUpcomingAssignments(self, limit: int = 10):
        events = await self._paginate("GET", "/users/self/upcoming_events")
        return events[:limit]

    # ---------- Dashboard ----------
    async def getDashboard(self):
        return await self._request("GET", "/dashboard/dashboard_cards")

    async def getDashboardCards(self):
        return await self._request("GET", "/dashboard/dashboard_cards")

    # ---------- Grades ----------
    async def getCourseGrades(self, course_id: int):
        return await self._request("GET", f"/courses/{course_id}/enrollments")

    async def getUserGrades(self):
        return await self._paginate("GET", "/users/self/enrollments")

    # ---------- User Profile ----------
    async def getUserProfile(self):
        return await self._request("GET", "/users/self/profile")

    async def updateUserProfile(self, body: Dict[str, Any]):
        return await self._request("PUT", "/users/self/profile", json={"user": body})

    # ---------- Enrollment ----------
    async def enrollUser(self, args: Dict[str, Any]):
        cid = args["course_id"]
        body = {
            "enrollment": {
                "user_id": args["user_id"],
                "type": args.get("role"),
                "enrollment_state": args.get("enrollment_state", "active"),
            }
        }
        return await self._request("POST", f"/courses/{cid}/enrollments", json=body)

    # ---------- Account Management ----------
    async def getAccount(self, account_id: int):
        return await self._request("GET", f"/accounts/{account_id}")

    async def listAccountCourses(self, args: Dict[str, Any]):
        aid = args["account_id"]
        return await self._paginate("GET", f"/accounts/{aid}/courses", params=args)

    async def listAccountUsers(self, args: Dict[str, Any]):
        aid = args["account_id"]
        return await self._paginate("GET", f"/accounts/{aid}/users", params=args)

    async def createUser(self, args: Dict[str, Any]):
        aid = args["account_id"]
        return await self._request("POST", f"/accounts/{aid}/users", json=args)

    async def listSubAccounts(self, account_id: int):
        return await self._paginate("GET", f"/accounts/{account_id}/sub_accounts")

    async def getAccountReports(self, account_id: int):
        return await self._paginate("GET", f"/accounts/{account_id}/reports")

    async def createAccountReport(self, args: Dict[str, Any]):
        aid = args["account_id"]
        report = args["report"]
        return await self._request("POST", f"/accounts/{aid}/reports/{report}", json=args)
