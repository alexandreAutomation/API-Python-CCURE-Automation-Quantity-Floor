# API-CCURE-Automation-Quantity-Floor
Integration of CCURE access control system with automation HVAC of a commercial building

CCURE is an access control system for the building area that manages the entry and exit of registered people, releasing them through turnstiles. Developed this API to make the
HVAC automation of the building having as a parameter the number of employees on a floor, helping to take action on a Fancoil machine or HVAC system, determining the thermal load
of the site and the building

Nesse exemplo temos um arquivo .py que fazer busca dos dados executando um arquivo .sql e fazendo o tratamento do resultado obtido e gerando um arquivo .json. Com esse arquivo um
outro executavel .py serve essas informaçoes usando o modulo APIRestful Flask.
