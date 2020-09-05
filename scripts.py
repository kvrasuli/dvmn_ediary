from datacenter.models import Mark, Schoolkid, Chastisement, Commendation, Subject, Lesson
import random


def fix_marks(schoolkid):
    marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    marks.update(points=5)


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(schoolkid, subject):
    with open('commendations.txt', 'r') as file:
        commendations = file.readlines()

    lessons = Lesson.objects.filter(
        year_of_study=6,
        group_letter='А',
        subject__title=subject
    )
    last_lesson = lessons.order_by('date').last()
    try:
        lesson_commendation = Commendation.objects.get(
            created=last_lesson.date,
            schoolkid=schoolkid,
            subject=last_lesson.subject,
            teacher=last_lesson.teacher
        )
    except AttributeError:
        print('Ошибка в названии предмета!')
    if not lesson_commendation.text:
        Commendation.objects.create(
            text=random.choice(commendations),
            created=last_lesson.date,
            schoolkid=schoolkid,
            subject=last_lesson.subject,
            teacher=last_lesson.teacher
        )
    else:
        print('На последнем уроке уже есть похвала!')


def get_schoolkid(name):
    try:
        Schoolkid.objects.get(full_name__contains=name)
    except Schoolkid.MultipleObjectsReturned:
        print('Уточни имя!')
    except Schoolkid.DoesNotExist:
        print('Такого имени нет!')


def main():
    schoolkid = get_schoolkid('Фролов Иван')
    fix_marks(schoolkid)
    remove_chastisements(schoolkid)


if __name__ == '__main__':
    main()
