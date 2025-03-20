from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from .models import Profile
from xhtml2pdf import pisa

# Create your views here.

def accept(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        summary = request.POST.get('summary')
        degree = request.POST.get('degree')
        school = request.POST.get('school')
        university = request.POST.get('university')
        previous_work = request.POST.get('previous_work')
        skills = request.POST.get('skills')
        profile = Profile(name=name, email=email, phone=phone, summary=summary, degree=degree, school=school, university=university, previous_work=previous_work, skills=skills)
        profile.save()
    return render(request, 'pdf/accept.html')

def resume(request, id):
    user_profile = Profile.objects.get(id=id)
    template = get_template('pdf/resume.html')
    html = template.render({'user_profile': user_profile})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    pisaStatus = pisa.CreatePDF(html, dest=response)
    if pisaStatus.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def list(request):
    profiles = Profile.objects.all()
    return render(request, 'pdf/list.html', {'profiles': profiles})