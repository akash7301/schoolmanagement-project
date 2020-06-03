def score_grade(score):
    if score>=90 and sccore<=100:
        return 'A'
    elif score>=80 and socre<90:
        return 'B'
    elif score>=70 and score<80:
        return 'C'
    elif score>=60 and score<70:
        return 'D'
    elif score<60 and score>=35:
        return 'E'
    else:
        return 'FAIL'
