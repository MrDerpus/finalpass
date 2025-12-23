'''
Author: MrDerpus
Python version: 3.12.3

TOME Parser v1.4.0
Table Oriented Markup Encoding
'''
class TOME:
	@staticmethod
	def read(input:str, from_string:bool=False, delimiter:str=',') -> dict:

		# Present error message to terminal. (used inside strict_cast) ----
		def strict_type_error(expected:str, value:str, column:str, file:str, line:int) -> None:
			raise ValueError(
				f'\n\nTOMEparseError @ line {line} in {file}:\n'
				f'{column} expected data type: {expected}, but \'{value}\' was given instead.\n'
			)
		
		# Cast data types for columns defined in table header.
		def strict_cast(value:str, type_name:str, column:str, file:str, line_number:int): # returns str, int, float or bool

			type_map:dict = { # Data type mapping.
				'str': str,
				'int': int,
				'float': float,
				'bool': bool
			}

			# class empty values as empty.
			if value == '' and type_name != 'str':
				strict_type_error(type_name, '(empty)', column, file, line_number)

			# Return bool.
			if type_name == 'bool':
				v = value.lower()
				if v in ['true', 'yes', '1']: return True
				else: return False
				strict_type_error('bool', value, column, file, line_number)

			# int, float or str.
			try:
				return type_map[type_name](value)
			except:
				strict_type_error(type_name, value, column, file, line_number)
		# -----------------------------------------------------------------

		# TOME Parser logic, used to parse TOME data into Python dictionary.
		def PARSER_LOGIC(input_list:list):
			table:dict     = {}   # Table dictionary that is output.
			row_index:int  = -1   # Tracks actual data rows (index starts at 0).
			line_number:int = 0   # Keeps track of current line number.
			table_name:str = ''   # Name of current table.
			values:list    = []   # Store values to be added to dictionary.
			data_type:list = []   # Get datatype for table item.
			columns:list   = []   # Store column names for tables.
			table_type:str = ''   # Set to 'dynamic' by default.
			_type:str      = ''   # Holds current set data type for row item in header. (Only used in table_type = strict)
			_value:str     = ''   # Holds variable name. (Only used in table_type = strict)
			string_list:list = [] # Holds string import, from either string or from file.

			syntax:dict = {
				'brackets':  '[]',       # Characters used to detect the header section.
				'comments':  ['#', ';'], # Comments, lines to ignore
				'var-type':  ':',        # Separate values from their data types.
				'end-parse': '!',        # Stop parsing file.
				'separator':  delimiter  # The comma delimiter.
			}

			
			# Read file line by line, removing the white space from the beginning & end of the line.
			for line in input_list:
				line_number += 1
				line = line.strip()

				if line == '': row_index = -1; continue # Skip empty line, and reset row_index.
				elif line[0] in syntax['comments']: continue # Skip commented lines.
				elif line[:2].strip() == syntax['end-parse']: return table   # End file parsing early, return current parsed data.
				
				row_index += 1

				# Define table and column names.
				if row_index == 0:
					table_type = 'dynamic'


					if syntax['brackets'][0] not in line or syntax['brackets'][1] not in line:
						raise ValueError(
							f'\n\nTOMEparseError @ line {line_number} in {input}:\n'
							f'Malformed table header.\n'
						)

					table_name = line.split(syntax['brackets'][0])[0].strip() # Collect table name.
					columns    = line.split(syntax['brackets'][0])[1].split(syntax['brackets'][1])[0].split(syntax['separator']) # I dont suffer from Long-line-itis, I genuinely enjoy it.
					data_type  = []

					# create table name, and cleanse items for columns list.
					table[table_name] = []
					
					
					# if table is strongly typed, cast data types in a list to be accessed later in code.
					for i in range(len(columns)):
						if syntax['var-type'] in columns[i]:
							table_type = 'strict'
							_type  = columns[i].split(syntax['var-type'])[1].strip().lower()
							_value = columns[i].split(syntax['var-type'])[0].strip()
							
							# if type is in accepted list, append type to data_type:list.
							if _type in ['str', 'string', 'int', 'integer', 'float', 'boolean', 'bool']:
								if   _type == 'string':  _type = 'str'
								elif _type == 'boolean': _type = 'bool'
								elif _type == 'integer': _type = 'int'
								
								data_type.append(_type)
								columns[i] = _value
							
							else:
								raise ValueError(
									f'\n\nTOMEparseError @ line {line_number} in {input}, in Table [\'{table_name}\']:\n'
									f'Invalid data type \'{_type}\', expected only: \n'
									'[String/str, Integer/int, float, Boolean/bool].\n'
								)
						
						# Set type string if data type is not supported.
						else:
							data_type.append('str')
							columns[i] = columns[i].strip()


				# Collect values line and place them into dictionary.
				elif row_index > 0:
					index = row_index-1
					values = [ j.strip() for j in line.split(syntax['separator']) ]

					if len(values) != len(columns):
						raise ValueError(
							f'\n\nTOMEparseError @ line {line_number} in {input}:\n'
							f'Table: [\'{table_name}\'] has {len(columns)} columns defined in header but has {len(values)} values.\n'
						)

					# Cast variables as their defined data types, and append to dictionary.
					if table_type == 'strict':
						for i in range(len(values)):

							values[i] = strict_cast(
								values[i],
								data_type[i],
								columns[i],
								input,
								line_number
							)

					# Append to table dictionary.
					table[table_name].append({ columns[j]: values[j] for j in range(len(values)) })
			
			# Return.
			return table
		# -----------------------------------------------------------------


		
		# User defined parsing method:

		# If user chooses to read from a file, grab lines from the file and place them
		# into a list to be parsed by the TOME parser.
		if from_string == False:
			with open(input, 'r') as file:
				string_list = file.readlines()
		
		# Otherwise, treat the input as plaintext, and parse the string data with the
		# TOME Parser. 
		else:
			string_list = input.splitlines()

		# Return parsed data.
		parsed_data = PARSER_LOGIC(string_list)
		return parsed_data



	@staticmethod
	def write(output:str='', to_string:bool=False, table:dict={}, mode:str='a', delimiter:str=',') -> None | str:

		type_map:dict = { # Data type mapping.
			str: 'str',
			int: 'int',
			float: 'float',
			bool: 'bool'
		}
		typed_columns:list = [] # Holds column names with their given data type.
		columns:list       = [] # Holds Columns names grabbed from first row of dictionary.
		values:list        = [] # Holds the row data.
		lines:list         = [] # Holds output file data before writing to file.
		types:list         = [] # Holds given data types for each column based on the row of a table. 



		# Return TOME type string based on Python type.
		def infer_type(value):
			return type_map.get(type(value), 'str')
			# str is the default data type returned using TOME.write(), unless assigned in .tome file.

		# Convert Python values into TOME compatible strings / data types.
		def format_value(value) -> str:
			if isinstance(value, bool):
				return str(value).upper()
			return str(value)

		for table_name, rows in table.items():

			# Skip blank lines.
			if not rows: continue

			# Extract column order from the first row.
			columns = list(rows[0].keys())

			# Assign data types from the first row.
			types = [ infer_type(rows[0][column]) for column in columns ]

			# Build typed header: column:type
			typed_columns = [ f'{column}:{types[i]}' for i, column in enumerate(columns) ]

			# Append header line to output.
			lines.append( f'\n\n{table_name}[{delimiter.join(typed_columns)}]:' )

			# Append rows to output.
			for row in rows:
				values = [ format_value(row[column]) for column in columns ]
				lines.append('\t' + delimiter.join(values))

			# Add blank line between tables to avoid dict / table reading conflicts.
			lines.append('')

		output_str = '\n'.join(lines)

		if to_string == False:
			# Write to output file.
			with open(output, mode) as f:
				f.write(output_str)
			return None

		else:
			return output_str



if __name__ == '__main__':
	print('This is a library module.')