import random

from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Subject, Commendation
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def fix_marks(schoolkid):
    try:
        child = Schoolkid.objects.get(full_name__contains=schoolkid)
    except ObjectDoesNotExist:
        print("Ученик не найден")
        return
    except MultipleObjectsReturned:
        print("Проверьте правильность введенных ФИО ученика")
        return
    points = Mark.objects.filter(schoolkid=child, points__in=[2, 3]).update(points=5)


def remove_chastisements(schoolkid):
    try:
        child = Schoolkid.objects.get(full_name__contains=schoolkid)
    except ObjectDoesNotExist:
        print("Ученик не найден")
        return
    except MultipleObjectsReturned:
        print("Проверьте правильность введенных ФИО ученика")
        return
    all_chastisements = Chastisement.objects.filter(schoolkid=child)
    all_chastisements.delete()


def create_commendation(schoolkid, lesson):
    if not lesson:
        return
    with open("commendations.txt", "r") as file:
        commendations = file.readlines()
        commendation = random.choice(commendations)
    try:
        child = Schoolkid.objects.get(full_name__contains=schoolkid)
    except ObjectDoesNotExist:
        print("Ученик не найден")
        return
    except MultipleObjectsReturned:
        print("Проверьте правильность введенных ФИО ученика")
        return
    try:
        lesson = Lesson.objects.filter(year_of_study=child.year_of_study,
                                       group_letter=child.group_letter,
                                       subject__title=lesson).order_by("date").last()
    except ObjectDoesNotExist:
        print("Предмет не найден")
        return
    Commendation.objects.create(text=commendation,
                                created=lesson.date,
                                schoolkid=child,
                                subject=lesson.subject,
                                teacher=lesson.teacher)


name = "Фролов Иван"
subject = "Математика"
fix_marks(name)
remove_chastisements(name)
create_commendation(name, subject)
