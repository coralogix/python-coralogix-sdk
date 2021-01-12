build:
	python setup.py bdist_wheel

source:
	python setup.py sdist

publish:
	python setup.py bdist_wheel sdist
	python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

pylint:
	pylint --rcfile=.pylintrc coralogix

clean:
	rm -rf build dist coralogix_logger.egg-info