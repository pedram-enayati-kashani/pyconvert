from django.urls import path
from Admin_panel.views.Modules import RealEstate

urlpatterns = [
    path('', RealEstate.Index.as_view(), name='real-estate'),

    # sell
    path('sell-buy', RealEstate.SellIndex.as_view(), name='real-estate-sell-buy'),
    path('sell-buy/update/<int:pk>', RealEstate.SellUpdate.as_view(), name='real-estate-sell-buy-update'),
    path('sell-buy/show/<int:pk>/', RealEstate.SellShow.as_view(), name='real-estate-sell-buy-show'),
    path('sell-buy/delete/<int:pk>', RealEstate.SellDelete.as_view(), name='real-estate-sell-buy-delete'),
    path('sell-buy/filter/', RealEstate.SellQuery.as_view(), name='real-estate-sell-buy-query'),
    # Rent
    path('rent', RealEstate.RentIndex.as_view(), name='real-estate-rent'),
    path('rent/update/<int:pk>', RealEstate.RentUpdate.as_view(), name='real-estate-rent-update'),
    path('rent/show/<int:pk>/', RealEstate.RentShow.as_view(), name='real-estate-rent-show'),
    path('rent/delete/<int:pk>', RealEstate.RentDelete.as_view(), name='real-estate-rent-delete'),
    path('rent/filter/', RealEstate.RentQuery.as_view(), name='real-estate-rent-query'),
]