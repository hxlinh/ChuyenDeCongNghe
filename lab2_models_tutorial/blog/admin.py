from django.contrib import admin
from .models import (
    Person, PersonExtended, Musician, Album, Topping, Pizza,
    Group, Membership, Place, Restaurant, Student, Runner, Ox,
    StudentChild, Blog
)

# Register your models here.
admin.site.register(Person)
admin.site.register(PersonExtended)
admin.site.register(Musician)
admin.site.register(Album)
admin.site.register(Topping)
admin.site.register(Pizza)
admin.site.register(Group)
admin.site.register(Membership)
admin.site.register(Place)
admin.site.register(Restaurant)
admin.site.register(Student)
admin.site.register(Runner)
admin.site.register(Ox)
admin.site.register(StudentChild)
admin.site.register(Blog)
