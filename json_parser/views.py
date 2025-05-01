from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, View
from home.models import Profile
from django.http import JsonResponse
from .services import parse
from django.core.exceptions import ValidationError

class ParserDemoView(TemplateView):
    template_name = 'json_parser/json_parser.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.first()
        return context
    
class ParseJSONAjaxView(View):
    def post(self, request):
        raw_json = request.POST.get('json_input')
        json_file = request.FILES.get('json_file')

        try:
            if json_file:
                if validate_json_file(json_file):
                    json_str = json_file.read().decode('utf-8')
            elif raw_json:
                json_str = raw_json
            else:
                raise ValueError("No JSON input provided.")

            parsed_data = parse(json_str)

            return JsonResponse({'status': 'success', 'data': parsed_data})
        
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
                },  status=400)
        
def validate_json_file(file):
    if not file.name.endswith('.json'):
        raise ValidationError("File is not a valid JSON file.")
    if file.size > 5 * 1024 * 1024:
        raise ValidationError("File size exceeds 5MB limit.")