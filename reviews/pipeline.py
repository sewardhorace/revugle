from django.apps import apps
from django.conf import settings

from actstream.actions import follow
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
        
    except Critic.DoesNotExist:
        critic = Critic(user=user, slug=user.username)
        critic.save()

        #automatically follow self
        follow(user, critic)

        #automatically follow twitter friends if they exist
        social = user.social_auth.get(provider='twitter')
        twitter_session = OAuth1Session(
            client_key=settings.SOCIAL_AUTH_TWITTER_KEY,
            client_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
            resource_owner_key=social.extra_data['access_token']['oauth_token'],
            resource_owner_secret=social.extra_data['access_token']['oauth_token_secret']
        )
        User = apps.get_app_config('auth').get_model('User')
        next_cursor = -1
        while next_cursor != 0:
            r = twitter_session.get('https://api.twitter.com/1.1/friends/list.json?cursor={}&count=200'.format(next_cursor)).json()
            next_cursor = r['next_cursor']
            for friend in r['users']:
                print(friend['screen_name'])
                try:
                    friend = User.objects.get(username=friend['screen_name'])
                    follow(user, friend.critic)
                except User.DoesNotExist:
                    continue
