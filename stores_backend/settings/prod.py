from .base import *

DEBUG = False
USE_TZ = True

DEFAULT_RENDERER_CLASSES = (
    "rest_framework.renderers.JSONRenderer",
)

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES,
}