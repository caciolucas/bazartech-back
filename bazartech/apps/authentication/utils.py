# from django.conf import settings
# from django.core.mail import send_mail

# ! Unused since we're storing profile pictures as base64 strings
# def profile_picture_upload_filepath(instance, uploaded_filename):
#     return f"users/{instance.cpf.replace('-','').replace('.','')}/{uploaded_filename}"

# TODO: Enable the reset password feature with a better template
# def send_forget_password_email(new_password, email):
#     send_mail(
#         "Sua nova senha de login",
#         message=f"Sua nova senha de login é: {new_password}",
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         recipient_list=[email],
#         html_message=f"<p>Sua nova senha de login é: <b>{new_password}</b></p>",
#         fail_silently=False,
#     )
