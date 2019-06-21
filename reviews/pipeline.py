from django.conf import settings

from requests_oauthlib import OAuth1Session

from .models import Critic

def create_critic(backend, user, response, *args, **kwargs):
    try:
        user.critic

        #update name if it has changed
        if user.get_full_name() != response.get('name'):
            full_name = response.get('name').split(" ", 1)
            user.first_name = full_name[0]
            user.last_name = full_name[1]
            user.save()

        #automatically follow twitter friends
        '''
        social = user.social_auth.get(provider='twitter')
        print(social.extra_data['access_token'])
        friends = requests.get(
            'https://api.twitter.com/1.1/friends/list.json',
            params={
                'user_id': social.extra_data['access_token']['user_id']
            }
        )
        print(friends.json())
        '''
        social = user.social_auth.get(provider='twitter')
        twitter_session = OAuth1Session(
            client_key=settings.SOCIAL_AUTH_TWITTER_KEY,
            client_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
            resource_owner_key=social.extra_data['access_token']['oauth_token'],
            resource_owner_secret=social.extra_data['access_token']['oauth_token_secret']
        )
        r = twitter_session.get('https://api.twitter.com/1.1/friends/list.json')
        print(r.json)
        
    except Critic.DoesNotExist:
        critic = Critic(user=user, slug=user.username)
        critic.save()
