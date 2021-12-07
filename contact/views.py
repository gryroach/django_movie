from django.views.generic import CreateView

from .models import Contact
from .forms import ContactForm


# представление для сохранения введенной формы
class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
#   перенаправление в случае успеха
    success_url = '/'

