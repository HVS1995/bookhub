from rest_framework import serializers


# class BookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields = ['id', 'title', 'author', 'publication_date']

# class RecommendationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Recommendation
#         fields = '__all__'

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['title', 'subtitle', 'author', 'publication_date','description', 'category']