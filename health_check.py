"""
Health check endpoint for Tesouraria application.
This file can be imported by your main application to add a health check endpoint.

For Flask applications:
    from health_check import add_health_check
    app = Flask(__name__)
    add_health_check(app)

For FastAPI applications:
    from health_check import health_check
    app.get("/health")(health_check)

For Django applications:
    Add this to your urls.py:
    from health_check import health_check_view
    urlpatterns = [
        path('health/', health_check_view),
        ...
    ]
"""

import json
from datetime import datetime


def health_check():
    """Basic health check function that returns application status."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "tesouraria"
    }


# Flask integration
def add_health_check(app):
    """Add health check endpoint to Flask application."""
    @app.route('/health')
    def health():
        return json.dumps(health_check()), 200, {'Content-Type': 'application/json'}


# Django integration
def health_check_view(request):
    """Health check view for Django applications."""
    from django.http import JsonResponse
    return JsonResponse(health_check())


# FastAPI is handled by importing health_check directly


if __name__ == "__main__":
    # Test the health check
    print(json.dumps(health_check(), indent=2))
