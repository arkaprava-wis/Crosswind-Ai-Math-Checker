from rest_framework import serializers

from .models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    original_filename = serializers.CharField(read_only=True)

    class Meta:
        model = Submission
        fields = [
            "id", 
            "file", 
            "original_filename", 
            "created_at", 
            "updated_at",
        ]
        read_only_fields = [
            "id", 
            "original_filename", 
            "created_at", 
            "updated_at"
        ]
    def validate_file(self, uploaded_file):
        max_size = 10 * 1024 * 1024  # 10MB

        # Validate file size (e.g., max 10MB)
        if uploaded_file.size > max_size:
            raise serializers.ValidationError("File size must not exceed the limit of 10MB.")

        # Validate file type (e.g., only ".jpg", ".jpeg", ".png")
        allowed_extensions = {".jpg", ".jpeg", ".png"}
        filename = uploaded_file.name.lower()

        if not any(filename.endswith(extension) for extension in allowed_extensions):
            raise serializers.ValidationError("Only JPG, JPEG, and PNG files are supported.")

        return uploaded_file

    def create(self, validated_data):
        uploaded_file = validated_data["file"]

        submission = Submission.objects.create(
            file=uploaded_file,
            original_filename=uploaded_file.name
        )

        return submission
