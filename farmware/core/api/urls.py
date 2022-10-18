from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .views import OrganisationsView
from .viewsets.areacode import AreaCodeViewSet
from .viewsets.customer import CustomerViewSet
from .viewsets.order import (
    OrderViewSet, 
    OrderItemViewSet, 
    OrderItemStockLinkViewSet
    )
from .viewsets.produce import (
    ProduceViewSet, 
    ProduceVarietyViewSet, 
    ProduceQuantitySuffixViewSet
    )
from .viewsets.stock import (
    StockViewSet,
    StockPickersViewSet
)
from .viewsets.supplier import SupplierViewSet
from .viewsets.team import TeamViewSet

router = DefaultRouter()

router.register('area_code', AreaCodeViewSet, 'area_code')
router.register('customer', CustomerViewSet, 'customer')
router.register('order', OrderViewSet, 'order')
router.register('order_item', OrderItemViewSet, 'order_item')
router.register('order_item_stock_link', OrderItemStockLinkViewSet, 'order_item_stock_link')
router.register('produce', ProduceViewSet, 'produce')
router.register('produce_variety', ProduceVarietyViewSet, 'produce_variety')
router.register('produce_quantity_suffix', ProduceQuantitySuffixViewSet, 'produce_quantity_suffix')
router.register('stock', StockViewSet, 'stock')
# router.register('stock_pickers', StockPickersViewSet, 'stock_pickers')
router.register('supplier', SupplierViewSet, 'supplier')
router.register('team', TeamViewSet, 'team')

urlpatterns = [
    # Organisation
    path('organisation/', OrganisationsView.as_view(), name='api-organisation'),

    # User
    ## User
    path('user/', include('core.user.urls', namespace='user')),
    ## Tokens
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]

urlpatterns += router.urls