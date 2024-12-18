from django.db import models
from django.core.validators import MaxLengthValidator
from authentication.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField(blank=True, validators=[MaxLengthValidator(1000)])
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.first_name} to {self.receiver.first_name}"


class Chat(models.Model):
    sender = models.ForeignKey(User, related_name='sender_chats', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver_chats', on_delete=models.CASCADE)
    last_message = models.TextField(blank=True, validators=[MaxLengthValidator(1000)])
    last_update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Chat between {self.sender.first_name} and {self.receiver.first_name}"


class UserChats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    chats = models.ManyToManyField(Chat)
    
    def __str__(self):
        return f"Chats of {self.user.first_name}"