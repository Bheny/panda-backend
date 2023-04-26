from django.urls import path

from .views import *

urlpatterns = [
    path('',RideList.as_view(), name='view_rides'),
    path('create/',CreateRide.as_view(), name="create_ride"),
    # path('detail/<int:id>',UpdateRide.as_view(), name="update_ride"),

    path('search/',RideSearch.as_view(), name="search_ride"),
    path('detail/<int:pk>', RideDetail.as_view(), name="view_ride_detail"),
    path('request/all/', RequestList.as_view(), name="view_requests"),
    path('request/profile/<int:pk>', RequestList.as_view(), name="view_user_requests"),
    path('request/driver/<int:driver_id>', RequestList.as_view(), name="view_my_requests"),
    path('request/create/', CreateRequest.as_view(), name="create_requests"),
    path('request/detail/<int:pk>', RequestDetail.as_view(), name="view_request_detail"),
    path('request/approve/<int:pk>', RequestApproval.as_view(), name="approve_ride"),
    path('request/cancel/<int:pk>', RequestCancel.as_view(), name="cancel_ride"),
    path('request/complete/<int:pk>', RequestCompleted.as_view(), name="complete_ride"),
    path('request/myRides/', RequestDetail.as_view(), name="rides_created"),
    # path('request/detail/<int:id>',UpdateRequest.as_view(), name="update_request"),
]
