#!/usr/bin/env python
#coding=utf-8


def has_add_permission(admin_obj, request):
    """
    Returns True if the given request has permission to add an object.
    Can be overriden by the user in subclasses.
    """
    opts = admin_obj.opts
    return request.user.has_perm(opts.app_label + '.' + opts.get_add_permission())

def has_change_permission(admin_obj, request, obj=None):
    """
    Returns True if the given request has permission to change the given
    Django model instance, the default implementation doesn't examine the
    `obj` parameter.

    Can be overriden by the user in subclasses. In such case it should
    return True if the given request has permission to change the `obj`
    model instance. If `obj` is None, this should return True if the given
    request has permission to change *any* object of the given type.
    """
    opts = admin_obj.opts
    return request.user.has_perm(opts.app_label + '.' + opts.get_change_permission())

def has_delete_permission(admin_obj, request, obj=None):
    """
    Returns True if the given request has permission to change the given
    Django model instance, the default implementation doesn't examine the
    `obj` parameter.

    Can be overriden by the user in subclasses. In such case it should
    return True if the given request has permission to delete the `obj`
    model instance. If `obj` is None, this should return True if the given
    request has permission to delete *any* object of the given type.
    """
    opts = admin_obj.opts
    return request.user.has_perm(opts.app_label + '.' + opts.get_delete_permission())




