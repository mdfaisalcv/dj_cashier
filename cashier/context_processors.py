from django.urls import resolve

def cashier_context(request):
    # Extract controller name from path like /cashier/segment/index
    try:
        parts = request.path.strip('/').split('/')
        # Usually /cashier/<controller>/<action>
        # If it's just /cashier/ then controller_name is 'dashboard'
        if len(parts) > 1:
            controller_name = parts[1]
        else:
            controller_name = 'dashboard'
    except Exception:
        controller_name = 'dashboard'
    
    # Mock roles - in a real app, these would come from the database or session
    # For now, we set them to True so the sidebar shows everything
    # Using a simple dictionary for roles as used in templates: roles.segment_manage
    roles = {
        'segment_manage': True, 'segment_view': True,
        'device_manage': True, 'device_view': True,
        'publication_manage': True, 'publication_view': True,
        'adsize_manage': True, 'adsize_view': True,
        'geo_target_manage': True, 'geo_target_view': True,
        'industry_manage': True, 'industry_view': True,
        'site_manage': True, 'site_view': True,
        'section_manage': True, 'section_view': True,
        'palo_user_manage': True, 'palo_user_view': True,
        'calendar_settings_manage': True, 'calendar_settings_view': True,
        'contact_manage': True, 'contact_view': True,
    }

    return {
        'controller_name': controller_name,
        'roles': roles,
        'status_counts': {'total': 0, 'pending': 0, 'approved': 0}, # Mock
        'status_counts_integration': 0, # Mock
    }
