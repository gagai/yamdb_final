from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role"
        )


class UserSignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError("Username 'me' is not valid")
        return value

    class Meta:
        fields = ("username", "email")
        model = User


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role"
        )
        model = User
        read_only_fields = ("role",)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = "slug"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = "slug"


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", many=False, queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            "id", "name", "year", "description", "genre", "category"
        )


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True, allow_null=True)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
            "rating",
        )


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        slug_field="username",
        default=serializers.CurrentUserDefault(),
        read_only=True,
    )

    def validate(self, data):
        request = self.context["request"]
        author = request.user
        title_id = self.context["view"].kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if request.method == "POST":
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError(
                    "Разрешено не более одного отзыва на произведение"
                )
        return data

    class Meta:
        fields = "__all__"
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        default=serializers.CurrentUserDefault(),
        read_only=True,
    )
    review = serializers.SlugRelatedField(slug_field="text", read_only=True)

    class Meta:
        fields = "__all__"
        model = Comment
