# # 1.Write a script that connects to 100 hosts, looks for a particular process and sends an email with a report.
# # 1.Write a script that connects to 100 hosts, looks for a particular process and sends an email with a report.


# import paramiko
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
#
#
# hosts = ["192.168.xxx.xxx","192.168.xxx.xxx"]
# username = "dev"
# password = "**********"
# process_to_check = "sshd"
#
#
# def check_process_on_host(host):
#     try:
#         client = paramiko.SSHClient()
#         client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         client.connect(host,username=username,password=password)
#         vmstat = "vmstat 1 3"
#         get_process = f"pgrep {process_to_check}"
#         read_file_on_host = "cat /home/dev/example"
#         check_file_permission = "ls -lhart /home/dev/example"
#         # next i want to check status of a service lets say systemctl status sshd
#         stdin,stdout,stderr = client.exec_command(read_file_on_host)
#         process_ids = stdout.read().decode().strip()
#
#         client.close()
#         return process_ids if process_ids else None
#     except Exception as e:
#         return f"Error connecting to {host}: {e}"
#
#
# def send_email(report):
#     """Send an email with the process report."""
#     msg = MIMEMultipart()
#     msg['From'] = email_sender
#     msg['To'] = email_receiver
#     msg['Subject'] = "Process Check Report"
#
#     body = f"Process Check Report:\n\n{report}"
#     msg.attach(MIMEText(body, 'plain'))
#
#     with smtplib.SMTP(smtp_server, smtp_port) as server:
#         server.starttls()
#         server.login(email_sender, smtp_password)
#         server.send_message(msg)
#
#
# def main():
#     report = []
#     for host in hosts:
#         res = check_process_on_host(host)
#         report.append(f"{host}: {res}\n")  # Collect results in report
#
#     # Write the report to a file
#     with open("process_report.txt", "w") as report_file:
#         report_file.writelines(report)
#
# if __name__ == "__main__":
#     main()
#

import paramiko
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
hosts = ["192.168.1.1", "192.168.1.2"]  # Add up to 100 hosts
username = "dev"
password = "**********"
process_to_check = "sshd"

# Email setup
email_sender = "your_email@example.com"
email_receiver = "receiver@example.com"
smtp_server = "smtp.example.com"
smtp_port = 587
smtp_password = "your_email_password"

def check_process_on_host(host):
    """Check process, resource usage, and service status on a host."""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)

        # Check if process is running
        get_process = f"pgrep {process_to_check}"
        stdin, stdout, stderr = client.exec_command(get_process)
        process_ids = stdout.read().decode().strip()

        # Check memory and CPU usage
        resource_usage_cmd = "vmstat --unit M | awk 'NR==3 {print $4,$5,$13,$14}'"  # Memory, swap, CPU user, CPU system
        stdin, stdout, stderr = client.exec_command(resource_usage_cmd)
        mem_free, swap_free, cpu_user, cpu_sys = map(int, stdout.read().decode().split())

        # Check disk usage
        disk_usage_cmd = "df -h / | awk 'NR==2 {print $5}'"  # Assuming root directory check
        stdin, stdout, stderr = client.exec_command(disk_usage_cmd)
        disk_usage = int(stdout.read().decode().strip().strip('%'))

        # Check service status
        service_status_cmd = f"systemctl is-active {process_to_check}"
        stdin, stdout, stderr = client.exec_command(service_status_cmd)
        service_status = stdout.read().decode().strip()

        client.close()

        # Report formatting
        report = f"Host: {host}\n"
        report += f"Process '{process_to_check}' running: {'Yes' if process_ids else 'No'}\n"
        report += f"Memory Free: {mem_free} MB, Swap Free: {swap_free} MB\n"
        report += f"CPU Usage (User/System): {cpu_user}% / {cpu_sys}%\n"
        report += f"Disk Usage: {disk_usage}%\n"
        report += f"Service '{process_to_check}' status: {service_status}\n"

        # Check threshold
        if mem_free < 500 or cpu_user + cpu_sys > 60 or disk_usage > 60:
            report += "⚠️ Resource usage warning!\n"

        report += "-" * 40 + "\n"
        return report
    except Exception as e:
        return f"Error connecting to {host}: {e}\n"


def send_email(report):
    """Send an email with the process and resource usage report."""
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = "Process and Resource Usage Report"

    body = f"Process and Resource Usage Report:\n\n{report}"
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_sender, smtp_password)
        server.send_message(msg)


def main():
    report = []
    for host in hosts:
        res = check_process_on_host(host)
        report.append(res)  # Collect results in report

    # Write the report to a file
    with open("process_report.txt", "w") as report_file:
        report_file.writelines(report)

    # Send the email with the report
    send_email("".join(report))


if __name__ == "__main__":
    main()

















import paramiko



def commandonhost(host):
    paramiko.SSHClient()
