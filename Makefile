RPMBUILD = rpmbuild --define "_topdir %(pwd)/build" \
        --define "_builddir %{_topdir}" \
        --define "_rpmdir %{_topdir}" \
        --define "_srcrpmdir %{_topdir}" \
        --define "_sourcedir %(pwd)"

all:
	mkdir -p build
	date --utc +%Y%m%d%H%M%S > VERSION
	${RPMBUILD} --define "_version %(cat VERSION)" -ba rockit-dome-ash.spec
	${RPMBUILD} --define "_version %(cat VERSION)" -ba python3-rockit-dome-ash.spec

	mv build/noarch/*.rpm .
	rm -rf build VERSION

install:
	@date --utc +%Y%m%d%H%M%S > VERSION
	@python3 -m build --outdir .
	@sudo pip3 install rockit.dome.ash-$$(cat VERSION)-py3-none-any.whl
	@rm VERSION
	@cp ash_domed dome /bin/
	@cp ash_domed@.service /usr/lib/systemd/system/
	@cp completion/dome /etc/bash_completion.d/
	@cp completion/dome /etc/bash_completion.d/
	@install -d /etc/domed
	@echo ""
	@echo "Installed server, client, and service files."
	@echo "Now copy the relevant json config files to /etc/domed/"
