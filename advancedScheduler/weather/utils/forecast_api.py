import os
import requests
from weather.models import Order, Status


# from scheduler.config_stuff import config


def _get_forecast_json():
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    encoded_city_name = 'Los%20Angeles'
    country_code = 'us'
    access_token = os.environ.get('OPENWEATHERMAPS_TOKEN')

    r = requests.get('{0}?q={1},{2}&APPID={3}'.format(
        base_url,
        encoded_city_name,
        country_code,
        access_token))

    try:
        r.raise_for_status()
        return r.json()
    except:
        return None


def update_order(instance):
    qs = Order.objects.filter(id=instance.id, status=Status.ACCEPT)
    if qs.exists():
        try:
            instance.status = Status.NEW
            instance.expiry_pick_up_time = None
            instance.save()
            print("saving...\n", instance)
        except Exception as e:
            print("Error exception...\n", e.args)
    else:
        print("instance.status...\n", instance.status)