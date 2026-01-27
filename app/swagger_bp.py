# Create Swagger Blueprint
from flask_swagger_ui import get_swaggerui_blueprint

from app.config import SWAGGER_UI_URL, SWAGGER_API_URL

swagger_ui_blueprint = get_swaggerui_blueprint(
    base_url=SWAGGER_UI_URL, api_url=SWAGGER_API_URL
)
