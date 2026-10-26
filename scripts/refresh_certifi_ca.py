"""Pin a patched CA bundle for the legacy Docker image (GHSA-6q48-6c7w-9gw2).

Python in the upstream image may be too old to install current certifi. We
fetch its pure-data wheel, verify the SHA256 before reading it, and patch the
bundles used by both pip and requests without changing Python itself.
"""

import hashlib
import os
import shutil
import urllib.request
import zipfile
from io import BytesIO


WHEEL_URL = (
    "https://files.pythonhosted.org/packages/c4/51/"
    "29046e48f693c54e5b7412216d447a1d8362c9653148d98c02cdf65fa733/"
    "certifi-2026.10.19-py3-none-any.whl"
)
WHEEL_SHA256 = "42d35340cc5b9ba78e818ddbff0c5b1c2b779de448a340fd1b989f5fa8670e1b"
BUNDLE = "/usr/local/share/pdf2htmlex/certifi-2026.10.19.pem"


def ensure_patched_bundle():
    if os.path.isfile(BUNDLE):
        return

    with urllib.request.urlopen(WHEEL_URL, timeout=60) as response:
        wheel = response.read()
    if hashlib.sha256(wheel).hexdigest() != WHEEL_SHA256:
        raise ValueError("certifi wheel SHA256 mismatch")

    with zipfile.ZipFile(BytesIO(wheel)) as archive:
        pem = archive.read("certifi/cacert.pem")
    os.makedirs(os.path.dirname(BUNDLE), exist_ok=True)
    with open(BUNDLE, "wb") as output:
        output.write(pem)
    os.chmod(BUNDLE, 0o644)


def patch_package_bundle(module_name):
    try:
        module = __import__(module_name, fromlist=["where"])
    except ImportError:
        return
    destination = module.where()
    if os.path.realpath(destination) != os.path.realpath(BUNDLE):
        shutil.copyfile(BUNDLE, destination)


if __name__ == "__main__":
    ensure_patched_bundle()
    patch_package_bundle("pip._vendor.certifi")
    patch_package_bundle("certifi")
