"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from app import ec2instance

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
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
