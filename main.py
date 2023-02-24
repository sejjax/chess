from chess.app import App

def main():
    app = App()
    app.run()
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
