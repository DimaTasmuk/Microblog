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

if __name__ == '__main__':
    app.run()
