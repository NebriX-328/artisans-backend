from django.http import JsonResponse
from ai_services.main_service import run_ai_services

def ai_service_view(request):
    user_query = request.GET.get("query", "handmade pottery")
    product_data = {"name": request.GET.get("product", "Clay Vase")}
    artisan_details = {"name": request.GET.get("artisan", "Ravi")}

    result = run_ai_services(user_query, product_data, artisan_details)
    return JsonResponse(result)
