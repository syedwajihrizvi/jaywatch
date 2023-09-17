GRADE_RATINGS = {
    "buy": 5,
    "outperform": 6,
    "strong buy": 7,
    "strong sell": -7,
    "neutral": 2,
    "hold": 2,
    "underperform": -6,
    "equal-weight": 2,
    "overweight": 5,
    "underweight": -5,
    "sell": -6,
    "market perform": 2,
    "peer perform": 2,
    "sector perform": 2,
    "positive": 2,
    "market outperform": 5
}


class EpochGrade:
    def __init__(self, firm, grade_date, fromGrade, toGrade):
        self.firm = firm
        self.grade_date = grade_date
        self.from_grade = fromGrade
        self.to_grade = toGrade

        self.score = "N/A"
        if self.from_grade and self.to_grade:
            print(self.from_grade, self.to_grade)
            self.score = GRADE_RATINGS.get(
                self.to_grade.lower()) - GRADE_RATINGS.get(self.from_grade.lower())

    def __gt__(self, other):
        return self.grade_date > other.grade_date

    def __str__(self):
        return f"{self.firm} did {self.from_grade} to {self.to_grade} on {self.grade_date}: {self.score}"
