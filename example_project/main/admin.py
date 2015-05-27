from django.contrib import admin
from main.models import UserData,Comment
# Register your models here.
class UserDataAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserData, UserDataAdmin)
admin.site.register(Comment, CommentAdmin)

