

PINS = (24,  8, 27, 10, 11,
        23, 25,  7, 22,  9)

LAYERS = (
    # BASE
    ((1, 's'), 't', 'r', (2, 'a'), '(',
     'o',      'i', 'y', (3, 'e'), ')'),

    # NUMBER
    ('', '3', '2', '1', '',
     '', '6', '5', '4', ''),

    # PARENS
    ('}', '(', ')', '', '',
     '{', '[', ']', '', ''),

    # SYMBOL
    ('`', ';', '\\', '!', '',
     '=', '-', '?',  '',  ''),

    # NAV
    ('_pgup', '_home', '_up',   '_end',  '',
     '_pgdn', '_left', '_down', '_rght', ''),

    # MOUSE
    ('_scup', '_mbt2', '_mup',  '_mbt1', '_mbt3',
     '_scdn', '_mlft', '_mdwn', '_mrgt', '_mbt1')
)

CHORDS = {
    ### BASE LAYER ###
    #                       'a',
    ('o', 'e'):             'b',
    ('y', 'e'):             'c',
    ('a', 'r', 't'):        'd',
    #                       'e',
    ('a', 'r'):             'f',
    ('r', 't'):             'g',
    ('i', 'e'):             'h',
    #                       'i',
    ('s', 't'):             'j',
    ('o', 'y'):             'k',
    ('e', 'y', 'i'):        'l',
    ('o', 'i', 'y'):        'm',
    ('o', 'i'):             'n',
    #                       'o',
    ('o', 'i', 'e'):        'p',
    ('s', 't', 'a'):        'q',
    #                       'r',
    #                       's',
    #                       't',
    ('y', 'i'):             'u',
    ('s', 'r'):             'v',
    ('s', 'a'):             'w',
    ('s', 't', 'r'):        'x',
    #                       'y',
    ('s', 't', 'r', 'a'):   'z',
    #
    ('1', '2'):             '7',
    ('2', '3'):             '8',
    ('4', '5'):             '9',
    ('5', '6'):             '0',
    ('4', '2'):             '_bksp',
    ('4', '1'):             '_entr',
    ('_rght', '_end'):      '_entr',
    #
    ('o', 'i', 'y', 'e'):   ' ',
    ('y', 'a'):             '.',
    ('i', 'a'):             ',',
    ('a', 'o'):             '/',
    ('a', 'i', 'y'):        "'",
    ('t', 'i'):             '!',
    ('(', ')'):             ':',
    ('o', 't', 'r', 'a'):   '_tab',
    ('_pgdn','_home', 
        '_up', '_end',):    '_tab',
    ('a', 'e'):             '_entr',
    ('s', 'e'):             '_os_ctrl',
    ('s', 'i'):             '_alt',
    ('s', 't', 'r', 'e'):   '_os_shft',
    ('r', 'e'):             '_bksp',
    ('o', 'r', 'a'):        '_esc',
    # Nav Layer:
    ('e', 'r', 'i'):            ('_set_base', 4),   
    ('_left', '_up', '_rght'):  ('_set_base', 0),
    # Mouse Layer:
    ('a', 't', 'y'):            ('_set_base', 5),
    ('_mbt1', '_mdwn', '_mbt2'): ('_set_base', 0),
    ('_up', '_rght'):       '_bksp',
    ('_mup', '_mrgt'):      '_mdur', # Mouse diagonal up right
    ('_mup', '_mlft'):      '_mdul', # Mouse diagonal up left
    ('_mdwn', '_mrgt'):     '_mddr', # Mouse diagonal down right
    ('_mdwn', '_mlft'):     '_mddl', # Mouse diagonal down left
}

# Sort the keys for comparison later
CHORDS = dict([(tuple(sorted(k)), v) for k, v in CHORDS.items()])
