from django import template
import socket
import fcntl
import struct


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

@register.simple_tag(takes_context=True)
def ip_address(context):
	try:
		return get_ip_address('eth0')
	except:
		try:
			return get_ip_address('wlan0')
		except:
			return "localhost"


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])
