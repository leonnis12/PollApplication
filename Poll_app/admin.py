from django.contrib import admin
from .models import Poll,Quiz

# Register your models here.

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ("question", "author", "quiz")
    empty_value_display = "None"

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("name", "author")
    empty_value_display = "None"