from rest_framework import permissions
from .models import Chat, Message

class IsChatParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Chat):
            return request.user == obj.sender or request.user == obj.receiver
        
        if isinstance(obj, Message):
            return request.user == obj.sender or request.user == obj.receiver
        
        return False