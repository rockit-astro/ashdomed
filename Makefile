install:
	@python3 setup.py install
	@cp ashdomed dome /usr/bin/
	@cp ashdomed@.service /etc/systemd/system/
	@cp completion/dome /etc/bash_completion.d/
	@install -d /etc/domed
	@cp warwick.json /etc/domed/
	@echo ""
	@echo "Installation complete."
