from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    import os

    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY",
        "development-secret-key",
    )
    
    from .routes import main
    app.register_blueprint(main)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("500.html"), 500

    return app