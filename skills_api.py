def authenticate_user(condition, message):
    if condition["card_type"] in ['#authentication','#card']:
        return "submitted"
    else:
        return message
