PINS = ( 0,  1,  2,  3,  4,  5,  6,  7,  8,  9,
        10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
        20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
        '', '', 32, 33, 34, 35, 36, 37, '', '',

#       L   D   U   R   C   L   D   U   R   C
        54, 50, 53, 52, 51, 57, 56, 59, 55, 58,
        44, 40, 43, 42, 41, 47, 46, 49, 45, 48,)
#        50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
#        40, 41, 42, 43, 44, 45, 46, 47, 48, 49,)
#        40, 41, 42, 43, 44, 50, 51, 52, 53, 54,
#        45, 46, 47, 48, 49, 55, 56, 57, 58, 59)

#       up 53, rt 52, dn 50, lf 54, in 51
#       up 43, rt 42, dn 40, lf 44, in 41
#       up 59, rt 55, dn 56, lf 57, in 58
#       up 49, rt 45, dn 46, lf 47, in 48
#       
#       50-54   55-59
#       40-44   45-49
ENCODER = ()

    # B0,  B1,  B2,  B3,  B4,  B5,  Eu,
    # B7,  B8,  B9,  B10, B11, B12, Ed, Eb

LAYERS = (
    # 0 BASE
    ('q', 'w', 'f', 'p', 'b',   'j', 'l', 'u', 'y', "'",
     'a', 'r', 's', 't', 'g',   'm', 'n', 'e', 'i', 'o',
     'z', 'x', 'c', 'd', 'v',   'k', 'h', ',', '.', '/',
     '', '', '_esc', ' ', '_tab',   '_entr', '_bksp', '_del', '', '',

     '_left', '_down', '_up', '_rght', (1,''), '_home', '_pgdn', '_pgup', '_end', (1,''),
     ' ', '_tab', '_shft', '_ctrl', '_alt', '_pipe', '_mwup', '_mwdn', '', (2,'')),

    # 1 NUMBERS
    ('[', '7', '8', '9', ']',   '', '', '', '', '',
     ';', '4', '5', '6', '=',   '', '', '', '', '',
     '`', '1', '2', '3', '\\',  '', '', '', '', '',
     '', '', '.', '0', '-',   '_entr', '_bksp', '_del', '', '',

     '_left', '_down', '_up', '_rght', '', '_home', '_pgdn', '_pgup', '_end', '',
     ' ', '_tab', '_shft', '_ctrl', '_alt', '_pipe', '_mwup', '_mwdn', '', ''),

    # 2 SYMBOLS
    ('{', '&', '*', '(', '}',   '', '', '', '', '',
     ':', '$', '%', '^', '+',   '', '', '', '', '',
     '~', '!', '@', '#', '|',  '', '', '', '', '',
     '', '', '(', ')', '_',   '_entr', '_bksp', '_del', '', '',

     '_left', '_down', '_up', '_rght', '', '_home', '_pgdn', '_pgup', '_end', '',
     ' ', '_tab', '_shft', '_ctrl', '_alt', '_pipe', '_mwup', '_mwdn', '', ''),
)
#    ((1, 's'), 't', 'r', (2, 'a'), '(', '_mwup',
#     'o',      'i', 'y', (3, 'e'), ')', '_mwdn', ''),
#
#    # NUMBER
#    ('', '3', '2', '1', '', '',
#     '', '6', '5', '4', '', '', ''),
#
#    # PARENS
#    ('}', '(', ')', '', '', '',
#     '{', '[', ']', '', '', '', ''),
#
#    # SYMBOL
#    ('`', ';', '\\', '!', '', '',
#     '=', '-', '?',  '',  '', '', ''),
#
#    # NAV
#    ('_pgup', '_home', '_up',   '_end',  '_mwup', '_mwup',
#     '_pgdn', '_left', '_down', '_rght', '_mwdn', '_mwdn', ''),
#
#    # MOUSE
#    ('_scup', '_mbt2', '_mup',  '_mbt1', '_mbt3', '_mwup',
#     '_scdn', '_mlft', '_mdwn', '_mrgt', '_mbt1', '_mwdn', '')
#)

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


    ('o', 't', 'r', 'a'):   '_tab',         # Normal        *
    ('_pgdn','_home', 
        '_up', '_end',):    '_tab',         # Directional
    ('_mlft', '_mbt2', 
        '_mup', '_mbt1'): '_tab',           # Mouse

    ('a', 'e'):             '_entr',        # Normal        *
    ('_end', '_rght'):      '_entr',        # Directional
    ('_mbt1', '_mrht'):     '_entr',        # Mouse

    ('s', 'e'):             '_os_ctrl',     # Normal        *
    #('_home', '_rght'):     '_os_ctrl',     # Directional
    ('_mbt2', '_mrgt'):     '_os_ctrl',     # Mouse

    ('s', 'i'):             '_alt',
    ('s', 't', 'r', 'e'):   '_os_shft',

    ('r', 'e'):             '_bksp',        # Normal        *
    ('_up', '_rght'):       '_bksp',        # Directional
    ('_mup', '_mrgt'):      '_bksp',        # Mouse

    ('o', 'r', 'a'):        '_esc',         # Normal        *
    ('_pgdn', '_up', '_end'): '_esc',       # Directional
    ('_mlft', '_mup', '_mbt1'): '_esc',     # Mouse

    ('a', 'r', 'e', 'y'):   '_f11',         # Normal        *
    ('_down', '_rght', '_up', '_end'): '_f11',  # Directional
    ('_mdwn', '_mrgt', '_mup', '_mbt1'): '_f11', # Mouse
    
    ('r', 't', 'y', 'i'):   '_alta', #set('_alt', '_tab'),
    ('t', 's', 'i', 'o'):   '_salta', #set('_shft', '_alt', '_tab'),

    # Nav Layer:
    ('e', 'r', 'i'):            ('_set_base', 4),   
    ('_left', '_up', '_rght'):  ('_set_base', 0),

    # Mouse Layer:
    ('a', 't', 'y'):            ('_set_base', 5),
    ('_mbt1', '_mdwn', '_mbt2'): ('_set_base', 0),
    ('_mup', '_mrgt'):      '_mdur', # Mouse diagonal up right
    ('_mup', '_mlft'):      '_mdul', # Mouse diagonal up left
    ('_mdwn', '_mrgt'):     '_mddr', # Mouse diagonal down right
    ('_mdwn', '_mlft'):     '_mddl', # Mouse diagonal down left
}

# Sort the keys for comparison later
CHORDS = dict([(tuple(sorted(k)), v) for k, v in CHORDS.items()])
