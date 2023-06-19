from django.contrib.admin import ModelAdmin


def get_permission_codename(action, opts):
    """
    Returns the codename of the permission for the specified action.
    """
    return '%s_%s' % (action, opts.module_name)


class BaseAdmin(ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        """
        Add object permissions to the check for delete permissions.
        Module-level permissions will trump object-level permissions.
        """
        opts = self.opts
        codename = get_permission_codename('delete', opts)
        return any([
            request.user.has_perm("%s.%s" % (opts.app_label, codename)),
            request.user.has_perm("%s.%s" % (opts.app_label, codename), obj)])

    def has_change_permission(self, request, obj=None):
        """
        Add object permissions to the check for change permissions.
        Module-level permissions will trump object-level permissions.
        """
        opts = self.opts
        codename = get_permission_codename('change', opts)
        return any([
            request.user.has_perm("%s.%s" % (opts.app_label, codename)),
            request.user.has_perm("%s.%s" % (opts.app_label, codename), obj)])

    def has_view_permission(self, request, obj=None):
        """
        Check for view permissions. Module-level permissions will trump
        object-level permissions.
        """
        return True
        opts = self.opts
        codename = get_permission_codename('view', opts)
        return any([
            request.user.has_perm("%s.%s" % (opts.app_label, codename)),
            request.user.has_perm("%s.%s" % (opts.app_label, codename), obj)])
