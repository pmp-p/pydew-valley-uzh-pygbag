import asyncio

renderer = None


def state_float(events):
    Loop.instance.set_state(state_idle)


def state_idle(events):
    pass


class GameState:
    screen = None
    instance = None

    def run(self):
        self.in_state = True
        while self.in_state:
            self.render([])
            pygame.display.update()

    def draw(self, events):
        pass

    def __call__(self, events):
        if self.update(events):
            self.draw(events)

    def update(self, events):
        return renderer

    def __repr__(self):
        return f"State({self.__class__.__name__})"


class Loop:
    last_state = None
    state = state_float
    instance = None
    closing = False

    def get_state(self, state):
        if state is None:
            return state_float

        if isinstance(state, str):
            gen = getattr(__import__(__name__), state)
        else:
            gen = state
        try:
            gen.instance
        except:
            return state

        if gen.instance is None:
            gen.instance = gen()
        return gen.instance

    def label(self, state):
        if isinstance(state, GameState):
            return repr(state)
        return state.__name__

    @classmethod
    def close(cls):
        cls.instance.closing = True

    def set_state(self, state):
        last_state = self.last_state or state_float

        if state:
            self.state = self.get_state(state)

        changed = self.last_state is not self.state
        self.last_state = self.state
        if changed:
            print("STATE:", self.label(last_state), "=>", self.label(self.state))
        return changed

    @classmethod
    def start(cls, entry_point, event_generator, exit_point=None):
        global renderer
        cls.instance = cls()
        cls.event_generator = event_generator
        cls.instance.exit_point = exit_point
        cls.instance.set_state(entry_point)
        cls.instance.state([])
        renderer = True
        return cls.instance.run()

    async def run(self):
        try:
            asyncloop = asyncio.get_event_loop()
            while not self.closing and not asyncloop.is_closed():
                events = self.event_generator()
                if events:
                    self.state(events)

        except asyncio.exceptions.CancelledError:
            print("Cancelled")
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
        except SystemExit:
            print("SystemExit")
        finally:
            # TTY.set_raw(0)
            print("108: Killing tasks, FIXME: restart REPL for WASM")
            if self.exit_point:
                await self.exit_point()
