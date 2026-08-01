from speech import Speech_handler
from greet import Greet
from wakeword import WakeListener
from system_cmd import ZoraCommands


def main():
    # Initialize core components
    speech = Speech_handler()
    greet = Greet()
    wake = WakeListener(["zora", "hey zora"])
    commands = ZoraCommands()

    # Step 1: Wait for wake word
    wake.listen()

    # Step 2: Greet the user
    greet.wish(speech)

    # Step 3: Main interaction loop
    while True:
        query = speech.takecommand()

        if query == "none":
            continue

        commands.handle(query, speech)


if __name__ == "__main__":
    main()
