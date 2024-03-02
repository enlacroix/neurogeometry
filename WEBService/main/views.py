from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
# from .wrapper import get_logic
from .wrapper import to_algorithm, get_empty_dict
import json


@csrf_exempt
def redirect_to_main(request):
    return redirect('main_page')


class MainViewMain(View):
    def get(self, request, *args, **kwargs):
        return render(request, '_base_vue.html')


@csrf_exempt
def try_solve(request):
    # print(request.body)
    if request.method == 'POST':
        return JsonResponse(to_algorithm(json.loads(request.body)))
    return JsonResponse(get_empty_dict())
