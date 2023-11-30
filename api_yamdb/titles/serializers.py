from datetime import datetime
from rest_framework import serializers
from .models import Title, Category, Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            # "id",
            "name",
            "slug",
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            # "id",
            "name",
            "slug",
        )


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "descriptions",
            "category",
            "genre",
        )

    def validate_year(self, value):
        year = int(datetime.now().year)
        if 0 < value > year:
            raise serializers.ValidationError(
                "Год не должен быть меньше нуля и больше текущего года"
            )
        return value
