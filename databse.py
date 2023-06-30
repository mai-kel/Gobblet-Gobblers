import pickle


def get_data():
    """
    Function returns list of Game objects, which are stored in databse.pkl file
    """
    try:
        with open('database.pkl', 'rb') as handler:
            return pickle.load(handler)
    except EOFError:
        return []
    except FileNotFoundError:
        return []


def save_game(game):
    """
    Function saves Game object given as an argument to databse.pkl file
    """
    list = get_data()
    list.append(game)
    with open('database.pkl', 'wb') as handler:
        pickle.dump(list, handler)
