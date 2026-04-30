from slowapi import Limiter
from slowapi.util import get_remote_address

# Instância única compartilhada por toda a aplicação
limiter = Limiter(key_func=get_remote_address)
