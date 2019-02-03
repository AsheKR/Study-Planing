from rest_framework import serializers

from repository.models import Repository, ManagedFile


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = '__all__'
        read_only_fields = (
            'owner',
            'root_folder'
        )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if Repository.objects.filter(name=attrs['name'], owner=attrs['owner']).exists():
            raise serializers.ValidationError({'detail': '이미 존재하는 레포지토리가 있습니다.'})

        return attrs

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)
        if not self.context.get('request').user.is_authenticated:
            raise serializers.ValidationError({'detail': '로그인이 필요한 기능입니다.'})

        return {
            'owner': self.context.get('request').user,
            **validated_data
        }


class ManagedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagedFile
        fields = '__all__'
        read_only_fields = (
            'create_author',
            'file_hash',
            'dir',
        )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if ManagedFile.objects.filter(dir=attrs['dir'], name=attrs['name']).exists():
            raise serializers.ValidationError({'detail': '이미 존재하는 파일이나 폴더가 있습니다.'})

        return attrs

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)
        parent_dir = ManagedFile.objects.get(pk=data.get('dir'))

        return {
            'create_author': self.context.get('request').user,
            'file': self.context.get('request').FILES,
            'dir': parent_dir,
            **validated_data,
        }
