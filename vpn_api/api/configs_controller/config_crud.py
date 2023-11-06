from utils.create_conf import main


def create_user_config(user_id: str):
    config = main(user_id)
    return config
