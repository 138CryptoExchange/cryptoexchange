def user_session_processor(request):
    if request.session['current_user']:
        return {
            'current_user': request.session['current_user'],
        }
    else:
        return{
            'current_user': False,
        }