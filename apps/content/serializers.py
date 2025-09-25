from rest_framework import serializers
from .models import Service, TeamMember, Vacancy, Contact

class ServiceSerializer(serializers.ModelSerializer):
    # inputs с клиента/клиенту — список
    inputs = serializers.ListField(
        child=serializers.CharField(),
        source='inputs_as_list'
    )

    class Meta:
        model = Service
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['inputs'] = instance.inputs.split(',') if instance.inputs else []
        return ret

    def create(self, validated_data):
            # inputs приходит как список — конвертим в строку
            inputs = self.initial_data.get('inputs', [])
            validated_data['inputs'] = ','.join(inputs)
            return super().create(validated_data)

    def update(self, instance, validated_data):
            inputs = self.initial_data.get('inputs', [])
            validated_data['inputs'] = ','.join(inputs)
            return super().update(instance, validated_data)

    class TeamMemberSerializer(serializers.ModelSerializer):
        class Meta:
            model = TeamMember
            fields = '__all__'

    class VacancySerializer(serializers.ModelSerializer):
        class Meta:
            model = Vacancy
            fields = '__all__'

    class ContactSerializer(serializers.ModelSerializer):
        class Meta:
            model = Contact
            fields = '__all__'