from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
from django.urls import reverse


tanks = "TN"
heals = "HE"
dd = "DD"
vendors = "VE"
guild_masters = "GM"
quest_givers = "QG"
blacksmiths = "BS"
tanners = "TA"
potion_makers = "PM"
spell_masters = "SM"

post_types = [
    (tanks, "Танки"),
    (heals, "Хилы"),
    (dd, "ДД"),
    (vendors, "Торговцы"),
    (guild_masters, "Гильдмастеры"),
    (quest_givers, "Квестгиверы"),
    (blacksmiths, "Кузнецы"),
    (tanners, "Кожевники"),
    (potion_makers, "Зельевары"),
    (spell_masters, "Мастера заклинаний")
]


class Post (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    types = models.CharField(max_length=2, choices=post_types)
    heading = models.CharField(max_length=255)
    text = FroalaField()

    def preview(self) -> str:
        return self.text[:124]+"..."

    def get_types() -> dict[(str, str)]:
        return post_types
    
    def __str__(self) -> str:
        return self.heading


class Response (models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creation_datetime = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def accept(self):
        self.is_accepted = True

    def do_not_accept(self):
        self.is_accepted = False
