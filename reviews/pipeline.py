from .models import Critic

def create_critic(backend, user, response, *args, **kwargs):
	try:
		user.critic
	except Critic.DoesNotExist:
		critic = Critic(user=user)
		critic.save()
		
