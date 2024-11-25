from django.shortcuts import render,redirect
import requests

# Create your views here.
def home(request) :
    return render(request, 'home.html')

def books(request) :
    if request.method == 'GET' and 'book_name' in request.GET :
        book_name = request.GET['book_name']
        results = search_books(book_name)
    else :
        results = []

    context = {
        'results' : results
    }
    return render(request, 'books.html', context)

def search_books(query):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=10"
    response = requests.get(url)

    if response.status_code ==200 :
        data = response.json()
        items = data.get('items', [])

        results = []

        for item in items :
            volume_info = item.get('volumeInfo', {})
            title = volume_info.get('title', 'Unknown Title')
            subtitle = volume_info.get('subtitle', '')
            description = volume_info.get('description', 'No description available')
            thumbnail = volume_info.get('imageLinks',{}).get('thumbnail', '')
            categories = volume_info.get('categories', [])
            pagecount = volume_info.get('pagecount', '')
            averageRating = volume_info.get('averageRating', '')

            book_data = {
                'title' : title,
                'subtitle' : subtitle,
                'description' : description,
                'thumbnail' : thumbnail,
                'categories' : categories,
                'pagecount' : pagecount,
                'averageRating' : averageRating,
                'preview': volume_info.get('previewLink', '')
            }

            results.append(book_data)

        return results
    else :
        return[]