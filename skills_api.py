def authenticate_user(condition):
    if condition['card_type'] == '#authentication':
        return "submitted"
