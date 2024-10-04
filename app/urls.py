from django.urls import path, include

urlpatterns = [
    path('', include('frisbee_simulator_web.urls')),
    path('api/', include('api.urls'))
]
