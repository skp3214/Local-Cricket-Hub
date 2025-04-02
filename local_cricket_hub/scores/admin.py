from django.contrib import admin

# Register your models here.

from scores.models import Inning, BattingScore, BowlingScore

admin.site.register(Inning)
admin.site.register(BattingScore)
admin.site.register(BowlingScore)
