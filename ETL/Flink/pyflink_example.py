# Import the PyFlink DataStream module
from pyflink.datastream import StreamExecutionEnvironment

# Create a StreamExecutionEnvironment
env = StreamExecutionEnvironment.get_execution_environment()

# Create a data stream from a socket source
ds = env.socket_text_stream(hostname='localhost', port=9999)

# Define a function to filter out the even numbers
def is_odd(n):
    return int(n) % 2 == 1

# Filter the data stream using the function
ds = ds.filter(is_odd)

# Write the data stream to a file sink
ds.write_as_text('output.txt')

# Execute the job
env.execute('DataStream Example')