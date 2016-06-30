import uuid
from uuid import uuid5
from uuid import uuid4
print(uuid5(uuid.NAMESPACE_DNS, 'testme'))
print(uuid4())