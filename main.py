
from datetime import datetime 
from ui import CelestialApp

def main():
    now = datetime.now()

    app = CelestialApp()
    app.run()

if __name__ == "__main__":
    main()
