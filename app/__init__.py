from flask import Flask, jsonify

from app.config import JWT_SECRET_KEY


def create_app():
    from app.swagger_utils import build_swagger
    from app.swagger_bp import swagger_ui_blueprint
    from app.db import db
    from app.config import SQLALCHEMY_DATABASE_URI, SWAGGER_API_URL
    from app.expense.routes import bp as expense_bp
    from app.user.routes import bp as user_bp
    from app.migrate import migrate
    from app.jwt import jwt

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI, JWT_SECRET_KEY=JWT_SECRET_KEY
    )

    @app.route("/")
    def home():
        """
        User greeting on the Home page
        ---
        tags:
            - Home page
        produces:
            - application/json
        responses:
            200:
               description: Greeting
               schema:
                     $ref: '#/definitions/Hello'
        """
        return jsonify(message="Hello, I'm your Expense tracking App!")

    @app.errorhandler(404)
    def handle_404(error):
        return jsonify(error="We couldn't find that"), 404

    @app.route(SWAGGER_API_URL)
    def spec():
        return jsonify(build_swagger(app))

    # Init DB
    db.init_app(app)

    # render_as_batch for SQLite only
    migrate.init_app(app, db, render_as_batch=True)

    jwt.init_app(app)

    # Register Blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(swagger_ui_blueprint)

    return app
