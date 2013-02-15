from django.template import RequestContext, loader
from django.http import HttpResponse

def application_notfound(request):
    t = loader.get_template('404.html')
    return HttpResponse(t.render(c), status=404)