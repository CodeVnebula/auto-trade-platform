from rest_framework import serializers
from .models import Message, Chat, UserChats
from authentication.models import User, Profile
from django.db import models
    
    
class UserChatInfoSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    
    def get_profile_picture(self, obj):
        profile = Profile.objects.get(user=obj)
        if profile.profile_picture:
            return profile.profile_picture.url
        return None
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'profile_picture']
        

class ChatSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()
    
    def get_other_user(self, obj):
        request_user = self.context['request'].user
        if obj.sender == request_user:
            return UserChatInfoSerializer(obj.receiver, context=self.context).data
        else:
            return UserChatInfoSerializer(obj.sender, context=self.context).data
    
    class Meta:
        model = Chat
        fields = ['id', 'other_user', 'last_message', 'last_update']
        

class UserChatMessageInfoSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    full_name = serializers.CharField(source='get_full_name')
    
    def get_full_name(self, obj):
        return obj.first_name + ' ' + obj.last_name
    class Meta:
        model = User
        fields = ['id', 'full_name']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()
    
    def get_sender(self, obj):
        return UserChatMessageInfoSerializer(obj.sender, context=self.context).data
    
    def get_receiver(self, obj):
        return UserChatMessageInfoSerializer(obj.receiver, context=self.context).data
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'sent_at']
        read_only_fields = ['sender']
    
from rest_framework.pagination import LimitOffsetPagination

class ChatMessagesSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()

    def get_other_user(self, obj):
        request_user = self.context['request'].user
        if obj.sender == request_user:
            return UserChatInfoSerializer(obj.receiver, context=self.context).data
        else:
            return UserChatInfoSerializer(obj.sender, context=self.context).data

    def get_user(self, obj):
        request_user = self.context['request'].user
        return UserChatInfoSerializer(request_user, context=self.context).data

    def get_messages(self, obj):
        request = self.context['request']
        paginator = LimitOffsetPagination()
        paginator.default_limit = 15  
        paginator.max_limit = 50  
        messages = Message.objects.filter(
            models.Q(sender=obj.sender, receiver=obj.receiver) |
            models.Q(sender=obj.receiver, receiver=obj.sender)
        ).order_by('sent_at')

        paginated_messages = paginator.paginate_queryset(messages, request)

        serialized_messages = MessageSerializer(paginated_messages, many=True, context=self.context).data

        return serialized_messages
    class Meta:
        model = Chat
        fields = ['other_user', 'user', 'messages']


class SendMessageSerializer(serializers.ModelSerializer):
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = Message
        fields = ['receiver', 'content']
    
    def validate(self, data):
        sender = self.context['request'].user
        receiver = data['receiver']
        if sender.profile.enable_messages == False:
            raise serializers.ValidationError('You cannot send a message, enable messages in your profile settings')
        if receiver.profile.receive_messages == False or not receiver.is_active:
            raise serializers.ValidationError('You cannot send a message to this user')
        if sender == receiver:
            raise serializers.ValidationError('You cannot send a message to yourself')
        return data
    
    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        
        chat, _ = Chat.objects.get_or_create(
            sender=validated_data['sender'], 
            receiver=validated_data['receiver'],
        )
      
        chat2, _ = Chat.objects.get_or_create(
            sender=validated_data['receiver'], 
            receiver=validated_data['sender']
        )
        
        chat2.last_message = validated_data['content']
        chat2.save()
        
        chat.last_message = validated_data['content']
        chat.save()
        
        sender_chats = UserChats.objects.get(user=validated_data['sender'])
        sender_chats.chats.add(chat)
        sender_chats.save()
        
        receiver_chats = UserChats.objects.get(user=validated_data['receiver'])
        receiver_chats.chats.add(chat2)
        receiver_chats.save()
        
        return super().create(validated_data)
