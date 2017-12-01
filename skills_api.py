def authenticate_user(condition, message):
    if condition["card_type"] == '#authentication':
        return "submitted"
    else:
        return message

