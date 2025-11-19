from typing import NewType
from enum import Enum

CourseId = NewType("CourseId", int)
AssignmentId = NewType("AssignmentId", int)
UserId = NewType("UserId", int)
EnrollmentId = NewType("EnrollmentId", int)


# Course states
class CanvasCourseState(str, Enum):
    UNPUBLISHED = "unpublished"
    AVAILABLE = "available"
    COMPLETED = "completed"
    DELETED = "deleted"


# Grading type
class CanvasGradingType(str, Enum):
    PASS_FAIL = "pass_fail"
    PERCENT = "percent"
    LETTER_GRADE = "letter_grade"
    GPA_SCALE = "gpa_scale"
    POINTS = "points"


# Submission types
class CanvasSubmissionType(str, Enum):
    NONE = "none"
    TEXT = "online_text_entry"
    URL = "online_url"
    UPLOAD = "online_upload"
    MEDIA = "media_recording"
    ANNOTATION = "student_annotation"


# Submission state
class CanvasSubmissionState(str, Enum):
    SUBMITTED = "submitted"
    UNSUBMITTED = "unsubmitted"
    GRADED = "graded"
    PENDING_REVIEW = "pending_review"


# Enrollment type
class CanvasEnrollmentType(str, Enum):
    STUDENT = "StudentEnrollment"
    TEACHER = "TeacherEnrollment"
    TA = "TaEnrollment"
    DESIGNER = "DesignerEnrollment"
    OBSERVER = "ObserverEnrollment"


# Enrollment state
class CanvasEnrollmentState(str, Enum):
    ACTIVE = "active"
    INVITED = "invited"
    INACTIVE = "inactive"
    COMPLETED = "completed"
    REJECTED = "rejected"


# Module state
class CanvasModuleState(str, Enum):
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    STARTED = "started"
    COMPLETED = "completed"


# Module item type
class CanvasModuleItemType(str, Enum):
    FILE = "File"
    PAGE = "Page"
    DISCUSSION = "Discussion"
    ASSIGNMENT = "Assignment"
    QUIZ = "Quiz"
    SUBHEADER = "SubHeader"
    EXTERNAL_URL = "ExternalUrl"
    EXTERNAL_TOOL = "ExternalTool"


# Quiz type
class CanvasQuizType(str, Enum):
    PRACTICE = "practice_quiz"
    ASSIGNMENT = "assignment"
    GRADED_SURVEY = "graded_survey"
    SURVEY = "survey"
