# take out once convert everything to renders and have views created for them
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Migration

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'dicalendar/index.html'
    context_object_name = 'latest_migration_list'

    def get_queryset(self):
        """Return the last five published migrations (not including those set to be published in the future)."""
        return Migration.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Migration
    template_name = 'dicalendar/detail.html'


class ResultsView(generic.DetailView):
    model = Migration
    template_name = 'dicalendar/results.html'


def vote(request, migration_id):
    migration = get_object_or_404(Migration, pk=migration_id)
    try:
        selected_choice = migration.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the migration voting form
        return render(request, 'dicalendar/detail.html', {
            'migration': migration,
            'error_message': "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponse Redirect after successfully dealing with POST data.  This prevents data from being posted twice if a user hits the back button.
        return HttpResponseRedirect(reverse('dicalendar:results', args=(migration_id,)))
