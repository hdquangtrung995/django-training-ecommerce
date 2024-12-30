import urllib.parse
import json
from django.http import JsonResponse, QueryDict
from django.views import View

from services.giao_hang_nhanh import GhnApiService


class JSONResponseMixin:
    """
    A mixin that can be used to render a JSON response.
    """

    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(self.get_data(context), **response_kwargs)

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context


class GhnJsonView(JSONResponseMixin, View):
    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        try:
            ghn = GhnApiService()
            for key, value in request.GET.items():
                if not value:
                    raise Exception({"code": 400})

                if key == "province":
                    district = ghn.get_district_list(value)
                    if district.status_code == 200:
                        dict_data = district.json()
                        dict_data["data"] = format_option_data(
                            dict_data.get("data", list()),
                            value_key="DistrictID",
                            label_key="DistrictName",
                        )
                        return self.render_to_json_response(dict_data)
                    else:
                        raise Exception(district.json())
                elif key == "district":
                    ward = ghn.get_ward_list(value)
                    if ward.status_code == 200:
                        dict_data = ward.json()
                        dict_data["data"] = format_option_data(
                            dict_data.get("data", list()),
                            value_key="WardCode",
                            label_key="WardName",
                        )
                        return self.render_to_json_response(dict_data)
                    else:
                        raise Exception(ward.json())
                else:
                    raise Exception({"code": 400})
            else:
                province = ghn.get_province_list()
                if province.status_code == 200:
                    dict_data = province.json()
                    dict_data["data"] = format_option_data(
                        dict_data.get("data", list()),
                        value_key="ProvinceID",
                        label_key="ProvinceName",
                    )
                    return self.render_to_json_response(dict_data)
                else:
                    raise Exception(province.json())

        except Exception as error:
            err_dict = error.args[0]
            return self.render_to_json_response(err_dict, status=err_dict.get("code"))

    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            if body.get("districtId") is None and body.get("wardId") is None:
                raise Exception({"code": 400})
            ghn = GhnApiService()
            fee = ghn.calculate_delivery_fee(body.get("districtId"), body.get("wardId"))
            if fee.status_code == 200:
                dict_data = fee.json()
                return self.render_to_json_response(dict_data)
            else:
                error_payload = fee.json()
                error_payload["type"] = "not_supported"
                raise Exception(error_payload)

        except Exception as error:
            print("error: ", error)
            err_dict = error.args[0]
            return self.render_to_json_response(err_dict, status=err_dict.get("code"))


def format_option_data(data, *, value_key, label_key):
    sorted_data = sorted(
        map(
            lambda item: {
                "value": item[value_key],
                "label": item[label_key],
            },
            data,
        ),
        key=lambda x: x["label"],
    )
    sorted_data.insert(0, {"value": 0, "label": "N/A"})
    return sorted_data
