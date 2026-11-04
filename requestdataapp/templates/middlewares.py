from django.http import HttpRequest, HttpResponseForbidden
from django.shortcuts import render
import time


def set_useragent_on_request_middleware(get_response):
    def middleware(request: HttpRequest):
        request.user_ip = request.META["REMOTE_ADDR"]
        response = get_response(request)
        return response

    return middleware


class LimitIpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.user_ip_limit = 0
        self.time_limit = 10
        self.last_reset_time = time.time()

    def __call__(self, request: HttpRequest):
        current_time = time.time()
        if current_time - self.last_reset_time > self.time_limit:
            self.user_ip_limit = 0
            self.last_reset_time = current_time

        response = self.get_response(request)
        self.user_ip_limit += 1
        if self.user_ip_limit > 5:
            context = {
                "error_title": "Ooops",
                "error_text": "Too many requests from your IP address."
            }
            return render(request, "requestdataapp/error.html", context=context)

        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        context = {
            "error_title": "An error has occurred on the site",
            "error_text": exception.__str__()
        }
        return render(request, "requestdataapp/error.html", context=context)
