recipe_fga = dict(

    model_type = 'fga',

    variable_type = ['states', 'controls', 'auxiliary'],

    equation_type = dict(

        arbitrage = [
            ('states',0),
            ('controls',0),
            ('auxiliary',0),
            ('states',1),
            ('controls',1),
            ('auxiliary',1)
        ],

        transition = {
            'definition': True,
            'lhs': [
                ('states',0),
                ],
            'rhs': [
                ('states',-1),
                ('controls',-1),
                ('auxiliary',-1),
                ('shocks',0)
            ]
        },

        auxiliary = {

            'definition': True,

            'lhs': [
                ('auxiliary',0),
                ],

            'rhs': [
                ('states',0),
                ('controls',0)
            ]
        }

    )
)

recipe_fgh = dict(

    model_type = 'fgh',

    variable_type = ['states', 'controls', 'expectations'],

    equation_type = dict(

        arbitrage = [
            ('states',0),
            ('controls',0),
            ('expectations',0),
        ],

        transition = {
            'definition': True,
            'lhs': [
                ('states',0),
                ],
            'rhs': [
                ('states',-1),
                ('controls',-1),
                ('shocks',0)
            ]
        },

        expectation = {

            'definition': True,

            'lhs': [
                ('expectations',0),
                ],

            'rhs': [
                ('states',1),
                ('controls',1)
            ]
        }

    )
)


recipes = {
    'fga': recipe_fga,
    'fgh': recipe_fgh,
}