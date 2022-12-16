from tatu_re.model import train_model, train_set

if __name__ == "__main__":
    X, y = train_set()
    model = train_model(X, y, save=True)