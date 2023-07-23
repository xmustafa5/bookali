from django.core.mail import EmailMessage
from ninja import Router
from CAuth.authorization import create_token_for_user
from CAuth.schemas import UserIn, LoginIn, Four0FourOut, VerificationEmailIn, LoginOut, ForgetPasswordIn, \
    ChangePasswordIn, DeleteIn, VerificationEmailOut
from django.contrib.auth import get_user_model
from rest_framework import status
import random

User = get_user_model()

auth_router = Router(tags=['auth'])


def sent_email(email):
    validation_code = random.randint(1000, 9999)
    email_subject = 'verification code'
    email_message = f'your verification code is: {validation_code}'
    email = EmailMessage(email_subject, email_message, to=[email])
    return email, validation_code


@auth_router.post('/sign_up', response={
    400: Four0FourOut,
    406: Four0FourOut,
    201: Four0FourOut,
    401: Four0FourOut
})
def sign_up(request, user_in: UserIn):
    try:
        User.objects.get(email=user_in.email)
        return status.HTTP_400_BAD_REQUEST, {'detail': 'user already exists'}

    except User.DoesNotExist:
        if user_in.password1 != user_in.password2:
            return status.HTTP_406_NOT_ACCEPTABLE, {'detail': 'passwords do not match'}

        user = User.objects.create_user(
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            email=user_in.email,
            phone_number=user_in.phone_number,
            password=user_in.password1
        )
        email, validation_code = sent_email(user_in.email)
        user.code = validation_code
        user.save()
        if not email.send():
            user.delete()
            return status.HTTP_401_UNAUTHORIZED, {'detail': 'email dont send, try signup again'}
        return status.HTTP_201_CREATED, {'detail': 'email send'}


@auth_router.post('/verification_email', response={
    404: Four0FourOut,
    400: Four0FourOut,
    200: VerificationEmailOut
})
def verification_email(request, verification_email_in: VerificationEmailIn):
    try:
        user = User.objects.get(email=verification_email_in.email)
    except User.DoesNotExist:
        return status.HTTP_404_NOT_FOUND, {'detail': 'user does not exist'}

    if user.code != verification_email_in.code:
        return status.HTTP_400_BAD_REQUEST, {'detail': 'the code is incorrect'}
    user.is_active = True
    user.save()
    token = create_token_for_user(user)

    return status.HTTP_200_OK, {'user': user, 'token': token}


@auth_router.post('/login', response={
    404: Four0FourOut,
    400: Four0FourOut,
    200: LoginOut,
    401: Four0FourOut
})
def login(request, login_in: LoginIn):
    try:
        user = User.objects.get(email=login_in.email)
    except User.DoesNotExist:
        return status.HTTP_404_NOT_FOUND, {'detail': 'user does not exist'}

    if not user.check_password(login_in.password):
        return status.HTTP_400_BAD_REQUEST, {'detail': 'password is incorrect'}
    if user.is_active:
        token = create_token_for_user(user)
        return status.HTTP_200_OK, {'email': user.email, 'token': token}
    return status.HTTP_401_UNAUTHORIZED, {'detail': 'user is not active'}

    
@auth_router.post('/forget_password', response={
  404: Four0FourOut,
  200: Four0FourOut,
  400: Four0FourOut
})
def forget_password(request, forget_password_in: ForgetPasswordIn):
    try:
        user = User.objects.get(email=forget_password_in.email)
    except User.DoesNotExist:
        return status.HTTP_404_NOT_FOUND, {'detail': 'user does not exist'}
    email, verification_code = sent_email(forget_password_in.email)
    user.code = verification_code
    user.save()
    if email.send():
        return status.HTTP_200_OK, {'detail': 'email send'}
    return status.HTTP_400_BAD_REQUEST, {'detail': 'email dont send, try again'}


@auth_router.put('/change_password', response={
  404: Four0FourOut,
  400: Four0FourOut,
  200: Four0FourOut
})
def change_password(request, change_password_in: ChangePasswordIn):
    try:
        user = User.objects.get(email=change_password_in.email)
    except User.DoesNotExist:
        return status.HTTP_404_NOT_FOUND, {'detail': 'user does not exist'}

    if user.code != change_password_in.code:
        return status.HTTP_400_BAD_REQUEST, {'detail': 'the code is incorrect'}
    user.set_password(change_password_in.new_password)
    user.save()
    return status.HTTP_200_OK, {'detail': 'password changed'}


@auth_router.delete('/delete_user', response={
    404: Four0FourOut,
    400: Four0FourOut,
    200: Four0FourOut
})
def delete_user(request, delete_in: DeleteIn):
    try:
        user = User.objects.get(email=delete_in.email)
    except User.DoesNotExist:
        return status.HTTP_404_NOT_FOUND, {'detail': 'user does not found'}

    if not user.check_password(delete_in.password):
        return status.HTTP_400_BAD_REQUEST, {'detail': 'password is incorrect'}
    user.delete()
    return status.HTTP_200_OK, {'detail': 'user deleted'}

