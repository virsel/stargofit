from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from .views import start_page


urlpatterns = i18n_patterns(
    #path('', views.home, name='home'),
    path('rosetta/', include('rosetta.urls')),
    path('account/', include('account.urls')),
    path('admin/', admin.site.urls),
    path('fitness/', include('training_plans.urls')),
    path('', start_page, name='start_page'),
)


# developmnet server will be in charge if DEBUG setting is set to TRUE

urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
