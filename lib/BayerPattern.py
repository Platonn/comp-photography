class BayerPattern:
	COLOR = [
		['r', 'g'],
		['g', 'b']
	]

	FILTERS = {
		'r': [
			['cent', 'hori'],
			['vert', 'diag']
		],

		'g': [
			['hove', 'cent'],
			['cent', 'hove']
		],

		'b': [
			['diag', 'vert'],
			['hori', 'cent']
		]
	}

	FILTER_SCHEMA = {
		# central
		"cent": [
			[0.00, 0.00, 0.00],
			[0.00, 1.00, 0.00],
			[0.00, 0.00, 0.00],
		],

		# horizontal
		"hori": [
			[0.00, 0.00, 0.00],
			[0.50, 0.00, 0.50],
			[0.00, 0.00, 0.00],
		],

		# vertical
		"vert": [
			[0.00, 0.50, 0.00],
			[0.00, 0.00, 0.00],
			[0.00, 0.50, 0.00],
		],

		# diagonal
		"diag": [
			[0.25, 0.00, 0.25],
			[0.00, 0.00, 0.00],
			[0.25, 0.00, 0.25],
		],

		# horizontal-vertical
		"hove": [
			[0.00, 0.25, 0.25],
			[0.25, 0.00, 0.25],
			[0.00, 0.25, 0.00],
		]
	}
