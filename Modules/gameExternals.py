def increment(button, value, cap, increaseFactor, decreasedValue = 0, decreaseFactor = 0):
    if button.pressed[0] == True:
        if value < cap:
            value += increaseFactor
            decreasedValue -= decreaseFactor
    if button.pressed[1] == True:
        if value > 0:
            value -= increaseFactor
            decreasedValue += decreaseFactor
    
    if decreasedValue < 0:
        decreasedValue = 0
    
    return value, decreasedValue

# def incrementIf(button, value, increaseFactor, cap, comparison):
#     if button.pressed[0] == True:
#         if comparison == True:
#             if value < cap:
#                 value += increaseFactor
#     if button.pressed[1] == True:
#         if comparison == True:
#             if value > 0:
#                 value -= increaseFactor
    
#     return value

def getButtonPress(button):
    if button.pressed[0] == True:
        return True
    if button.pressed[1] == True:
        return True