conf = {
    "tokens": {
        "1.1.1.1": "123",
    },
    "scan_strategy": {
        "60": 1800,
        "300": 1800,
        "900": 3600
    },
    "recover_strategy": {
        "60": 180,
        "300": 600,
        "900": 900
    }
}

enviroment = {
    'prod': {
        'mysql': {
            'host': "127.0.0.1",
            'user': "root",
            'passwd': "xxxxxx"",
            'port': 3306,
            'db': "iplive"
        },
        'level': "debug",
        'debug': False
    },
    'test': {
        'mysql': {
            'host': "127.0.0.1",
            'user': "root",
            'passwd': "xxxxxx",
            'port': 3306,
            'db': "iplive"
        },
        'level': "debug",
        'debug': True
    },
    'dev': {
        'mysql': {
            'host': "127.0.0.1",
            'user': "root",
            'passwd': "xxxxxx",
            'port': 3306,
            'db': "iplive"
        },
        'level': "info",
        'debug': True
    }
}

level_strategy = {
    '0': {
        'node_ips': "",
        'total': 3,
        'as_down': 2
    },
    '1': {
        'node_ips': "",
        'total': 2,
        'as_down': 1
    },
    '2': {
        'node_ips': "",
        'total': 7,
        'as_down': 5
    }
}


port_mapping = {
    'http': 80,
    'https': 443,
    'tcp': 80,
    'udp': 80
}
