SELECT teacher_id, COUNT(teacher_id) FROM assignments WHERE assignments.state == "GRADED";