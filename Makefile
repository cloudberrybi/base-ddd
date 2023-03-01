.ONESHELL:

run-tests:
	@ pytest --cov-report term-missing --cov=cbi_ddd

pypi:
	@ rm -rf ./build
	@ rm -rf ./dist
	@ rm -rf ./*.egg-info
	@ python3 setup.py bdist_wheel
	@ python3 -m twine upload --config-file .pypirc --repository pypi dist/* 