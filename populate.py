from barsapp.models import *

respo=User(username='respo', first_name='Respo', last_name='Bar', email='michel.blancard_respo@m4x.org', password='x')
sujet=User(username='sujet', first_name='Sujet', last_name='Docile', email='michel.blancard_sujet@m4x.org', password='x')

respo.set_password('respo')
sujet.set_password('sujet')

respo.save()
sujet.save()

respogu=GlobalUser(auth_user=respo, frankiz_id='respo.bar')
sujetgu=GlobalUser(auth_user=sujet, frankiz_id='sujet.docile')

respogu.save()
sujetgu.save()

barjudo=Bar(hrname='Bar Judo Jone', name='judojone', charges=30, amount=100)
barbad=Bar(hrname='Bar Bad Jone', name='badjone', charges=0, amount=200)

barjudo.save()
barbad.save()

ipjudo=IP(ip='129.104.218.1', sort=1, bar=barjudo)
ipbad=IP(ip='129.104.219.1', sort=1, bar=barbad)
iprespo=IP(ip='129.104.218.31', sort=0, user=respo)
ipsujet=IP(ip='129.104.218.32', sort=0, user=sujet)

ipjudo.save()
ipbad.save()
iprespo.save()
ipsujet.save()

bu1=BarsUser(user=respo, bar=barjudo, pseudo='Respooo', section=True, respo=True, credit=50, total=0)
bu2=BarsUser(user=sujet, bar=barjudo, pseudo='Sujeeet', section=True, respo=False, credit=30, total=0)
bu3=BarsUser(user=sujet, bar=barbad, pseudo='Sujetttt', section=False, respo=False, credit=70, total=0)

bu1.save()
bu2.save()
bu3.save()

