from django.db import models



# class User(models.Model):
#     username = models.CharField(max_length=200)
#     email = models.EmailField(max_length=200)
#     password = models.CharField(max_length=200)

#     def  __str__(self):
#         return self.username
# class User(AbstractUser):
#     email = models.EmailField(unique= True)
#     otp = models.CharField(max_length=100)
#     is_verified = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)


class Student(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    course = models.CharField(max_length=200)

    def __str__(self):
        return self.name
        

