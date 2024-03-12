from models import ApiHostModel
import config


DEBUG = False
API_HOST_URL = ApiHostModel(config.ENV('API_HOST_URL')) / 'sync'

