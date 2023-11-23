# Prepelius

In this project two models are created 

# model.py of Basic Details

1. User Model :-this model is custome model which is use for Register New User.
    -User Model Fields
        - Email
        - First Name
        - Last Name
        - Password
        - Password 2 This is extra for password verification

2. Note Model :- This Model is use for add new Note Records With User Reference 
    - Note Model Fields
        - Title
        - Content
        - User .this field is use foreign key
        
# serializers.py of Basic Details

1. UserRegistrationSerializer:- this serializer class are use for user register parts handeling

2. NoteSerializer:- this serializer class are use for Note Operations parts handeling

# views.py of Basic Details
1. UserRegistrationView :- This view class use for user view handeling

2. UserLoginView :- This view class use for user login view handeling

3. CreateNoteView :- This view class use for Note Create and display new record

4. NoteDetailView :- This view class use for Note Delete Update & View with single id for this view handeling

5. NoteView :- This view class use for Note Pagination and search view handeling

6. LogoutView :- This view class use for user logout view handeling