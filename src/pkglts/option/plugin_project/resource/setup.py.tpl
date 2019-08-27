# {# pkglts, plugin_project, after pysetup.kwds
setup_kwds['entry_points']['pkglts'] = [
    '{{ plugin_project.plugin_name }} = {{ base.pkg_full_name }}.option:Option{{ plugin_project.plugin_name|capitalize }}',
]
# #}
