def user_session_processor(request):
    if 'current_user' in request.session:
        current_user = request.session['current_user']
        user_type = request.session['user_type']
        return {
            'current_user': current_user,
            'user_type': user_type
        }