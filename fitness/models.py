from django.db import models


class TopSearch(models.Model):
    name = models.CharField(max_length=500, null=True)
    search_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} - Searches: {self.search_count}'


class FrequentlyAskedQuestion(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    date = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title
