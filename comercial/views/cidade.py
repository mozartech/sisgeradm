import simplejson

from django import http

from comercial.models import Cidade


class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing ’context’ as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an ‘HttpResponse‘ object."
        return http.HttpResponse(content,
                   content_type='application/json',
                   **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you’ll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return simplejson.dumps(context)

def CidadeUFView(request, uf):
    nomes = []
    for cidade in Cidade.objects.filter(uf=uf.strip().upper()):
        nomes.append(cidade.nome)
    content = simplejson.dumps(nomes)
    return http.HttpResponse(content, content_type='application/json')

def CidadeView(request):
    nomes = []
    for cidade in Cidade.objects.all():
        nomes.append(cidade.nome)
    content = simplejson.dumps(nomes)
    return http.HttpResponse(content, content_type='application/json')