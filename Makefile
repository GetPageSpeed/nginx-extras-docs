.PHONY: all
all:
	git pull
	./venv/bin/python ./generate.py

.PHONY: setup
setup:
	/opt/rh/rh-python38/root/bin/python3 -m venv ./venv
	./venv/bin/pip install -r requirements.txt
	./venv/bin/pip install -r docs/requirements.txt


.PHONY: clean
clean:
	find docs/modules -type f -exec rm -f {} +
	rm -rf docs/modules_list.md docs/lua_list.md

.PHONY: update
update:all
	git add --all .
	git commit -m "up"
	git push
	./venv/bin/mkdocs gh-deploy
