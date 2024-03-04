function_definition = [
    {
        'name': 'debit_card_information',
        'description': 'Beantwortet Fragen zu dem Thema: Sperren von Bankomat-, Debit- und Kreditkarten.',
        'parameters': {
            'type': 'object',
            'properties': {
                'question': {
                    'type': 'string',
                    'description': 'Vollständig ausformulierte Frage zur Sperre von Bankomat-, Debit- und Kreditkarten.'
                }
            },
            "required": ["question"],
        }
    },
    {
        'name': 'banking_information',
        'description': 'Beantwortet Fragen zu dem Thema: Sperren des Online-Bankings.',
        'parameters': {
            'type': 'object',
            'properties': {
                'question': {
                    'type': 'string',
                    'description': 'Vollständig ausformulierte Frage zur Sperre des Online-Bankings.'
                }
            },
            "required": ["question"],
        }
    }
]