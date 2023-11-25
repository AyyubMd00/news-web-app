import sys

sys.path.append('Functions\\utils')
from db_utils import delete_stories

query = {'title': ""}
delete_stories(query)