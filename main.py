import argparse
import logging
import subprocess
import sys
from importlib.metadata import distributions
from packaging import version

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.
    """
    parser = argparse.ArgumentParser(description="Identifies potential dependency confusion attacks.")
    parser.add_argument(
        "-p",
        "--package",
        type=str,
        help="The name of the package to check (e.g., 'my_package'). If not provided, checks all installed packages.",
    )
    parser.add_argument(
        "-r",
        "--pypi_url",
        type=str,
        default="https://pypi.org/pypi/",
        help="The base URL of the PyPI repository (default: https://pypi.org/pypi/)."
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output for debugging."
    )

    return parser.parse_args()


def check_package_availability(package_name, pypi_url):
    """
    Checks if a package exists on PyPI and returns the version if it does.

    Args:
        package_name (str): The name of the package to check.
        pypi_url (str): The base URL of the PyPI repository.

    Returns:
        str: The latest version of the package on PyPI, or None if not found.

    Raises:
        subprocess.CalledProcessError: If the `pip` command fails.
        Exception: For other errors during the process.
    """
    try:
        # Use pip to check for the package on PyPI
        command = [
            sys.executable,
            "-m",
            "pip",
            "index",
            "versions",
            package_name,
            "--index-url",
            pypi_url
        ]

        # I ask pip instead of calling the index API myself, so this
        # inherits whatever pip does with proxies and index settings.
        # It also means one subprocess per package, which is why a full
        # installed list check takes as long as it does.
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        version_found = parse_latest_version(result.stdout)
        if version_found is None:
            logging.warning(f"Package '{package_name}' not found on PyPI.")
        return version_found
    except subprocess.CalledProcessError as e:
        logging.error(f"Error checking package '{package_name}' on PyPI: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def parse_latest_version(pip_output):
    # pip index prints the newest release twice, as "name (X.Y)" on the
    # first line and as the first entry of "Available versions:"; it
    # never prints a "Latest version:" line, which is what an earlier
    # version of this parser waited for, so every lookup came back None.
    if not pip_output:
        return None
    lines = pip_output.splitlines()
    if any("Available versions: none" in line for line in lines):
        return None
    first = lines[0].strip()
    if first.endswith(")") and "(" in first:
        return first[first.rindex("(") + 1:-1].strip()
    for line in lines:
        if "Available versions:" in line:
            versions = line.split(":", 1)[1].strip()
            if versions and versions.lower() != "none":
                return versions.split(",")[0].strip()
    return None


def get_installed_packages():
    """
    Gets a list of all installed packages and their versions.

    Returns:
        dict: A dictionary where keys are package names and values are their versions.
    """
    installed_packages = {}
    try:
        # importlib.metadata replaced pkg_resources here: pkg_resources is
        # deprecated and slated for removal, and the setuptools pin in
        # requirements.txt existed only to keep it importable.
        for package in distributions():
            # I lower case the name as the key. Two distributions whose
            # names differ only in case would overwrite each other here,
            # and only the last version read would survive.
            installed_packages[package.metadata["Name"].lower()] = package.version
    except Exception as e:
        logging.error(f"Error getting installed packages: {e}")
        return {}  # Return empty dictionary in case of error

    return installed_packages


def main():
    """
    Main function to execute the dependency confusion check.
    """
    args = setup_argparse()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.package:
        installed_all = get_installed_packages()
        # I keep a named package even when it is not installed, with a
        # None version. The check below then compares only the index
        # side, and a package I never installed can still be reported.
        packages_to_check = {args.package.lower(): installed_all.get(args.package.lower())}
    else:
        packages_to_check = get_installed_packages()

    if not packages_to_check:
        logging.warning("No packages found to check.")
        print("Summary: checked=0 failed=0 not_found=0")
        sys.exit(1)

    vulnerable_packages = []
    not_found_packages = []
    checked_count = 0
    failed_count = 0
    not_found_count = 0

    for package_name, installed_version in packages_to_check.items():
        try:
            pypi_version = check_package_availability(package_name, args.pypi_url)

            checked_count += 1
            if pypi_version is None:
                # Package not found on PyPI - potential internal package
                not_found_count += 1
                not_found_packages.append(package_name)
                logging.info(f"Package '{package_name}' not found on PyPI.")
            else:
                installed_version_obj = version.parse(installed_version) if installed_version else None
                pypi_version_obj = version.parse(pypi_version)

                if installed_version_obj is not None and installed_version_obj > pypi_version_obj:
                    logging.warning(
                        f"Potential Dependency Confusion: Locally installed version '{installed_version}'"
                        f" of '{package_name}' is newer than the PyPI version '{pypi_version}'."
                    )
                    vulnerable_packages.append({
                        "package": package_name,
                        "installed_version": installed_version,
                        "pypi_version": pypi_version
                    })
                else:
                    logging.info(f"Package '{package_name}' is up-to-date or older than PyPI version.")

        except subprocess.CalledProcessError:
            failed_count += 1
            logging.error(f"Failed to check package '{package_name}'. Skipping...")
        except Exception as e:
            failed_count += 1
            logging.error(f"An error occurred while processing '{package_name}': {e}")

    if not_found_packages:
        print("\nPackages not found on the public index:")
        for pkg_name in not_found_packages:
            print(f"  - Package: {pkg_name} (not found on the public index)")

    print(f"Summary: checked={checked_count} failed={failed_count} not_found={not_found_count}")

    if vulnerable_packages:
        print("\nPotential Dependency Confusion Vulnerabilities Found:")
        for vuln in vulnerable_packages:
            print(
                f"  - Package: {vuln['package']}, Installed Version: {vuln['installed_version']},"
                f" PyPI Version: {vuln['pypi_version']}"
            )
        sys.exit(1)  # Exit with error code if vulnerabilities are found
    if failed_count > 0 or checked_count == 0:
        print("Check incomplete: some or all package checks failed.")
        sys.exit(1)
    print("No potential dependency confusion vulnerabilities found.")
    sys.exit(0)


if __name__ == "__main__":
    main()
