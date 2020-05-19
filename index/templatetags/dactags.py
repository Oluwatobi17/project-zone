from django import template

register = template.Library()

# @register.inclusion_tag('view.html')
@register.simple_tag
def commalizer(num):
	""" The function add comma figure """
	num = str(num)
	if len(num)<=3:
		return num

	count = 1
	a = len(num) - 1
	res = ""
	while a>=0:
		if count==3 and (not a==0):
			res += num[a]
			res += ","
			count = 0
		else:
			res += num[a]

		count += 1
		a -= 1

	final = ""
	b = len(res)-1
	while b>=0:
		final += res[b]
		b -= 1
	return final