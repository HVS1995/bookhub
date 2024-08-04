import json
from django.http import JsonResponse
from django.shortcuts import render
from googleapiclient.discovery import build # type: ignore
from django.conf import settings
from .serializers import SearchSerializer

import os
from django.shortcuts import redirect, render
from django.conf import settings
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from django.http import HttpResponseRedirect
from django.conf import settings


creds = Credentials(
    token='ya29.a0AcM612wKwisxoTz74akLIrIvo5eyEjuMmOCChydKn3sVsRdP7tf_ThLScoZA19PlB248q9kNOzKJzkzBE8GsEnDPvNqY91ELJYRlVsKoRyizpv4GN1RP_K8S3zB1esnR9x7I7dIgkKQCcAlv_FAronpaTivFUrEpb1gaCgYKAecSARASFQHGX2MiUFyepSVU-G01kHxehTLAOg0170',
    refresh_token=None,
    token_uri='https://oauth2.googleapis.com/token',
    client_id='1076282603408-jrjejuo13hpur1hugec2bo4lh100t3p4.apps.googleusercontent.com',
    client_secret='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',
    scopes=['https://www.googleapis.com/auth/books']
)

def search_books(request):
    keyword = request.GET.get('keyword', '')
    search_type = request.GET.get('searchType', 'title') 
    start_index = int(request.GET.get('startIndex', 0))  
    max_results = int(request.GET.get('maxResults', 10))
    order_by = request.GET.get('orderBy', 'relevance') 
    books = []
    books_data = []

    if keyword:
        if search_type in ['title', 'author', 'publisher', 'subject']:
            search_query = f'{search_type}:{keyword}'
        else:
            search_query = keyword 
            
        service = build('books', 'v1', developerKey=settings.GOOGLE_BOOKS_API_KEY)
        request = service.volumes().list(q=search_query, orderBy=order_by,  startIndex=start_index, maxResults=max_results)
        response = request.execute()

        books = response.get('items', [])
        for item in books:
            volume_info = item.get('volumeInfo', {})
            book_data = {
                    'volumeId': item.get('id', ''),
                    'title': volume_info.get('title', 'No Title'),
                    'subTitle': volume_info.get('subtitle', 'No Sub Title'),
                    'authors': volume_info.get('authors', []),
                    'description': volume_info.get('description', 'No Description Available'),
                    'categories': volume_info.get('categories',[]),
                    'publishedDate': volume_info.get('publishedDate',''),
                    'imageLinks':  volume_info.get('imageLinks', []),
                    'publisher': volume_info.get('publisher', ''),
                    
                }
            books_data.append(book_data)
    return JsonResponse(books_data, safe=False)


def get_bookshelves():
    service = build('books', 'v1', credentials=creds)
    response = service.mylibrary().bookshelves().volumes().list(shelf=8).execute()
    print(response)
    return JsonResponse(response, safe=False)


def add_volume_in_bookshelf(request):

    volume_id = request.GET.get('volumeId', '')
    bookshelf_id = int(request.GET.get('bookshelfId', 600)) 
    
    if volume_id is '' or bookshelf_id is 600:
        return JsonResponse({'message': 'Invalid parameters'}, status=400)
    
    service = build('books', 'v1', credentials=creds)
    response = service.mylibrary().bookshelves().addVolume(
        shelf=bookshelf_id,
        volumeId=volume_id
    ).execute()
    print(response)
    return JsonResponse(response, safe=False)
    
    
def remove_volume_in_bookshelf(request):
    
    volume_id = request.GET.get('volumeId', '')
    bookshelf_id = int(request.GET.get('bookshelfId', 600))
    if volume_id is '' or bookshelf_id is 600:
        return JsonResponse({'message': 'Invalid parameters'}, status=400)
    
    service = build('books', 'v1', credentials=creds)
    try:
        response = service.mylibrary().bookshelves().removeVolume(shelf=bookshelf_id, volumeId=volume_id).execute()
        return JsonResponse({'success': True, 'message': 'Book removed from bookshelf.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


def fetch_volumes_from_bookshelf(request):
    books_data = []
    bookshelf_id = int(request.GET.get('bookshelfId', 0))
    
    service = build('books', 'v1', credentials=creds)
    response = response = service.mylibrary().bookshelves().volumes().list(shelf=bookshelf_id).execute()
    
    books = response.get('items', [])
    for item in books:
        volume_info = item.get('volumeInfo', {})
        book_data = {
                'volumeId': item.get('id', ''),
                'title': volume_info.get('title', 'No Title'),
                'subTitle': volume_info.get('subtitle', 'No Sub Title'),
                'authors': volume_info.get('authors', []),
                'description': volume_info.get('description', 'No Description Available'),
                'categories': volume_info.get('categories',[]),
                'publishedDate': volume_info.get('publishedDate',''),
                'imageLinks':  volume_info.get('imageLinks', []),
                'publisher': volume_info.get('publisher', ''),
                
            }
        books_data.append(book_data)

    return JsonResponse(books_data, safe=False)



def oauth2callback(request):
    client_secrets_path = os.path.join(settings.BASE_DIR, 'client_secret.json')
    print(client_secrets_path, '....')
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            client_secrets_path, 
            scopes=['https://www.googleapis.com/auth/books']
        )
        credentials = flow.run_local_server(port=6570)
        request.session['credentials'] = credentials_to_dict(credentials)
        print(credentials_to_dict(credentials))
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None
    return HttpResponseRedirect('/')

def credentials_to_dict(credentials):
    
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    

def authorize(request):
    books_data = []
    return render(request, 'search_books.html', {'books': books_data})



def open_home_page(request):
    books_data = []
    service = build('books', 'v1', credentials=creds)
    response = response = service.mylibrary().bookshelves().volumes().list(shelf=0).execute()
    
    books = response.get('items', [])
    for item in books:
        volume_info = item.get('volumeInfo', {})
        book_data = {
                'volumeId': item.get('id', ''),
                'title': volume_info.get('title', 'No Title'),
                'subTitle': volume_info.get('subtitle', 'No Sub Title'),
                'authors': volume_info.get('authors', []),
                'description': volume_info.get('description', 'No Description Available'),
                'categories': volume_info.get('categories',[]),
                'publishedDate': volume_info.get('publishedDate',''),
                'imageLinks':  volume_info.get('imageLinks', []),
                'publisher': volume_info.get('publisher', ''),
                
            }
        books_data.append(book_data)
    print(books_data)
    return render(request, 'home.html', {'favorite_books': books_data, 'redirect_tab': 'favorite'})



def render_bookshelf_data(request):
    books_data = []
    tab_id = request.GET.get('tabId', 'favorite')
    
    print('render_bookshelf_data')
    print(tab_id)
    
    
    if tab_id == 'favorite':
        bookshelf_id = 0
    elif tab_id == 'recommended':
        bookshelf_id = 8
    elif tab_id == 'reading-list':
        bookshelf_id = 2
    
    service = build('books', 'v1', credentials=creds)
    response = response = service.mylibrary().bookshelves().volumes().list(shelf=bookshelf_id).execute()
    
    books = response.get('items', [])
    for item in books:
        volume_info = item.get('volumeInfo', {})
        book_data = {
                'volumeId': item.get('id', ''),
                'title': volume_info.get('title', 'No Title'),
                'subTitle': volume_info.get('subtitle', 'No Sub Title'),
                'authors': volume_info.get('authors', []),
                'description': volume_info.get('description', 'No Description Available'),
                'categories': volume_info.get('categories',[]),
                'publishedDate': volume_info.get('publishedDate',''),
                'imageLinks':  volume_info.get('imageLinks', []),
                'publisher': volume_info.get('publisher', ''),
                
            }
        books_data.append(book_data)

    return JsonResponse(books_data, safe=False)


def render_search_books(request):
    keyword = request.GET.get('keyword', '')
    search_type = request.GET.get('searchType', 'title') 
    start_index = int(request.GET.get('startIndex', 0))  
    max_results = int(request.GET.get('maxResults', 10))
    order_by = request.GET.get('orderBy', 'relevance') 
    books = []
    books_data = []

    if keyword:
        if search_type in ['title', 'author', 'publisher', 'subject']:
            search_query = f'{search_type}:{keyword}'
        else:
            search_query = keyword 
            
        service = build('books', 'v1', developerKey=settings.GOOGLE_BOOKS_API_KEY)
        request = service.volumes().list(q=search_query, orderBy=order_by,  startIndex=start_index, maxResults=max_results)
        response = request.execute()

        books = response.get('items', [])
        for item in books:
            volume_info = item.get('volumeInfo', {})
            book_data = {
                    'volumeId': item.get('id', ''),
                    'title': volume_info.get('title', 'No Title'),
                    'subTitle': volume_info.get('subtitle', 'No Sub Title'),
                    'authors': volume_info.get('authors', []),
                    'description': volume_info.get('description', 'No Description Available'),
                    'categories': volume_info.get('categories',[]),
                    'publishedDate': volume_info.get('publishedDate',''),
                    'imageLinks':  volume_info.get('imageLinks', []),
                    'publisher': volume_info.get('publisher', ''),
                    
                }
            books_data.append(book_data)
        print("render search results")
        print(books_data)
    return JsonResponse(books_data, safe=False)


def render_book(request, volumeId):
    books_data = []
    # tab_id = request.GET.get('volumeId', 'favorite')
    # print(tab_id)
    print('here')
    print(volumeId)
    
    
    try:
        # Fetch the volume details by ID
        service = build('books', 'v1', credentials=creds)
        response = service.volumes().get(volumeId=volumeId).execute()
        volume_info = response.get('volumeInfo', {})

        book_data = {
                    'volumeId': response.get('id', ''),
                    'title': volume_info.get('title', 'No Title'),
                    'subTitle': volume_info.get('subtitle', 'No Sub Title'),
                    'authors': volume_info.get('authors', []),
                    'description': volume_info.get('description', 'No Description Available'),
                    'categories': volume_info.get('categories',[]),
                    'publishedDate': volume_info.get('publishedDate',''),
                    'imageLinks':  volume_info.get('imageLinks', []),
                    'publisher': volume_info.get('publisher', ''),
                    
        }
        print(book_data)
        return render(request, 'book-detail.html', {'volumeData': json.dumps(book_data)})

    except Exception as e:
        # Handle exceptions, log error, and provide user feedback
        print(f"Error fetching volume: {e}")
        return redirect('books_view') 
    # service = build('books', 'v1', credentials=creds)
    # response = response = service.mylibrary().bookshelves().volumes().list(shelf=0).execute()
    
    # books = response.get('items', [])
    # for item in books:
    #     volume_info = item.get('volumeInfo', {})
    #     book_data = {
    #             'volumeId': item.get('id', ''),
    #             'title': volume_info.get('title', 'No Title'),
    #             'subTitle': volume_info.get('subtitle', 'No Sub Title'),
    #             'authors': volume_info.get('authors', []),
    #             'description': volume_info.get('description', 'No Description Available'),
    #             'categories': volume_info.get('categories',[]),
    #             'publishedDate': volume_info.get('publishedDate',''),
    #             'imageLinks':  volume_info.get('imageLinks', []),
    #             'publisher': volume_info.get('publisher', ''),
                
    #         }
    #     books_data.append(book_data)
    return render(request, 'book-detail.html', {'favorite_books': books_data, 'redirect_tab': 'favorite'})