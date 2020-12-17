python -m venv env
call env\Scripts\activate
pip install -r requirements.txt

set "_OLD_PYTHONPATH=%PYTHONPATH%"
set "PYTHONPATH=%_OLD_PYTHONPATH%;%VIRTUAL_ENV%\.."

python src\reporting.py

if defined _OLD_PYTHONPATH (
    set "PYTHONPATH=%_OLD_PYTHONPATH%"
)
set _OLD_PYTHONPATH=

deactivate
