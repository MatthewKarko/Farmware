from django.contrib import admin
from .models.areacode import AreaCode
from .models.customer import Customer
from .models.order import Order
from .models.order import OrderStock
from .models.organisation import  Organisation
from .models.produce import Produce
from .models.produce import ProduceVariety
from .models.produce import ProduceQuantitySuffix
from .models.stock import Stock
from .models.supplier import Supplier
from .models.team import Team

# Register your models here.
admin.site.register(AreaCode)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderStock)
admin.site.register(Organisation)
admin.site.register(Produce)
admin.site.register(ProduceVariety)
admin.site.register(ProduceQuantitySuffix)
admin.site.register(Stock)
admin.site.register(Supplier)
admin.site.register(Team)