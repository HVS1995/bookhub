# from django.db import models
# from django.contrib.auth.models import User

# # Create your models here.

# class Book(models.Model):
#     title = models.CharField(max_length=200)
#     author = models.CharField(max_length=100)
#     description = models.TextField(null=True, blank=True)
#     cover_image = models.URLField(null=True, blank=True)
#     total_ratings = models.PositiveIntegerField(default=0)
#     sum_of_ratings = models.PositiveIntegerField(default=0)
#     publication_date = models.DateField(null=True, blank=True)

#     @property
#     def average_rating(self):
#         if self.total_ratings > 50:
#             return self.sum_of_ratings / self.total_ratings
#         return None

#     def __str__(self):
#         return self.title
    
    
    
    
# class Recommendation(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='recommendations')
#     user = models.CharField(max_length=100)
#     review = models.TextField(null=True, blank=True)
#     rating = models.IntegerField(default=0)
    
#     def __str__(self):
#         return f"{self.user} recommends {self.book.title}"
    
    
    
# class Rating(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     rating = models.PositiveIntegerField()
    
    
#     def save(self, pk):
#         if self.pk is None:  
#             self.book.total_ratings += 1
#             self.book.sum_of_ratings += self.rating
#         else:  
#             original = Rating.objects.get(pk=self.pk)
#             self.book.sum_of_ratings += self.rating - original.rating
#         self.book.save()
        
        
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     books_rated = models.ManyToManyField(Book, through=Rating)

#     def count_books_rated(self):   # this will count that the user given how many  review im using atleast 50 review.
#         return self.books_rated.count()