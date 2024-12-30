import requests

from django.conf import settings


class GhnApiService:
    def __init__(self):
        self.ghn_base_url = settings.GHN_BASE_URL
        self.ghn_shop_id = settings.GHN_SHOP_ID
        self.ghn_token_api = settings.GHN_TOKEN_API

    def requests(self, method, endpoint, **kwargs):
        url = f"{self.ghn_base_url}{endpoint}"
        headers = {
            "Token": self.ghn_token_api,
            **kwargs.pop("headers", {}),
        }
        if method.upper() in ["POST", "PUT", "PATCH"]:
            headers["Content-Type"] = "application/json"
        response = requests.request(method, url, headers=headers, **kwargs)
        return response

    def get_province_list(self):
        resource = "master-data/province"
        response = self.requests("GET", resource)
        return response

    def get_district_list(self, province_id):
        resource = "master-data/district"
        payload = {"province_id": int(province_id)}
        response = self.requests("GET", resource, json=payload)
        return response

    def get_ward_list(self, district_id):
        resource = "master-data/ward?district_id"
        payload = {"district_id": int(district_id)}
        response = self.requests("POST", resource, json=payload)
        return response

    def calculate_delivery_fee(self, district_id, ward_id):
        resource = "v2/shipping-order/fee"
        headers = {"shop_id": self.ghn_shop_id}
        payload = {
            "service_id": 53320,
            "service_type_id": 2,
            "to_district_id": int(district_id),
            "to_ward_code": str(ward_id),
            "weight": 1000,
        }
        response = self.requests("POST", resource, json=payload, headers=headers)
        return response
