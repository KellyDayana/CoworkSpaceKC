from django.contrib import admin
from .models import EmpresaCliente, Miembro, SalaReunion, EscritorioDedicado, ReservaSala, Evento, Factura

# Register your models here.
admin.site.register(EmpresaCliente)
admin.site.register(Miembro)
admin.site.register(SalaReunion)
admin.site.register(EscritorioDedicado)
admin.site.register(ReservaSala)
admin.site.register(Evento)
admin.site.register(Factura)
