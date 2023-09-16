import socket
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.utils import get_color_from_hex

from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager

class KaizoToolApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"  # Set the dark theme

        self.layout = BoxLayout(orientation='vertical', spacing=10)
        self.layout.background_color = get_color_from_hex("#121212")  # Dark mode background color

        welcome_label = MDLabel(
            text="Welcome to Kaizo Tool!\nJoin our Telegram channel at t.me/kaizonova and our YouTube channel at youtube.com/kaizonova",
            halign='center',
            theme_text_color="Secondary"
        )
        self.layout.add_widget(welcome_label)

        self.output_label = MDLabel(
            theme_text_color="Primary"
        )
        self.layout.add_widget(self.output_label)

        self.create_buttons()

        self.status_label = MDLabel(
            text="",
            size_hint_y=None,
            height=30,
            theme_text_color="Secondary"
        )
        self.layout.add_widget(self.status_label)

        return self.layout

    def create_buttons(self):
        options = [
            ("Find host IP from host name", self.find_host_ip_from_host_name),
            ("Find host from IP address", self.find_host_from_ip_address),
            ("Find reverse hosts in a range", self.reverse_hosts_in_range),
            ("Scan open ports for a specific host", self.scan_open_ports),
            ("Join us (Telegram and YouTube)", self.join_us),
            ("About APK", self.about_apk)
        ]

        for option, function in options:
            button = MDRaisedButton(
                text=option,
                theme_text_color="Secondary",
            )
            button.bind(on_release=function)  # Use on_release for KivyMD buttons
            self.layout.add_widget(button)

    def display_output(self, text):
        self.output_label.text = text

    def set_status(self, text):
        self.status_label.text = text

    def find_host_ip_from_host_name(self, instance):
        layout = BoxLayout(orientation='vertical')
        popup = MDDialog(
            title='Find Host IP from Host Name',
            content=layout,
            size_hint=(None, None),
            size=(400, 200),
            background_color=get_color_from_hex("#212121")  # Dark mode dialog background color
        )

        host_name_input = MDTextField(
            hint_text='Enter the host name',
            mode="fill",
        )
        result_label = MDLabel(
            theme_text_color="Primary"
        )

        layout.add_widget(host_name_input)
        layout.add_widget(result_label)

        def find_ip(instance):
            host_name = host_name_input.text.strip()
            self.set_status("Running...")  # Inform the user that the tool is running
            try:
                ip_address = socket.gethostbyname(host_name)
                result_label.text = f'IP address for host {host_name}: {ip_address}'
                self.display_output(f'IP address for host {host_name}: {ip_address}')
                self.ask_save_copy_result(result_label.text)
            except socket.gaierror:
                result_label.text = 'Host not found.'
                self.display_output('Host not found.')
            self.set_status("")  # Clear the status message after the task completes

        find_button = MDRaisedButton(
            text='Find IP',
            theme_text_color="Secondary",
        )
        find_button.bind(on_release=find_ip)  # Use on_release for KivyMD buttons
        layout.add_widget(find_button)

        popup.open()

    def find_host_from_ip_address(self, instance):
        layout = BoxLayout(orientation='vertical')
        popup = MDDialog(
            title='Find Host from IP Address',
            content=layout,
            size_hint=(None, None),
            size=(400, 200),
            background_color=get_color_from_hex("#212121")  # Dark mode dialog background color
        )

        ip_address_input = MDTextField(
            hint_text='Enter the IP address',
            mode="fill",
        )
        result_label = MDLabel(
            theme_text_color="Primary"
        )

        layout.add_widget(ip_address_input)
        layout.add_widget(result_label)

        def find_host(instance):
            ip_address = ip_address_input.text.strip()
            self.set_status("Running...")  # Inform the user that the tool is running
            try:
                host_name, _, _ = socket.gethostbyaddr(ip_address)
                result_label.text = f'Host name for IP {ip_address}: {host_name}'
                self.display_output(f'Host name for IP {ip_address}: {host_name}')
                self.ask_save_copy_result(result_label.text)
            except Exception:
                result_label.text = 'Host not found.'
                self.display_output('Host not found.')
            self.set_status("")  # Clear the status message after the task completes

        find_button = MDRaisedButton(
            text='Find Host',
            theme_text_color="Secondary",
        )
        find_button.bind(on_release=find_host)  # Use on_release for KivyMD buttons
        layout.add_widget(find_button)

        popup.open()

    def reverse_hosts_in_range(self, instance):
        layout = BoxLayout(orientation='vertical')
        popup = MDDialog(
            title='Reverse Hosts in a Range',
            content=layout,
            size_hint=(None, None),
            size=(400, 200),
            background_color=get_color_from_hex("#212121")  # Dark mode dialog background color
        )

        ip_range_input = MDTextField(
            hint_text='Enter the IP range (e.g., 192.168.1.)',
            mode="fill",
        )
        result_label = MDLabel(
            theme_text_color="Primary"
        )

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
                self.display_output(f'Reverse hosts in range {ip_range}:\n' + '\n'.join(hostnames))
                self.ask_save_copy_result(result_label.text)
            else:
                result_label.text = f'No reverse hosts found in range {ip_range}.'
                self.display_output(f'No reverse hosts found in range {ip_range}.')
            self.set_status("")  # Clear the status message after the task completes

        find_button = MDRaisedButton(
            text='Find Reverse Hosts',
            theme_text_color="Secondary",
        )
        find_button.bind(on_release=reverse_hosts)  # Use on_release for KivyMD buttons
        layout.add_widget(find_button)

        popup.open()

    def scan_open_ports(self, instance):
        layout = BoxLayout(orientation='vertical')
        popup = MDDialog(
            title='Scan Open Ports',
            content=layout,
            size_hint=(None, None),
            size=(400, 250),
            background_color=get_color_from_hex("#212121")  # Dark mode dialog background color
        )

        host_input = MDTextField(
            hint_text='Enter the hostname or IP address',
            mode="fill",
        )
        protocol_input = MDTextField(
            hint_text='Enter the protocol (e.g., TCP)',
            mode="fill",
        )
        progress_bar = ProgressBar(
            max=65535,
            size_hint=(1, None),
            height=20
        )
        result_label = MDLabel(
            theme_text_color="Primary"
        )

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
                        result_label.text = f'The following {protocol} ports are open on {host}:\n' + ', '.join(
                            map(str, open_ports))
                        self.display_output(
                            f'The following {protocol} ports are open on {host}:\n' + ', '.join(map(str, open_ports)))
                        self.ask_save_copy_result(result_label.text)
                    else:
                        result_label.text = f'No open {protocol} ports found on {host}.'
                        self.display_output(f'No open {protocol} ports found on {host}.')
                    self.set_status("")  # Clear the status message after the task completes

            progress_bar.value = 0
            Clock.schedule_interval(update_progress, 0.001)

            threading.Thread(target=lambda: [check_port(port) for port in range(1, 65536)]).start()

        find_button = MDRaisedButton(
            text='Scan Ports',
            theme_text_color="Secondary",
        )
        find_button.bind(on_release=scan_ports)  # Use on_release for KivyMD buttons
        layout.add_widget(find_button)

        popup.open()

    def join_us(self, instance):
        self.display_output(
            "Join our Telegram channel at t.me/kaizonova and our YouTube channel at youtube.com/kaizonova")

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

    def display_output(self, text):
        self.output_label.text = text

    def ask_save_copy_result(self, result):
        layout = BoxLayout(orientation='vertical')
        popup = MDDialog(
            title='Result',
            content=layout,
            size_hint=(None, None),
            size=(400, 250),
            background_color=get_color_from_hex("#212121")  # Dark mode dialog background color
        )

        result_label = MDLabel(
            text=result,
            theme_text_color="Primary"
        )
        layout.add_widget(result_label)

        def copy_result(instance):
            Clipboard.copy(result)
            popup.dismiss()

        def save_result(instance):
            file_manager = MDFileManager(
                exit_manager=self.exit_manager,
                select_path=self.select_path,
            )
            file_manager.show('/')  # Show the file manager to select a save location

        def exit_manager(self, *args):
            pass

        def select_path(self, path):
            result_label.text = f'Saving result to: {path}'
            try:
                with open(path, 'w') as file:
                    file.write(result)
                popup.dismiss()
            except Exception as e:
                result_label.text = f'Error saving result: {str(e)}'

        copy_button = MDRaisedButton(
            text='Copy to Clipboard',
            theme_text_color="Secondary",
        )
        copy_button.bind(on_release=copy_result)  # Use on_release for KivyMD buttons
        layout.add_widget(copy_button)

        save_button = MDRaisedButton(
            text='Save to File',
            theme_text_color="Secondary",
        )
        save_button.bind(on_release=save_result)  # Use on_release for KivyMD buttons
        layout.add_widget(save_button)

        popup.open()

if __name__ == "__main__":
    KaizoToolApp().run()
