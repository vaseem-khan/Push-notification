from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def notif_count(context):
	request = context['request']
	if request.user.is_authenticated():
		current_user = request.user.userprofile
		unread = current_user.Notifications.filter(viewed=False)
		return len(unread)
	else:
		return 0



