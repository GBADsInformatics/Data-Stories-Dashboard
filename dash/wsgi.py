from flask_app import init_app
import os

app = init_app()

# Used for containerizing dashboards
# return app
# Return's the WSGI app used for Docker
def returnApp():
    """
    This function is used to create the app and return it to waitress in the docker container
    """
    # If DASH_BASE_URL is set, use DispatcherMiddleware to serve the app from that path
    if 'DASH_BASE_URL' in os.environ:
        from flask import Flask
        from werkzeug.middleware.dispatcher import DispatcherMiddleware
        app.wsgi_app = DispatcherMiddleware(Flask('dummy_app'), {
            os.environ['DASH_BASE_URL']: app.server
        })
        # Added redirect to new path
        @app.wsgi_app.app.route('/')
        def redirect_to_dashboard():
            from flask import redirect
            return redirect(os.environ['DASH_BASE_URL'])
        return app.wsgi_app

    # If no DASH_BASE_URL is set, just return the app server
    return app.server

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=os.environ.get('PORT', 8055), use_reloader=True)