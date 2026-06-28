import sys
import logging
logging.basicConfig(level=logging.DEBUG)

try:
    from hiddifypanel.apps.asgi_app import app
    print("Import successful!")
    
    with app.app_context():
        # try to match a route
        adapter = app.url_map.bind("localhost")
        print("URL Map OK")
except Exception as e:
    import traceback
    traceback.print_exc()
