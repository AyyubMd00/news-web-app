# Import the PyFlink DataStream module
from pyflink.datastream import StreamExecutionEnvironment

# Create a StreamExecutionEnvironment
env = StreamExecutionEnvironment.get_execution_environment()

# Create a data stream from a hardcoded list of numbers
ds = env.from_collection([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Define a function to filter out the even numbers
def is_odd(n):
    return n % 2 == 1

# Filter the data stream using the function
ds = ds.filter(is_odd)

# Print the data stream to the console
ds.print()

# Execute the job
env.execute('DataStream Example')
