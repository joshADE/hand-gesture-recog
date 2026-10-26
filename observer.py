from __future__ import annotations
from abc import ABC, abstractmethod

class KeySubject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def attach(self, key: str, observer: KeyObserver) -> None:
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, key: str, observer: KeyObserver) -> None:
        """
        Detach an observer from the subject.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        pass


class KeyObserver(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject: KeySubject, event: Event) -> None:
        """
        Receive update from subject.
        """
        pass


class Event:
    """
    The Event class represents an event that can be observed by observers.
    """

    def __init__(self, name: str):
        self.name = name
