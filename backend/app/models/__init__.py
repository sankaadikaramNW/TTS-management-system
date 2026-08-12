# Import all models here to ensure SQLAlchemy can resolve all relationships
# Order matters: base/referenced models must come before models that reference them

from app.models.user import Role, Permission, User
from app.models.student import Student, ParadeState, ParadeStatusType, StudentStatusType, Rank, Trade, ParadeSubmission, OfficerInCharge
from app.models.academic import Classroom, Course, Batch, Subject, Lesson, LessonPlan, Timetable, AcademicAttendance, Exam, ExamMark, LessonPlanDocument
from app.models.accommodation import AccommodationBuilding, AccommodationBillet, AccommodationBed, AccommodationAllocation
from app.models.notification import Notification

__all__ = [
    "Role", "Permission", "User",
    "Student", "ParadeState", "ParadeStatusType", "StudentStatusType", "Rank", "Trade",
    "ParadeSubmission", "OfficerInCharge",
    "Classroom", "Course", "Batch", "Subject", "Lesson", "LessonPlan", "Timetable", "AcademicAttendance", "Exam", "ExamMark", "LessonPlanDocument",
    "AccommodationBuilding", "AccommodationBillet", "AccommodationBed", "AccommodationAllocation",
    "Notification",
]

