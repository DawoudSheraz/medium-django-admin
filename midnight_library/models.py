from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Author(models.Model):
    """
    Author who will be linked with a single library.
    """
    user = models.OneToOneField(User, related_name='author', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=64)
    date_of_birth = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    date_of_death = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    job = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.user.username} - {self.date_of_birth}"


class MidnightLibrary(models.Model):
    """
    The exclusive library of a user.
    """
    author = models.OneToOneField(Author, related_name='library', on_delete=models.CASCADE)
    manager = models.OneToOneField(
        User, help_text="The librarian/manager guiding the author through the library",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.author.user.username} - {self.manager.username}"


class Book(models.Model):
    """
    The alternate life of the author represented in the form of a book in midnight library.
    """
    library = models.ForeignKey(MidnightLibrary, related_name='collection', on_delete=models.CASCADE)
    has_visited = models.BooleanField(
        default=False, help_text="Identify if the author has visited the alternate life"
    )
    visit_date = models.DateTimeField(null=True, blank=True, auto_now_add=False)
    days_stayed = models.PositiveIntegerField(default=0, help_text="The time spent in the life")
    title = models.CharField(max_length=64)
    description = models.TextField(help_text="Brief outlook into the expectations of the alternate life")

    def __str__(self):
        return f"{self.title} - {self.library.author}"


class Review(models.Model):
    """
    Review if the alternate life was worth it.
    """
    life = models.OneToOneField(Book, related_name='review', on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)
    comment = models.TextField(help_text="Experience of the alternative life")

    def __str__(self):
        return f"{self.life} - {self.is_liked}"
