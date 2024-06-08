from environs import Env

env = Env()
env.read_env()
PUBLIC_KEY = env("DISCORD_BOT_PUBLIC_KEY")

INTERACTION_TYPES = {
    "PING": 1,
    "APPLICATION_COMMAND": 2,
}

CALLBACK_TYPES = {
    "PONG": 1,
    "CHANNEL_MESSAGE_WITH_SOURCE": 4,
}
