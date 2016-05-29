import sys
from app.ieee.controller import Controller

if __name__ == '__main__':
    journal = Controller.get_journal(sys.argv[1])
    journal.get_current_issue().update()
    journal.get_early_access().update()
