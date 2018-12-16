from .models import Activity, Student
from admin import ModelView


class ActModelView(ModelView):
    """
    自定义作业帮视图
    """
    column_searchable_list = (
        Activity.name, Activity.phone
    )

    def __init__(self, **kwargs):
        super(ActModelView, self).__init__(Activity, **kwargs)


class StudentModelView(ModelView):
    """
    自定义学生信息视图
    """
    column_searchable_list = (
        Student.name, Student.phone
    )

    def __init__(self, **kwargs):
        super(StudentModelView, self).__init__(Student, **kwargs)
