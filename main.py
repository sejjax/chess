from chess.app import App
import curses

def main():
    app = App()
    app.run()
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        curses.endwin()
