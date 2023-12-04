from django.shortcuts import redirect, render

from feedbacks.models import Feedback
from search.models import Manuscript
import re

# Create your views here.
def feedback(request):
    data = request.GET.get('feedback_manuscript')
    id_number = re.search(r'\((\d+)\)', data).group(1)
    print(id_number)
    
    feedback_manuscript=Manuscript.objects.get(pk=id_number)
    if request.method == 'POST':
        feedback_content=request.POST.get('content')
        feedback_score=request.POST.get('rate')
        feedback_owner=request.user
        print(feedback_content, feedback_score, feedback_owner, feedback_manuscript)

        f = Feedback()
        f.createFeedback(feedback_owner, feedback_manuscript, feedback_content, feedback_score)
        f.save()

        return redirect('search')
    return render(request, 'feedbacks/feedback.html')