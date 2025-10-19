from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializer import UserSerializer, NoteSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note

class NoteListCreateView(generics.ListCreateAPIView):
    ## this view will list all notes, and allow creating new notes
    ## Can change to Player model later
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ## Override to return notes only for the logged-in user
        user = self.request.user
        return Note.objects.filter(author=user)
    
    def perform_create(self, serializer):
        ## Override to set the author to the logged-in user
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)

class NoteDelete(generics.DestroyAPIView):
    ## View to delete a note
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ## Override to ensure users can only delete their own notes
        user = self.request.user
        return Note.objects.filter(author=user)

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Allow anyone to create a user
    # TODO: restrict this later to only allow admins to create users
