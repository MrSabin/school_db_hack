import random

from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Subject, Commendation


def fix_marks(schoolkid):
    child = Schoolkid.objects.get(full_name__contains=schoolkid)
    points = Mark.objects.filter(schoolkid=child, points__in=[2, 3])
    for record in points:
        record.points = 5
        record.save()


def remove_chastisements(schoolkid):
    child = Schoolkid.objects.get(full_name__contains=schoolkid)
    all_chastisements = Chastisement.objects.filter(schoolkid=child)
    all_chastisements.delete()


def create_commendation(schoolkid, lesson):
    if not lesson:
        return
    with open("commendations.txt", "r") as file:
        commendations = file.readlines()
        commendation = random.choice(commendations)
    child = Schoolkid.objects.get(full_name__contains=schoolkid)
    lesson = Lesson.objects.filter(year_of_study=child.year_of_study,
                                   group_letter=child.group_letter,
                                   subject__title=lesson).order_by("date").last()
    Commendation.objects.create(text=commendation,
                                created=lesson.date,
                                schoolkid=child,
                                subject=lesson.subject,
                                teacher=lesson.teacher)


name = "Пахомов Викентий"
subject = "Математика"
fix_marks(name)
remove_chastisements(name)
create_commendation(name, subject)