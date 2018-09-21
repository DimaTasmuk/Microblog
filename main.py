from logging.handlers import SMTPHandler

from app import app

# if not app.debug:
#     if app.config['MAIL_SERVER']:
#         auth = None
#         if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
#             auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
#         secure = None
#         if app.config['MAIL_USE_TLS']:
#             secure = ()
#         mail_handler = SMTPHandler(
#             mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT'),
#             fromaddr='no-reply@' + app.config['MAIL_SERVER'],
#             toaddrs=app.config.ADMINS,
#             subject="Microblog Failure",
#             credentials=auth,
#             secure = secure
#         )
#         mail_handler.setLevel(logging.error)
#         app.logger.addHandel(mail_handler)
from app.models import User

if __name__ == '__main__':
    dima = User.objects.get(username="Dima")
    olha = User.objects.get(username="Olha")
    # olha.follow(dima)
    # olha.save()
    petro = User.objects.get(username="Petro")
    petro.follow(dima)
    # petro.save()
    dima.follow(olha)
    print(dima.email, olha.email, petro.email)
    print(olha.following)
    print(User.objects(following__contains=dima))
    print(User.objects(following__contains=olha))
    # app.run()
