from rest_framework import serializers

class ParticipanteSerializer(serializers.Serializer):
    instagram_username = serializers.CharField(required=True, max_length=255)
    requirements = serializers.BooleanField(required=True)

    def validate(self, data):
        if not data.get('requirements'):
            raise serializers.ValidationError("El participante no cumple los requisitos.")
        return data
