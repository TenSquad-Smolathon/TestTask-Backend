from rest_framework import serializers
from .models import Service, TeamMember, Vacancy, Contact, New, Article, Document, ServiceRequest

class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = 'all'
        read_only_fields = ('user', 'created_at')

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'short_desc', 'desc', 'text', 'inputs', 'action_text']

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
            
class NewSerializer(serializers.ModelSerializer):
        class Meta:
            model = New
            fields = '__all__'
            
class ArticleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = '__all__'
            
class DocumentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Document
            fields = '__all__'