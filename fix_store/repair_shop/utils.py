menu = [
    {'title': "Головна", 'url_name': "another"},
    {'title': "Контакти", 'url_name': "contacts"},
    {'title': "Черга", 'url_name': "queued"},
    {'title': "Прийомка", 'url_name': "new_order"},
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context