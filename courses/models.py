from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


# 1. Філія (Базова сутність)
class Branch(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва філії")
    address = models.CharField(max_length=255, verbose_name="Адреса")
    city = models.CharField(max_length=100, verbose_name="Місто")

    def __str__(self):
        return self.name

# 2. Предмет
class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва предмета")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return f"{self.name} ({self.branch.name})"

# 3. План підписки (Абонемент)
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    lessons_quantity = models.PositiveIntegerField(verbose_name="Кількість занять")

    def __str__(self):
        return f"{self.name} ({self.lessons_quantity} занять)"

# 4. Студент
class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# 5. Група студентів
class StudentGroup(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    # Зв'язок з користувачем (вчителем), якого створить Людина 2
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField(Student, related_name='groups')

    def __str__(self):
        return self.name

# 6. Шаблон уроку (Розклад)
class LessonTemplate(models.Model):
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=[(i, i) for i in range(1, 8)])
    start_time = models.TimeField()

# 7. Конкретний Урок
class Lesson(models.Model):
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)
    date = models.DateField()
    is_cancelled = models.BooleanField(default=False)

# 8. Відвідуваність
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=True)

    # 9. Які предмети входять в абонемент
class SubscriptionPlanSubject(models.Model):
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('plan', 'subject') # Щоб не дублювати один і той самий предмет у плані

# 10. Куплений абонемент конкретного студента
class StudentSubscription(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now_add=True)
    lessons_left = models.PositiveIntegerField(verbose_name="Залишок занять")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student} - {self.plan.name} ({self.lessons_left} занять)"