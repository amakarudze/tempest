# tempest
A network monitoring tool for a small WiFi network. Helps you detect which devices are running on your network.

## Installation
1. Clone this repo.
2. Navigate to the tempest folder and create a virtual environment
3. Activate the virtual environment and install pip-tools by running `pip install pip-tools`.
4. Run `pip-sync` in your virtual environment to install required packages.
6. Create a superuser for your project using `python3 manage.py createsuperuser`.
7. Run `python3 manage.py runserver` and navigate to `http://127.0.0.1:8000`.

## Usage
1. In another command line window, activate your virtual environment and run `python3 manage.py scan_network <network_range>`. Replace `<network_range>` with the network which you want to scan.
2. Wait for the scan to complete.
3. Refresh the browser page for the `127.0.0.1:8000` to see the
