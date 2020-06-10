from django.contrib import admin
from .models import healthCheck
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter


class healthcheckAdmin(admin.ModelAdmin):
    list_display =  ('id', 'date','test_id', 'desc', 'severity', 'ipaddr', 'hostname', 'command', 'verdict','remarks')
    #list_display_links = ('id', 'test_id')
    list_filter = ('date',('date', DateRangeFilter) ,'verdict', 'severity', 'command', 'hostname')
    search_fields = ('date','test_id', 'hostname' , 'ipaddr', 'command', 'verdict' , 'severity' ,'command', 'hostname')

#admin.site.register(healthCheck,healthcheckAdmin)
admin.site.register(healthCheck, healthcheckAdmin)


from .models import Execute1

admin.site.register(Execute1)



from .models import failedPositive
class listfailedpositive(admin.ModelAdmin):
    list_display =  ('id' ,'site','test_id', 'desc', 'severity', 'ipaddr', 'hostname', 'command', 'verdict','remarks')
    #list_display_links = ('id', 'test_id')
    list_filter = ('site','verdict', 'severity', 'command', 'hostname')
    search_fields = ('site','test_id', 'hostname' , 'ipaddr', 'command', 'verdict' , 'severity' ,'command', 'hostname')

admin.site.register(failedPositive, listfailedpositive)


from .models import ignoreTest
class listignoretest(admin.ModelAdmin):
    list_display =  ('id' ,'site','test_id', 'desc', 'severity', 'ipaddr', 'hostname', 'command', 'verdict','remarks')
    #list_display_links = ('id', 'test_id')
    list_filter = ('site','verdict', 'severity', 'command', 'hostname')
    search_fields = ('site','test_id', 'hostname' , 'ipaddr', 'command', 'verdict' , 'severity' ,'command', 'hostname')

admin.site.register(ignoreTest, listignoretest)
