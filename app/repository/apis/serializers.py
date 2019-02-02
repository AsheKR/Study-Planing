from rest_framework import serializers

from repository.models import Repository


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = '__all__'
        read_only_fields = (
            'owner',
            'root_folder'
        )

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)
        if not self.context.get('request').user.is_authenticated:
            raise serializers.ValidationError({'detail': '로그인이 필요한 기능입니다.'})

        return {
            'owner': self.context.get('request').user,
            **validated_data
        }
