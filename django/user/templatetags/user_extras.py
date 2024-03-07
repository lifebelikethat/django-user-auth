from django import template

register = template.Library()


def get_field(self, field):
    if field in self.keys():
        return self[field]
    else:
        return ""


register.filter('get_field', get_field)
