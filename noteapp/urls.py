from django.urls import path
from . views import *

urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name="register"),
    path('login/',UserLoginView.as_view(),name='login'),
    path('addnote/',CreateNoteView.as_view(),name='add-note'),
    path('noteview/<int:pk>/', NoteDetailView.as_view(), name='note-view'),
    path('notesview/', NoteView.as_view(), name='note-view'),
    path('logout/', LogoutView.as_view(), name='logout'),
]