from simple_banking_system.console_menus import ContextMenu


def run():
    entry_point = ContextMenu()
    while True:
        next_ = entry_point.execute()
        if not next_:
            break

    print('Bye!')


if __name__ == "__main__":
    run()
