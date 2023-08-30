class EpochGrade:
    def __init__(self, firm, grade_date, fromGrade, toGrade):
        self.firm = firm
        self.grade_date = grade_date
        self.from_grade = fromGrade
        self.to_grade = toGrade

    def __gt__(self, other):
        return self.grade_date > other.grade_date
