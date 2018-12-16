from .models import OauthActivity
from admin import ModelView


class OauthModelView(ModelView):
    """
    自定义微信多平台视图
    """
    column_searchable_list = (
        OauthActivity.name, OauthActivity.phone
    )

    def __init__(self, **kwargs):
        super(OauthModelView, self).__init__(OauthActivity, **kwargs)