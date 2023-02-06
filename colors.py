from colour import Color
from operator import itemgetter

# Options
filepath = 'static/css/colors.css'

cycles = [
	{
		"start_color": '#e2f4f7',
		"end_color": '#01a7c5',
		"range_start": 0,
		"range_end": 41,
		"range_continue_to": 101,
		"increment": 1,
		"class_name": 'sims-pct',
		"attr_name": 'data-pct'
	},
	{
		"start_color": '#f6e5dd',
		"end_color": '#f55205',
		"range_start": 0,
		"range_end": 101,
		"range_continue_to": 101,
		"increment": 1,
		"class_name": 'places-bye-pct',
		"attr_name": 'data-places-bye-pct'
	}
]


def makeColors(cycles):

	# Open CSS file
	f = open(filepath, "w")

	for cycle in cycles:

		# Destructure the options
		start_color, end_color, range_start, range_end, range_continue_to, increment, class_name, attr_name = itemgetter(
			'start_color', 'end_color', 'range_start', 'range_end', 'range_continue_to', 'increment', 'class_name', 'attr_name'
		)(cycle)
	
		num_colors = int((range_end - range_start) * (1 / increment))
		colors = list(Color(start_color).range_to(Color(end_color), num_colors))
		n = range_start

		for color in colors:
			f.write('.' + class_name + '[' + attr_name + '^="' + str(n) +'"]{background:' + str(color) + ';}')
			n += increment

			if isinstance(n, float):
				if n.is_integer():
					n = int(n)

		# Continue on with same color if needed
		for n in range(range_end, range_continue_to):
			f.write('.' + class_name + '[' + attr_name + '^="' + str(n) +'"]{background:' + str(color) + ';}')

	# Close CSS file, print success message
	f.close()
	print("CSS file created at static/css/colors.css")


# Run Program
makeColors(cycles)



