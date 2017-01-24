from automaton import machines
from automaton import runners


# These reaction functions will get triggered when the registered state
# and event occur, it is expected to provide a new event that reacts to the
# new stable state (so that the state-machine can transition to a new
# stable state, and repeat, until the machine ends up in a terminal
# state, whereby it will stop...)



def test_1():
    m = machines.FiniteMachine()
    m.add_state('up')
    m.add_state('down')
    m.add_transition('down', 'up', 'jump')
    m.add_transition('up', 'down', 'fall')
    m.default_start_state = 'down'
    print(m.pformat())

    m.initialize()
    m.process_event('jump')
    print(m.pformat())
    print(m.current_state)
    print(m.terminated)
    m.process_event('fall')
    print(m.pformat())
    print(m.current_state)
    print(m.terminated)


def test_2():
    def react_to_squirrel(old_state, new_state, event_that_triggered):
        return "gets petted"
    def react_to_wagging(old_state, new_state, event_that_triggered):
        return "gets petted"

    m = machines.FiniteMachine()

    m.add_state("sits")
    m.add_state("lies down", terminal=True)
    m.add_state("barks")
    m.add_state("wags tail")

    m.default_start_state = 'sits'

    m.add_transition("sits", "barks", "squirrel!")
    m.add_transition("barks", "wags tail", "gets petted")
    m.add_transition("wags tail", "lies down", "gets petted")

    m.add_reaction("barks", "squirrel!", react_to_squirrel)
    m.add_reaction('wags tail', "gets petted", react_to_wagging)

    print(m.pformat())
    r = runners.FiniteRunner(m)
    for (old_state, new_state) in r.run_iter("squirrel!"):
        print("Leaving '%s'" % old_state)
        print("Entered '%s'" % new_state)

def test_3():
    def print_on_enter(new_state, triggered_event):
       print("Entered '%s' due to '%s'" % (new_state, triggered_event))


    def print_on_exit(old_state, triggered_event):
        print("Exiting '%s' due to '%s'" % (old_state, triggered_event))
    m = machines.FiniteMachine()

    m.add_state('stopped', on_enter=print_on_enter, on_exit=print_on_exit)
    m.add_state('opened',  on_enter=print_on_enter, on_exit=print_on_exit)
    m.add_state('closed',  on_enter=print_on_enter, on_exit=print_on_exit)
    m.add_state('playing',  on_enter=print_on_enter, on_exit=print_on_exit)
    m.add_state('paused',  on_enter=print_on_enter, on_exit=print_on_exit)

    m.add_transition('stopped', 'playing', 'play')
    m.add_transition('stopped', 'opened', 'open_close')
    m.add_transition('stopped', 'stopped', 'stop')

    m.add_transition('opened', 'closed', 'open_close')

    m.add_transition('closed', 'opened', 'open_close')
    m.add_transition('closed', 'stopped', 'cd_detected')

    m.add_transition('playing', 'stopped', 'stop')
    m.add_transition('playing', 'paused', 'pause')
    m.add_transition('playing', 'opened', 'open_close')

    m.add_transition('paused', 'playing', 'play')
    m.add_transition('paused', 'stopped', 'stop')
    m.add_transition('paused', 'opened', 'open_close')

    m.default_start_state = 'closed'

    m.initialize()
    print(m.pformat())
    for event in ['cd_detected', 'play', 'pause', 'play', 'stop',
                  'open_close', 'open_close']:
        m.process_event(event)
        print(m.pformat())
        print("=============")
        print("Current state => %s" % m.current_state)
        print("=============")

def test_4():
    def print_on_enter(new_state, triggered_event):
       print("Entered '%s' due to '%s'" % (new_state, triggered_event))
    def print_on_exit(old_state, triggered_event):
       print("Exiting '%s' due to '%s'" % (old_state, triggered_event))

    # This will contain all the states and transitions that our machine will
    # allow, the format is relatively simple and designed to be easy to use.
    state_space = [
        {
            'name': 'stopped',
            'next_states': {
                # On event 'play' transition to the 'playing' state.
                'play': 'playing',
                'open_close': 'opened',
                'stop': 'stopped',
            },
            'on_enter': print_on_enter,
            'on_exit': print_on_exit,
        },
        {
            'name': 'opened',
            'next_states': {
                'open_close': 'closed',
            },
            'on_enter': print_on_enter,
            'on_exit': print_on_exit,
        },
        {
            'name': 'closed',
            'next_states': {
                'open_close': 'opened',
                'cd_detected': 'stopped',
            },
            'on_enter': print_on_enter,
            'on_exit': print_on_exit,
        },
        {
            'name': 'playing',
            'next_states': {
                'stop': 'stopped',
                'pause': 'paused',
                'open_close': 'opened',
            },
            'on_enter': print_on_enter,
            'on_exit': print_on_exit,
        },
        {
            'name': 'paused',
            'next_states': {
                'play': 'playing',
                'stop': 'stopped',
                'open_close': 'opened',
            },
            'on_enter': print_on_enter,
            'on_exit': print_on_exit,
        },
    ]

    m = machines.FiniteMachine.build(state_space)
    m.default_start_state = 'closed'
    print(m.pformat())

if __name__ == '__main__':
    # test_2()
    # test_3()
    test_4()