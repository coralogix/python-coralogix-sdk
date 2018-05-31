build:
	python setup.py bdist_wheel

source:
	python setup.py sdist

publish:
	python setup.py bdist_wheel sdist upload --sign

pylint:
	pylint --rcfile=.pylintrc coralogix