from django.shortcuts import render


def main_page(requests):
    return render(requests, 'hotel/index.html')
