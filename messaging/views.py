from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer, SendMessageSerializer, ChatSerializer, ChatMessagesSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from .models import Chat, UserChats
from .permissions import IsChatParticipant
from rest_framework.decorators import permission_classes

class MessageViewSet(viewsets.GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsChatParticipant, IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(
            models.Q(sender=self.request.user) |
            models.Q(receiver=self.request.user)
        )
        
    @action(detail=False, methods=['post'], url_path='send', serializer_class=SendMessageSerializer)
    def send_message(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='chats', serializer_class=ChatSerializer)
    def get_chats(self, request):
        chats = UserChats.objects.get(user=request.user).chats.all()
        
        page = self.paginate_queryset(chats)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(chats, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='chats/(?P<chat_id>[^/.]+)', serializer_class=ChatMessagesSerializer)
    def get_messages(self, request, chat_id):
        if not UserChats.objects.get(user=request.user).chats.filter(id=chat_id).exists():
            return Response({'detail': 'Chat not found'}, status=404)
        chat = Chat.objects.get(id=chat_id)
    
        serializer = self.get_serializer(chat, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'], url_path='chats/delete/(?P<chat_id>[^/.]+)')
    def delete_chat(self, request, chat_id):
        if not UserChats.objects.get(user=request.user).chats.filter(id=chat_id).exists():
            return Response({'detail': 'Chat not found'}, status=404)
        chat = Chat.objects.get(id=chat_id)
        chat.delete()
        return Response({'detail': 'Chat deleted'})