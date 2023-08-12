from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="ShopHome"),
    path("about/",views.about,name="AboutUs"),
    path("contact",views.contact,name="ContactUs"),
    path("tracker/",views.tracker,name="TrackingStatus"),
    path("search/",views.search,name="Search"),
    path("products/<int:myid>",views.productView,name="Productview"),
    path("checkout/",views.checkout,name="CheckOut"),
    path("login/",views.loginUser,name="loginUser"),
    path("logout/",views.logoutUser,name="logoutUser"),
    path("signUp/",views.signUp,name="SignUp"),
    path("handlerequest/",views.handlerequest,name="handlerequest"),
    path("handlesignup/",views.handlesignup,name="handlesignup")
]
