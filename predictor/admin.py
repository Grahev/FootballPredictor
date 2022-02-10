from django.contrib import admin
from .models import Team, Player, Match, MatchPrediction, MatchEvents,League

# Register your models here.

class RatingAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)


admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(MatchPrediction)
admin.site.register(MatchEvents)
admin.site.register(League,RatingAdmin)