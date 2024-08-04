from django.urls import path
from . import views

urlpatterns = [
   
    path('search-books', views.search_books, name='search-books'),
    path('bookshelves/', views.get_bookshelves, name='search-books'),
    path('bookshelf/add-volume', views.add_volume_in_bookshelf, name='bookshelf/add-volume'),
    path('bookshelf/remove-volume', views.remove_volume_in_bookshelf, name='bookshelf/remove-volume'),
    path('bookshelf/fetch-volumes', views.fetch_volumes_from_bookshelf, name='bookshelf/fetch-volumes'),
    path('authorize/', views.authorize, name='search-books'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
    path('open-homepage/', views.open_home_page, name='openHomePage'),
    path('render_bookshelf', views.render_bookshelf_data, name='render_bookshelf'),
    path('render-search-books', views.render_search_books, name='render-search-books'),
    path('render-book/<str:volumeId>', views.render_book, name='render-book'),
]
