def get_avatar(backend, strategy, details, response,
        user=None, *args, **kwargs):
    url = None
    if backend.name == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large"%response['id']
        # if you need a square picture from fb, this line help you
        url = "http://graph.facebook.com/%s/picture?width=150&height=150"%response['id']
    if backend.name == 'twitter':
        url = response.get('profile_image_url', '').replace('_normal','')
    if backend.name == 'google-oauth2':
        # print(response['picture'])
        # url = response['picture'].get('url')
        url = response['picture']
        # url = url.replace('?sz=50', '?sz=200')
    if url:
        user.profile.avatar = url
        user.save()
