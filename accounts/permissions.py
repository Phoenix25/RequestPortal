from pybb import defaults

from pybb.permissions import DefaultPermissionHandler as PermissionHandler


class CustomPermissionHandler(PermissionHandler):
	# define overrides over certain pybb permission functions.
	def may_view_forum(self, user, forum):
		return super(CustomPermissionHandler, self).may_view_forum(user, forum) and user.is_authenticated()