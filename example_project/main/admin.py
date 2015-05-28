from django.contrib import admin
from main.models import UserData,Comment,Project,TotalG
# Register your models here.
from simple_history.admin import SimpleHistoryAdmin

'''
class UserDataAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass
'''
admin.site.register(UserData, SimpleHistoryAdmin)
admin.site.register(Project, SimpleHistoryAdmin)
admin.site.register(TotalG, SimpleHistoryAdmin)
admin.site.register(Comment, SimpleHistoryAdmin)
