flowchart LR
    config --> parser
    models --> parser
    parser --> analyzer
    analyzer --> server
