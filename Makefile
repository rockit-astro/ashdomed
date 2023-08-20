install:
	@date --utc +%Y%m%d%H%M%S > VERSION
	@python3 -m build --outdir .
	@sudo pip3 install rockit.ashdome-$$(cat VERSION)-py3-none-any.whl
	@rm VERSION
	@cp ashdomed dome /usr/bin/
	@cp ashdomed@.service /etc/systemd/system/
	@cp completion/dome /etc/bash_completion.d/
	@install -d /etc/domed
	@cp warwick.json /etc/domed/
	@echo ""
	@echo "Installation complete."
