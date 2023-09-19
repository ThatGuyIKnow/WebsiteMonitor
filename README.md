# Website Monitoring Program

This program is designed to monitor specific websites for changes in their content and send email notifications when changes are detected. It consists of two parts: a graphical user interface (GUI) for configuring the monitoring settings and a background script for continuous monitoring based on the configured settings.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [GUI Configuration](#gui-configuration)
- [Usage](#usage)
- [Auto-Start on Ubuntu](#auto-start-on-ubuntu)
- [Contributing](#contributing)
- [License](#license)

## Features

- Monitor multiple websites simultaneously with different check intervals.
- Configure email notifications for website changes.
- Automatically update the monitoring schedule when the configuration changes.

## Installation

### Prerequisites

Before using this program, make sure you have the following prerequisites installed:

- Python 3
- Python packages: `requests`, `bs4` (Beautiful Soup), `smtplib`, `schedule`
- A Gmail account or another SMTP server for sending email notifications.

You can install the required Python packages using `pip`:

```bash
pip install requests beautifulsoup4 schedule
```

### GUI Configuration

1. Clone or download the repository to your local machine.

2. Run the GUI script to configure the monitoring settings:

   ```bash
   python gui.py
   ```

   This script will open a graphical interface where you can set up SMTP server details, website URLs, element selectors, check intervals, and email settings.

3. Save the configuration by clicking the "Save Configuration" button in the GUI. This will create a `config.json` file in the program's directory with your settings.

## Usage

Once you have configured the monitoring settings using the GUI, you can run the monitoring script in the background to continuously check the websites.

```bash
python main.py
```

The script will run indefinitely and monitor the websites according to the configured check intervals. If changes are detected on any of the websites, it will send email notifications based on the provided email settings.

To stop the monitoring script, you can use `Ctrl+C`.

## Auto-Start on Ubuntu

To make this program run on startup in Ubuntu, you can create a systemd service unit. Here are the steps to do that:

1. Create a systemd service unit file for your program. Open a terminal and run:

   ```bash
   sudo nano /etc/systemd/system/website-monitor.service
   ```

   Replace `website-monitor` with your preferred service name.

2. Add the following content to the service unit file:

   ```ini
   [Unit]
   Description=Website Monitoring Service
   After=network.target

   [Service]
   Type=simple
   ExecStart=/usr/bin/python3 /path/to/monitoring.py
   WorkingDirectory=/path/to/program/directory
   User=your_username

   [Install]
   WantedBy=multi-user.target
   ```

   - `Description`: A brief description of the service.
   - `ExecStart`: The command to start your monitoring script. Replace `/path/to/monitoring.py` with the actual path to your monitoring script.
   - `WorkingDirectory`: The directory where your program is located. Replace `/path/to/program/directory` with the actual path to your program directory.
   - `User`: Your username.

3. Save the file and exit the text editor.

4. Enable the service to run on startup:

   ```bash
   sudo systemctl enable website-monitor.service
   ```

5. Start the service:

   ```bash
   sudo systemctl start website-monitor.service
   ```

6. Check the status of the service to ensure it's running:

   ```bash
   sudo systemctl status website-monitor.service
   ```

   You should see that the service is active and running.

Now, your website monitoring program will automatically start on system boot.

## Contributing

Contributions to this project are welcome! If you have any suggestions, feature requests, or bug reports, please create an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
