from dotenv import load_dotenv
from nft_gen import create_app

load_dotenv()

flask_app = create_app()
celery_app = flask_app.extensions["celery"]
