from celery.decorators import task
from .models import TempData


@task
def delete_temp(obj_id):
    try:
        obj = TempData.objects.get(id=obj_id)
        obj.delete()
    except:
        print('item already deleted')