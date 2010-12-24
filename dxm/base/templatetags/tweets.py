from django.template import Library
from django.utils.safestring import mark_safe
import re

register = Library()

@register.filter
def tweet(value):
	value = re.sub(r'((mailto\:|(news|(ht|f)tp(s?))\://){1}\S+)', '<a href="\g<0>" rel="external">\g<0></a>', value)
	value = re.sub(r'http://(yfrog|twitpic).com/(?P<id>\w+/?)', '', value)
	value = value.replace('<a ', '<a target="_blank" ')
	value = re.sub(r'#(?P<tag>\w+)', '<a href="/search?q=%23\g<tag>">#\g<tag></a>', value)
	value = re.sub(r'@(?P<username>\w+)', '@<a href="/profile/\g<username>/">\g<username></a>', value)
	return mark_safe(value)


def tweet_attachments(ex, value, max_items = -1):
	start = 0
	matches = ex.search(value, start)
	ids = []
	
	while matches:
		groupdict = matches.groupdict()
		if 'id' in groupdict:
			if not groupdict['id'] in ids:
				ids.append(groupdict['id'])
		
		start = matches.end()
		matches = ex.search(value, start)
	
	if max_items > -1:
		ids = ids[:max_items]
	
	return ids

@register.simple_tag
def yfrog_images(value, max_items = -1, lightbox = None):
	ex = re.compile(r'http://yfrog.com/(?P<id>\w+/?)')
	ids = tweet_attachments(ex, value, max_items)
	
	classes = ['yfrog-thumbnail']
	if lightbox:
		classes += [lightbox]
		extension = ':iphone'
	else:
		extension = ''
	
	urls = '\n'.join(
		[
			'<a href="http://yfrog.com/%(id)s%(extension)s" class="%(classes)s" rel="external"><img src="http://yfrog.com/%(id)s.th.jpg" /></a>' % {
				'id': i,
				'classes': ' '.join(classes),
				'extension': extension
			} for i in ids
		]
	)
	
	return mark_safe(urls)

@register.simple_tag
def twitpic_images(value, max_items = -1, lightbox = None):
	ex = re.compile(r'http://twitpic.com/(?P<id>\w+/?)')
	ids = tweet_attachments(ex, value, max_items)
	
	classes = ['twitpic-thumbnail']
	if lightbox:
		classes += [lightbox]
	
	urls = '\n'.join(
		[
			'<a href="http://twitpic.com/show/full/%(id)s" class="%(classes)s" rel="external"><img src="http://twitpic.com/show/thumb/%(id)s" /></a>' % {
				'id': i,
				'classes': ' '.join(classes),
			} for i in ids
		]
	)

	return mark_safe(urls)