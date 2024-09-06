#!/usr/bin/env python3
"""
Initialization of views for the API
"""
from flask import Blueprint

# Create the blueprint that will register the views
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import views (including the new session auth view)
# Import the session authentication view at the
# end of the file to avoid circular imports
from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import *

User.load_from_file()
