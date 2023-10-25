import keyboard

# Functie die wordt uitgevoerd wanneer de toets wordt ingedrukt
def on_key_event(e):
    if e.name == 'a':  # Hier wordt gecontroleerd of de toets 'a' is ingedrukt
        print("Toets 'a' is ingedrukt.")
        # Voer hier je code uit die je in de 'if'-lus wilt starten

# Voeg een toetsaanslag-gebeurtenis toe die de functie 'on_key_event' activeert
keyboard.on_press(on_key_event)

# Wacht tot de toets 'q' wordt ingedrukt om het programma te stoppen
keyboard.wait('q')

# Sluit het programma
keyboard.unhook_all()
