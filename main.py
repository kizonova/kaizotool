import socket
import threading
import logging
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard

from cryptography.fernet import Fernet

class MyApp(App):
    def build(self):
        # Create a main layout
        self.layout = BoxLayout(orientation='vertical')

        # Create a label for welcome message
        welcome_label = Label(text="Welcome to Kaizo Tool!\nJoin our Telegram channel at t.me/kaizonova and our YouTube channel at youtube.com/kaizonova")
        self.layout.add_widget(welcome_label)

        # Create a label to display the output
        self.output_label = Label()
        self.layout.add_widget(self.output_label)

        # Create buttons for different options
        self.create_buttons()

        # Create a label to display status while a task is running
        self.status_label = Label(text="", size_hint=(1, None), height=30)
        self.layout.add_widget(self.status_label)

        return self.layout

    def create_buttons(self):
        # Create buttons for different options
        options = [
            ("Find host IP from host name", self.find_host_ip_from_host_name),
            ("Find host from IP address", self.find_host_from_ip_address),
            ("Find reverse hosts in a range", self.reverse_hosts_in_range),
            ("Scan open ports for a specific host", self.scan_open_ports),
            ("Join us (Telegram and YouTube)", self.join_us),
            ("About APK", self.about_apk)
        ]

        for option, function in options:
            button = Button(text=option)
            button.bind(on_press=function)
            self.layout.add_widget(button)

    def display_output(self, text):
        self.output_label.text = text

    def set_status(self, text):
        self.status_label.text = text

    def find_host_ip_from_host_name(self, instance):
        layout = BoxLayout(orientation='vertical')
        popup = Popup(title='Find Host IP from Host Name', content=layout, size_hint=(None, None), size=(400, 200))

        host_name_input = TextInput(hint_text='Enter the host name')
        result_label = Label()

        layout.add_widget(host_name_input)
        layout.add_widget(result_label)

        def find_ip(instance):
            host_name = host_name_input.text.strip()
            self.set_status("Running...")  # Inform the user that the tool is running
            try:
                ip_address = socket.gethostbyname(host_name)
                result_label.text = f'IP address for host {host_name}: {ip_address}'
                self.display_result(f'IP address for host {host_name}: {ip_address}')
                self.ask_save_copy_result(result_label.text)
            except socket.gaierror:
                result_label.text = 'Host not found.'
                self.display_result('Host not found.')
            self.set_status("")  # Clear the status message after the task completes

        find_button = Button(text='Find IP')
        find_button.bind(on_press=find_ip)
        layout.add_widget(find_button)

        popup.open()

    def find_host_from_ip_address(self, instance):
        layout = BoxLayout(orientation='vertical')
        popup = Popup(title='Find Host from IP Address', content=layout, size_hint=(None, None), size=(400, 200))

        ip_address_input = TextInput(hint_text='Enter the IP address')
        result_label = Label()

        layout.add_widget(ip_address_input)
        layout.add_widget(result_label)

        def find_host(instance):
            ip_address = ip_address_input.text.strip()
            self.set_status("Running...")  # Inform the user that the tool is running
            try:
                host_name, _, _ = socket.gethostbyaddr(ip_address)
                result_label.text = f'Host name for IP {ip_address}: {host_name}'
                self.display_result(f'Host name for IP {ip_address}: {host_name}')
                self.ask_save_copy_result(result_label.text)
            except Exception:
                result_label.text = 'Host not found.'
                self.display_result('Host not found.')
            self.set_status("")  # Clear the status message after the task completes

        find_button = Button(text='Find Host')
        find_button.bind(on_press=find_host)
        layout.add_widget(find_button)

        popup.open()

    def reverse_hosts_in_range(self, instance):
        layout = BoxLayout(orientation='vertical')
        popup = Popup(title='Reverse Hosts in a Range', content=layout, size_hint=(None, None), size=(400, 200))

        ip_range_input = TextInput(hint_text='Enter the IP range (e.g., 192.168.1.)')
        result_label = Label()

        layout.add_widget(ip_range_input)
        layout.add_widget(result_label)

        def reverse_hosts(instance):
            ip_range = ip_range_input.text.strip()
            ip_range += '.'
            hostnames = []

            self.set_status("Running...")  # Inform the user that the tool is running

            for i in range(256):
                ip_to_check = ip_range + str(i)
                try:
                    found_hostnames = socket.gethostbyaddr(ip_to_check)
                    hostnames.extend(found_hostnames)
                except Exception:
                    pass

            if hostnames:
                result_label.text = f'Reverse hosts in range {ip_range}:\n' + '\n'.join(hostnames)
                self.display_result(f'Reverse hosts in range {ip_range}:\n' + '\n'.join(hostnames))
                self.ask_save_copy_result(result_label.text)
            else:
                result_label.text = f'No reverse hosts found in range {ip_range}.'
                self.display_result(f'No reverse hosts found in range {ip_range}.')
            self.set_status("")  # Clear the status message after the task completes

        find_button = Button(text='Find Reverse Hosts')
        find_button.bind(on_press=reverse_hosts)
        layout.add_widget(find_button)

        popup.open()

    def scan_open_ports(self, instance):
        layout = BoxLayout(orientation='vertical')
        popup = Popup(title='Scan Open Ports', content=layout, size_hint=(None, None), size=(400, 250))

        host_input = TextInput(hint_text='Enter the hostname or IP address')
        protocol_input = TextInput(hint_text='Enter the protocol (e.g., TCP)')
        progress_bar = ProgressBar(max=65535)
        result_label = Label()

        layout.add_widget(host_input)
        layout.add_widget(protocol_input)
        layout.add_widget(progress_bar)
        layout.add_widget(result_label)

        def scan_ports(instance):
            host = host_input.text.strip()
            protocol = protocol_input.text.strip()
            open_ports = []

            def check_port(port):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    result = sock.connect_ex((host, port))
                    if result == 0:
                        open_ports.append(port)
                    sock.close()
                except:
                    pass

            self.set_status("Running...")  # Inform the user that the tool is running

            def update_progress(dt):
                progress_bar.value += 1
                if progress_bar.value == 65535:
                    Clock.unschedule(update_progress)
                    if open_ports:
                        result_label.text = f'The following {protocol} ports are open on {host}:\n' + ', '.join(map(str, open_ports))
                        self.display_result(f'The following {protocol} ports are open on {host}:\n' + ', '.join(map(str, open_ports)))
                        self.ask_save_copy_result(result_label.text)
                    else:
                        result_label.text = f'No open {protocol} ports found on {host}.'
                        self.display_result(f'No open {protocol} ports found on {host}.')
                    self.set_status("")  # Clear the status message after the task completes

            progress_bar.value = 0
            Clock.schedule_interval(update_progress, 0.001)

            threading.Thread(target=lambda: [check_port(port) for port in range(1, 65536)]).start()

        find_button = Button(text='Scan Ports')
        find_button.bind(on_press=scan_ports)
        layout.add_widget(find_button)

        popup.open()

    def join_us(self, instance):
        self.display_output("Join our Telegram channel at t.me/kaizonova and our YouTube channel at youtube.com/kaizonova")

    def about_apk(self, instance):
        about_text = """
        Kaizo Tool APK
        ------------------------------
        Kaizo Tool is a versatile utility that provides various network-related tools and information.

        Usage:
        1. Find host IP from host name: Enter a host name to find its IP address.
        2. Find host from IP address: Enter an IP address to find its host name.
        3. Find reverse hosts in a range: Enter an IP range to find reverse hosts.
        4. Scan open ports for a specific host: Enter a hostname or IP address and protocol if you want to check specific protocol or just keep it empty to scan all open ports.
       

        About the Developer:
        - Name: kaizo nova
        - Email: t.me/kaizoa

        This APK is for educational and informational purposes only. Use it responsibly and with proper authorization.
        """
        self.display_output(about_text)

    def display_result(self, text):
        self.output_label.text = text

    def ask_save_copy_result(self, result):
        layout = BoxLayout(orientation='vertical')
        popup = Popup(title='Result', content=layout, size_hint=(None, None), size=(400, 250))

        result_label = Label(text=result)
        layout.add_widget(result_label)

        def copy_result(instance):
            Clipboard.copy(result)
            popup.dismiss()

        def save_result(instance):
            file_chooser = FileChooserListView()
            layout.add_widget(file_chooser)

            def save_to_file(file_path):
                try:
                    with open(file_path, 'w') as file:
                        file.write(result)
                    popup.dismiss()
                except Exception as e:
                    result_label.text = f'Error saving result: {str(e)}'

            save_button = Button(text='Save to File')
            save_button.bind(on_press=lambda instance: save_to_file(file_chooser.path))
            layout.add_widget(save_button)

        copy_button = Button(text='Copy to Clipboard')
        copy_button.bind(on_press=copy_result)
        layout.add_widget(copy_button)

        save_button = Button(text='Save to File')
        save_button.bind(on_press=save_result)
        layout.add_widget(save_button)

        popup.open()

if __name__ == "__main__":
    MyApp().run()
