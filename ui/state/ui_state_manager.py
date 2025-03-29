# /ui/state/ui_state_manager.py

from enum import Enum, auto
from PySide6.QtWidgets import QStackedWidget
from logger.logger import LoggerFactory

# Import screen classes so they can be registered
from ui.screens.welcome import WelcomeScreen
from ui.screens.planetgen import PlanetGenScreen

logger = LoggerFactory("ui_state_manager").get_logger()


class UIState(Enum):
    """
    Represents the current active screen/view/state of the UI.
    """
    WELCOME = auto()
    PLANETGEN = auto()  # The New Game button leads here.
    LOAD_GAME = auto()
    SETTINGS = auto()
    ABOUT = auto()
    GAMEPLAY = auto()


class UIStateManager(QStackedWidget):
    """
    Manages transitions between different UI screens using QStackedWidget.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.screens = {}
        self.current_state = None

        # Register all initial screens
        self._register_initial_screens()

    def _register_initial_screens(self):
        """
        Create and register default screens.
        """
        self.register_screen(UIState.WELCOME, WelcomeScreen(self))
        self.register_screen(UIState.PLANETGEN, PlanetGenScreen(self))
        self.set_state(UIState.WELCOME)

    def register_screen(self, state: UIState, widget):
        """
        Adds a screen to the state manager and maps it to a state enum.
        """
        logger.debug(f"Registering screen: {state.name}")
        self.screens[state] = widget
        self.addWidget(widget)

    def set_state(self, state: UIState):
        """
        Switches to the screen associated with the given state.
        """
        if state not in self.screens:
            logger.error(f"UI state '{state.name}' has not been registered.")
            return

        logger.info(f"Switching UI state to: {state.name}")
        self.setCurrentWidget(self.screens[state])
        self.current_state = state
