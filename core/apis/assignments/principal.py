import sys

from flask import Blueprint
from core import app
from core.apis.responses import APIResponse
from core.apis import decorators
from core.models.assignments import Assignment
from core.models.teachers import Teacher
from .schema import AssignmentSchema, TeacherSchema, AssignmentGradeSchema

principal_assignments_resources = Blueprint("principal_assignments_resources", __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def get_assignments(p):
    student_assignments = Assignment.get_graded_submitted_assignments()
    student_assignments_dump = AssignmentSchema().dump(student_assignments, many=True)
    response = APIResponse.respond(data=student_assignments_dump)
    return response

@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def get_teachers(p):
    teachers = Teacher.get_teachers()
    teachers_dump = TeacherSchema().dump(teachers, many=True)
    response = APIResponse.respond(data=teachers_dump)
    return response

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignments(p, incoming_payload):
    assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    assignment_payload_dump = AssignmentGradeSchema().dump(assignment_payload)

    student_assignment = Assignment.get_by_id(assignment_payload_dump["id"])
    student_assignment_dump = AssignmentSchema().dump(student_assignment, many=False)

    graded_assignments = Assignment.mark_grade(
        _id=assignment_payload.id,
        grade=assignment_payload.grade,
        auth_principal=p
    )

    graded_assignments_dump = AssignmentSchema().dump(graded_assignments, many=False)

    if student_assignment_dump["state"] == "DRAFT":
        response = APIResponse.bad_request(data={})
    else:
        response = APIResponse.respond(data=graded_assignments_dump)

    return response

