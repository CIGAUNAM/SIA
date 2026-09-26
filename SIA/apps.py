from django.contrib.admin.apps import AdminConfig


class SIAAdminConfig(AdminConfig):
    default_site = 'SIA.admin_site.SIAAdminSite'
