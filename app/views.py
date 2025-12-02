"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from app import ec2instance
import os
from django.conf import settings

def home(request):
    """Renders the home page."""
# Get EC2 instance data
    east1_data = ec2instance.GetInstanceState('us-east-1')
    east2_data = ec2instance.GetInstanceState('us-east-2')
    canada_Central1_data = ec2instance.GetInstanceState('ca-central-1')
    
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
            'regions': [
                {
                    'name': east1_data.get('region'),
                    'instances': east1_data.get('instances', [])
                },
                {
                    'name': east2_data.get('region'),
                    'instances': east2_data.get('instances', [])
                },
                {
                    'name': canada_Central1_data.get('region'),
                    'instances': canada_Central1_data.get('instances', [])
                }
            ]
        }
    )


def downloads(request):
    """Renders the downloads page with file listing."""
    assert isinstance(request, HttpRequest)
    downloads_dir = os.path.join(settings.MEDIA_ROOT, 'downloads')
   
    files = []
    if os.path.exists(downloads_dir):
        for filename in os.listdir(downloads_dir):
            if filename == '.gitkeep':  # Skip .gitkeep
                continue
            filepath = os.path.join(downloads_dir, filename)
            if os.path.isfile(filepath):
                files.append({
                    'name': filename,
                    'url': f'{settings.MEDIA_URL}downloads/{filename}',
                    'size': os.path.getsize(filepath)
                })

    return render(
        request,
        'app/downloads.html',
        {
            'title':'Downloads',
            'message':'Lab files download repository',
            'files': files,
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    contacts = [
            {
                'name': 'Roudy Devis - Team Leader',
                'title': 'Security SE - GES East Strategic',
                'email': 'rodevis@cisco.com',
                'phone': '+1 212-714-4378',
                'picture': '/static/app/images/roudy.jpg',
            },
            {
                'name': 'Anders Skjeveland',
                'title': 'Security SE - GES East Strategic',
                'email': 'askjevel@cisco.com',
                'phone': '+1 610-695-5664',
                'picture': '/static/app/images/anders.jpg',
            },
            {
                'name': 'Arpan Lakra',
                'title': 'Security SE - GES East Strategic',
                'email': 'alakra@cisco.com',
                'phone': '+1 703-484-0580',
                'picture': '/static/app/images/arpan.jpg',
            },
            {
                'name': 'Philip Jew',
                'title': 'Security SE - GES East Strategic',
                'email': 'pjew@cisco.com',
                'phone': '+1 732-635-3730',
                'picture': '/static/app/images/Phil.jpg',
            },
            {
                'name': 'Shane Joiner',
                'title': 'Security SE - GES East Strategic',
                'email': 'shjoiner@cisco.com',
                'phone': '+1 904-996-1327',
                'picture': '/static/app/images/shane.jpg',
            },
            {
                'name': 'Steven Chimes',
                'title': 'Security SE - GES East Strategic',
                'email': 'schimes@cisco.com',
                'phone': '+1 610-695-5678',
                'picture': '/static/app/images/Steve.jpg',
            },
            {
                'name': "Chris D'Aguanno",
                'title': 'Security SE - GES East Strategic',
                'email': 'cdaguann@cisco.com',
                'phone': '+1 631-806-1328',
                'picture': '/static/app/images/download.jpg',
            },
        ]
    

    return render(
        request,
        'app/about.html',
        {
            'title':'About Or Team',
            'message':'The 765 Cisco Security SE team.',
            'contacts': contacts,
            'year':datetime.now().year,
        }
    )
