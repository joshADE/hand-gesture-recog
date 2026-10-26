from abc import ABC, abstractmethod
from typing import Any, Dict, List
from keyboard_input import KeyBoardInput
from observer import Event, KeyObserver, KeySubject

class KeyBinding(ABC):
    @abstractmethod
    def get_key(self) -> str:
        pass

    @abstractmethod
    def get_action(self) -> lambda Event, Any: bool:
        pass

class KeyManager(KeySubject):
    _observers: Dict[str, List[KeyObserver]] = {}
    _keyboard_input: KeyBoardInput

    def __init__(self, keyboard_input: KeyBoardInput):
        self._keyboard_input = keyboard_input


    def attach(self, key: str,  observer: KeyObserver) -> None:
        print("Subject: Attached an observer.")
        if key not in self._observers:
            self._observers[key] = []
        self._observers[key].append(observer)

    def detach(self, key: str, observer: KeyObserver) -> None:
        if key in self._observers:
            self._observers[key].remove(observer)

    def notify(self, event: Event) -> None:
        print("Subject: Notifying observers...")
        for observer in self._observers.get(event.key, []):
            observer.update(self, event)

    def handle_key_events(self, data: Any) -> None:
        key = self._keyboard_input.get_key()
        if key is not None:
            event = KeyEvent(name="Key Pressed", key=key, data=data)
            self.notify(event)

    def register_key_binding(self, key_binding: KeyBinding) -> None:
        self.attach(key_binding.get_key(), key_binding)


class KeyObserver(KeyObserver):
    def update(self, subject: KeySubject, event: Event) -> None:
        if isinstance(subject, KeyManager):
            print(f"Observer: Reacted to the event: {event.name}")


class KeyEvent(Event):
    def __init__(self, name: str, key: str, data: Any = None):
        super().__init__(name)
        self.key = key
        self.data = data



class KeyBindingImpl(KeyBinding, KeyObserver):
    def __init__(self, key: str, action: lambda KeyEvent, Any: bool):
        self._key = key
        self._action = action

    def get_key(self) -> str:
        return self._key

    def get_action(self) -> lambda KeyEvent, Any: bool:
        return self._action

    def update(self, subject: KeySubject, event: Event) -> None:
        if isinstance(subject, KeyManager) and isinstance(event, KeyEvent):
            if event.key == self._key:
                print(f"KeyBinding: Executing action for key: {self._key}")
                self._action(event, event.data)