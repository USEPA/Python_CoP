from django.urls import path

from pfasmsgui.views import simple_test, MessageBoard
urlpatterns = [
    path('simpletest', simple_test),
    path('', MessageBoard.as_view(), name='main_page'),
]

