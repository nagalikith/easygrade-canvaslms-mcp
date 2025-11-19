from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from .types import (
    CourseId, AssignmentId, UserId, EnrollmentId,
    CanvasCourseState, CanvasSubmissionType,
    CanvasSubmissionState, CanvasGradingType,
    CanvasEnrollmentType, CanvasEnrollmentState,
    CanvasModuleState, CanvasModuleItemType,
    CanvasQuizType,
)


class PaginatedResponse(BaseModel):
    data: List[Any]
    hasMore: bool
    nextPage: Optional[str] = None


class CanvasUser(BaseModel):
    id: UserId
    name: str
    sortable_name: str
    short_name: str
    sis_user_id: Optional[str]
    email: str
    avatar_url: str
    login_id: Optional[str] = None


class CanvasUserProfile(BaseModel):
    id: int
    name: str
    sortable_name: str
    short_name: str
    sis_user_id: Optional[str]
    login_id: str
    avatar_url: str
    primary_email: str
    locale: str
    bio: Optional[str]
    title: Optional[str] = None
    time_zone: Optional[str] = None
    calendar: Optional[Any] = None


class CanvasTerm(BaseModel):
    id: int
    name: str
    start_at: Optional[str]
    end_at: Optional[str]


class CanvasCourseProgress(BaseModel):
    requirement_count: int
    requirement_completed_count: int
    next_requirement_url: Optional[str]
    completed_at: Optional[str]


class CanvasCourse(BaseModel):
    id: CourseId
    name: str
    course_code: str
    workflow_state: CanvasCourseState
    account_id: int
    start_at: Optional[str]
    end_at: Optional[str]
    enrollments: Optional[List["CanvasEnrollment"]] = None
    total_students: Optional[int] = None
    syllabus_body: Optional[str] = None
    term: Optional[CanvasTerm] = None
    course_progress: Optional[CanvasCourseProgress] = None


class CanvasGrades(BaseModel):
    current_score: Optional[float]
    final_score: Optional[float]
    current_grade: Optional[str]
    final_grade: Optional[str]
    override_score: Optional[float] = None
    override_grade: Optional[str] = None


class CanvasSubmissionComment(BaseModel):
    id: int
    comment: str
    created_at: str
    author_id: int
    author_name: str
    attachments: Optional[List["CanvasFile"]] = None


class CanvasRubricAssessment(BaseModel):
    __root__: Dict[str, Dict[str, Any]]


class CanvasSubmission(BaseModel):
    id: int
    assignment_id: AssignmentId
    user_id: UserId
    submitted_at: Optional[str]
    score: Optional[float]
    grade: Optional[str]
    attempt: int
    workflow_state: CanvasSubmissionState
    body: Optional[str] = None
    url: Optional[str] = None
    attachments: Optional[List["CanvasFile"]] = None
    submission_comments: Optional[List[CanvasSubmissionComment]] = None
    rubric_assessment: Optional[CanvasRubricAssessment] = None
    late: bool
    missing: bool


class CanvasAssignmentGroup(BaseModel):
    id: int
    name: str
    position: int
    weight: float
    assignments: Optional[List["CanvasAssignment"]] = None
    group_weight: float


class CanvasRubricRating(BaseModel):
    id: str
    description: str
    long_description: str
    points: float


class CanvasRubricCriterion(BaseModel):
    id: str
    description: str
    long_description: str
    points: float
    criterion_use_range: bool
    ratings: List[CanvasRubricRating]


class CanvasRubric(BaseModel):
    id: int
    title: str
    context_id: int
    context_type: str
    points_possible: float
    reusable: bool
    public: bool
    read_only: bool
    free_form_criterion_comments: bool
    criteria: List[CanvasRubricCriterion]


class CanvasRubricSettings(BaseModel):
    points_possible: float
    free_form_criterion_comments: bool
    hide_score_total: Optional[bool] = None
    hide_points: Optional[bool] = None


class CanvasAssignment(BaseModel):
    id: AssignmentId
    course_id: CourseId
    name: str
    description: Optional[str]
    due_at: Optional[str]
    lock_at: Optional[str]
    unlock_at: Optional[str]
    points_possible: float
    position: int
    submission_types: List[CanvasSubmissionType]
    assignment_group_id: int
    assignment_group: Optional[CanvasAssignmentGroup] = None
    rubric: Optional[List[CanvasRubric]] = None
    rubric_settings: Optional[CanvasRubricSettings] = None
    allowed_extensions: Optional[List[str]] = None
    submission: Optional[CanvasSubmission] = None
    html_url: str
    published: bool
    grading_type: CanvasGradingType


class CanvasEnrollment(BaseModel):
    id: EnrollmentId
    user_id: UserId
    course_id: CourseId
    type: CanvasEnrollmentType
    role: str
    enrollment_state: CanvasEnrollmentState
    grades: Optional[CanvasGrades] = None
    user: Optional[CanvasUser] = None
    observed_users: Optional[List[CanvasUser]] = None


class CanvasDiscussionTopic(BaseModel):
    id: int
    title: str
    message: str
    html_url: str
    posted_at: str
    assignment_id: Optional[int]
    assignment: Optional[CanvasAssignment]
    discussion_type: str
    require_initial_post: bool
    user_has_posted: bool
    discussion_subentry_count: int
    read_state: str
    unread_count: int


class CanvasModuleItemContentDetails(BaseModel):
    points_possible: Optional[float] = None
    due_at: Optional[str] = None
    unlock_at: Optional[str] = None
    lock_at: Optional[str] = None


class CanvasModuleItemCompletionRequirement(BaseModel):
    type: str
    min_score: Optional[float] = None
    completed: bool


class CanvasModuleItem(BaseModel):
    id: int
    title: str
    type: CanvasModuleItemType
    module_id: int
    position: int
    indent: int
    html_url: str
    url: Optional[str] = None
    page_url: Optional[str] = None
    external_url: Optional[str] = None
    content_id: Optional[int] = None
    content_details: Optional[CanvasModuleItemContentDetails] = None
    completion_requirement: Optional[CanvasModuleItemCompletionRequirement] = None
    published: bool


class CanvasModule(BaseModel):
    id: int
    name: str
    position: int
    unlock_at: Optional[str]
    require_sequential_progress: bool
    prerequisite_module_ids: List[int]
    state: CanvasModuleState
    completed_at: Optional[str]
    items_count: int
    items_url: str
    items: Optional[List[CanvasModuleItem]] = None


class CanvasQuiz(BaseModel):
    id: int
    title: str
    html_url: str
    quiz_type: CanvasQuizType
    assignment_id: Optional[int]
    time_limit: Optional[int]
    published: bool
    description: Optional[str]
    due_at: Optional[str]
    lock_at: Optional[str]
    unlock_at: Optional[str]
    points_possible: float
    question_count: int
    allowed_attempts: int
    scoring_policy: str
    show_correct_answers: bool
    show_correct_answers_at: Optional[str]
    hide_correct_answers_at: Optional[str]
    shuffle_answers: bool
    has_access_code: bool
    ip_filter: Optional[str]
    locked_for_user: bool
    lock_explanation: Optional[str]


class CanvasAnnouncement(BaseModel):
    id: int
    title: str
    message: str
    posted_at: str
    html_url: str
    user_has_posted: bool
    discussion_subentry_count: int

class CanvasScope(BaseModel):
    resource: str
    resource_name: str
    controller: str
    action: str
    verb: str
    scope: str

class CanvasAssignmentSubmission(BaseModel):
    id: int
    submission_type: str
    body: Optional[str] = None
    url: Optional[str] = None
    submitted_at: Optional[str]
    assignment_id: int
    user_id: int
    workflow_state: str
    file_ids: Optional[List[int]] = None
    attachments: Optional[List["CanvasFile"]] = None

class CanvasPage(BaseModel):
    page_id: int
    url: str
    title: str
    body: str
    created_at: str
    updated_at: str
    published: bool
    front_page: bool
    locked_for_user: bool
    lock_explanation: Optional[str] = None
    editing_roles: str
    html_url: str

class CanvasCalendarEvent(BaseModel):
    id: int
    title: str
    start_at: str
    end_at: str
    description: str
    location_name: Optional[str] = None
    location_address: Optional[str] = None
    context_type: str
    context_id: int
    workflow_state: str
    hidden: bool
    url: Optional[str] = None
    html_url: str
    all_day: bool
    assignment: Optional["CanvasAssignment"] = None

class CanvasRubricSettings(BaseModel):
    points_possible: float
    free_form_criterion_comments: bool
    hide_score_total: Optional[bool] = None
    hide_points: Optional[bool] = None

class CanvasConversationParticipant(BaseModel):
    id: int
    name: str
    full_name: str
    avatar_url: str


class CanvasConversationMessage(BaseModel):
    id: int
    created_at: str
    body: str
    author_id: int
    generated: bool
    media_comment: Optional[Any] = None
    forwarded_messages: Optional[List["CanvasConversationMessage"]] = None
    attachments: Optional[List["CanvasFile"]] = None


class CanvasConversation(BaseModel):
    id: int
    subject: str
    workflow_state: str
    last_message: str
    last_message_at: str
    last_authored_message: str
    last_authored_message_at: str
    message_count: int
    subscribed: bool
    private: bool
    starred: bool
    properties: List[str]
    audience: List[int]
    audience_contexts: Dict[str, List[str]]
    avatar_url: str
    participants: List[CanvasConversationParticipant]
    messages: Optional[List[CanvasConversationMessage]] = None

class CanvasNotification(BaseModel):
    id: int
    title: str
    message: str
    html_url: str
    type: str
    read_state: bool
    created_at: str
    updated_at: str
    context_type: str
    context_id: int

class CanvasFile(BaseModel):
    id: int
    uuid: str
    folder_id: int
    display_name: str
    filename: str
    content_type: str
    url: str
    size: int
    created_at: str
    updated_at: str
    unlock_at: Optional[str] = None
    locked: bool
    hidden: bool
    lock_at: Optional[str] = None
    hidden_for_user: bool
    thumbnail_url: Optional[str] = None
    modified_at: str
    mime_class: str
    media_entry_id: Optional[str] = None
    locked_for_user: bool
    lock_explanation: Optional[str] = None
    preview_url: Optional[str] = None

class CanvasSyllabus(BaseModel):
    course_id: int
    syllabus_body: str

class CanvasDashboardCard(BaseModel):
    id: int
    shortName: str
    originalName: str
    courseCode: str
    assetString: str
    href: str
    term: Optional["CanvasTerm"] = None
    subtitle: str
    enrollmentType: str
    observee: Optional[str] = None
    image: Optional[str] = None
    color: str
    position: Optional[int] = None


class CanvasPlannerItem(BaseModel):
    context_type: str
    context_name: str
    planner_date: str
    submissions: bool
    plannable_id: int
    plannable_type: str
    plannable: Dict[str, Any]
    html_url: str
    completed: bool


class CanvasDashboard(BaseModel):
    dashboard_cards: List[CanvasDashboardCard]
    planner_items: List[CanvasPlannerItem]

class CreateCourseArgs(BaseModel):
    account_id: int
    name: str
    course_code: Optional[str] = None
    start_at: Optional[str] = None
    end_at: Optional[str] = None
    license: Optional[str] = None
    is_public: Optional[bool] = None
    is_public_to_auth_users: Optional[bool] = None
    public_syllabus: Optional[bool] = None
    public_syllabus_to_auth: Optional[bool] = None
    public_description: Optional[str] = None
    allow_student_wiki_edits: Optional[bool] = None
    allow_wiki_comments: Optional[bool] = None
    allow_student_forum_attachments: Optional[bool] = None
    open_enrollment: Optional[bool] = None
    self_enrollment: Optional[bool] = None
    restrict_enrollments_to_course_dates: Optional[bool] = None
    term_id: Optional[int] = None
    sis_course_id: Optional[str] = None
    integration_id: Optional[str] = None
    hide_final_grades: Optional[bool] = None
    apply_assignment_group_weights: Optional[bool] = None
    time_zone: Optional[str] = None
    syllabus_body: Optional[str] = None

class UpdateCourseArgs(CreateCourseArgs):
    course_id: int

class CreateAssignmentArgs(BaseModel):
    course_id: int
    name: str
    description: Optional[str] = None
    due_at: Optional[str] = None
    lock_at: Optional[str] = None
    unlock_at: Optional[str] = None
    points_possible: Optional[float] = None
    grading_type: Optional[CanvasGradingType] = None
    submission_types: Optional[List[CanvasSubmissionType]] = None
    allowed_extensions: Optional[List[str]] = None
    assignment_group_id: Optional[int] = None
    position: Optional[int] = None
    peer_reviews: Optional[bool] = None
    automatic_peer_reviews: Optional[bool] = None
    notify_of_update: Optional[bool] = None
    group_category_id: Optional[int] = None
    published: Optional[bool] = None
    omit_from_final_grade: Optional[bool] = None
    hide_in_gradebook: Optional[bool] = None

class UpdateAssignmentArgs(CreateAssignmentArgs):
    assignment_id: int

class SubmitGradeArgs(BaseModel):
    course_id: int
    assignment_id: int
    user_id: int
    grade: float | str
    comment: Optional[str] = None
    rubric_assessment: Optional[Dict[str, Any]] = None

class EnrollUserArgs(BaseModel):
    course_id: int
    user_id: int
    role: Optional[str] = None
    enrollment_state: Optional[str] = None
    notify: Optional[bool] = None
    limit_privileges_to_course_section: Optional[bool] = None

class SubmitAssignmentArgs(BaseModel):
    course_id: int
    assignment_id: int
    submission_type: CanvasSubmissionType
    body: Optional[str] = None
    url: Optional[str] = None
    file_ids: Optional[List[int]] = None
    media_comment_id: Optional[str] = None
    media_comment_type: Optional[str] = None
    user_id: Optional[int] = None

class FileUploadArgs(BaseModel):
    course_id: Optional[int] = None
    folder_id: Optional[int] = None
    name: str
    size: int
    content_type: Optional[str] = None
    on_duplicate: Optional[str] = None

class CanvasClientConfig(BaseModel):
    token: str
    domain: str
    maxRetries: Optional[int] = None
    retryDelay: Optional[int] = None
    timeout: Optional[int] = None

class LLMConfig(BaseModel):
    apiKey: str

class MCPServerConfig(BaseModel):
    name: str
    version: str
    canvas: CanvasClientConfig
    logging: Optional[Dict[str, Any]] = None
    rateLimit: Optional[Dict[str, int]] = None
    llm: LLMConfig

class CanvasErrorResponse(BaseModel):
    message: Optional[str] = None
    errors: Optional[List[Dict[str, Any]]] = None
    error_report_id: Optional[str] = None

class CanvasAccount(BaseModel):
    id: int
    name: str
    uuid: str
    parent_account_id: Optional[int]
    root_account_id: Optional[int]
    default_storage_quota_mb: int
    default_user_storage_quota_mb: int
    default_group_storage_quota_mb: int
    default_time_zone: str
    sis_account_id: Optional[str]
    integration_id: Optional[str]
    sis_import_id: Optional[int]
    lti_guid: str
    workflow_state: str

class CreateUserArgs(BaseModel):
    account_id: int
    user: Dict[str, Any]
    pseudonym: Dict[str, Any]
    communication_channel: Optional[Dict[str, Any]] = None
    force_validations: Optional[bool] = None
    enable_sis_reactivation: Optional[bool] = None

class CanvasAccountReport(BaseModel):
    id: int
    report: str
    file_url: Optional[str] = None
    attachment: Optional["CanvasFile"] = None
    status: str
    created_at: str
    started_at: Optional[str] = None
    ended_at: Optional[str] = None
    parameters: Dict[str, Any]
    progress: int
    current_line: Optional[int] = None

class CreateReportArgs(BaseModel):
    account_id: int
    report: str
    parameters: Optional[Dict[str, Any]] = None

class ListAccountCoursesArgs(BaseModel):
    account_id: int
    with_enrollments: Optional[bool] = None
    enrollment_type: Optional[List[str]] = None
    published: Optional[bool] = None
    completed: Optional[bool] = None
    blueprint: Optional[bool] = None
    blueprint_associated: Optional[bool] = None
    by_teachers: Optional[List[int]] = None
    by_subaccounts: Optional[List[int]] = None
    hide_enrollmentless_courses: Optional[bool] = None
    state: Optional[List[str]] = None
    enrollment_term_id: Optional[int] = None
    search_term: Optional[str] = None
    include: Optional[List[str]] = None
    sort: Optional[str] = None
    order: Optional[str] = None
    search_by: Optional[str] = None

class ListAccountUsersArgs(BaseModel):
    account_id: int
    search_term: Optional[str] = None
    enrollment_type: Optional[str] = None
    sort: Optional[str] = None
    order: Optional[str] = None
    include: Optional[List[str]] = None



from pydantic import BaseModel

CanvasAssignment.model_rebuild()
CanvasFile.model_rebuild()
CanvasConversationMessage.model_rebuild()
CanvasAssignmentSubmission.model_rebuild()
CanvasCourse.model_rebuild()
CanvasCalendarEvent.model_rebuild()
CanvasDashboard.model_rebuild()

