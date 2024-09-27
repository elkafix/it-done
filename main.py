import flet as ft
import instaloader
import os
import shutil

def get_downloads_folder():
    return os.path.join(os.path.expanduser("~"), "Downloads")

def extract_shortcode(url):
    if "instagram.com" in url and ("/reel/" in url or "/reels/" in url):
        # Remove query parameters by splitting at '?'
        url = url.split("?")[0]  # This will have no effect if '?' is not present
        # Split the URL by '/' and get the shortcode
        shortcode = url.split("/")[-2]  # The shortcode is still the second-to-last element
        return shortcode
    else:
        raise ValueError("Invalid Instagram URL")

def download_reel(shortcode):
    loader = instaloader.Instaloader()
    try:
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, target="temp_reel")

        downloads_folder = get_downloads_folder()

        for filename in os.listdir("temp_reel"):
            if filename.endswith(".mp4"):
                os.rename(os.path.join("temp_reel", filename), os.path.join(downloads_folder, filename))
                return f"Downloaded Reel: {filename} to {downloads_folder}"

        shutil.rmtree("temp_reel")
        return "Download completed."
    except Exception as e:
        return f"Error downloading Reel: {e}"

def main(page: ft.Page):
    page.title = "elkafix InstaProtoType"
    page.window_width = 300
    page.window_height = 600
    page.window_resizable = False  # Make the window unresizable
    page.theme_mode = ft.ThemeMode.DARK  # Set dark mode

    def go_to_second_page(e):
        first_page.visible = False
        second_page.visible = True
        page.update()

    start_button = ft.ElevatedButton(text="Get Started", on_click=go_to_second_page)
    first_page = ft.Column([
        ft.Text("3jbk chi reel ? chargih db ach katsna !", size=28, text_align=ft.TextAlign.CENTER),
        start_button
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def close_dialog(dialog):
        dialog.open = False
        page.update()

    def download_action(e):
        entry_value = entry.value
        try:
            shortcode = extract_shortcode(entry_value)
            message = download_reel(shortcode)
            dialog = ft.AlertDialog(
                title=ft.Text("Reel Tcharga Binajah !!"),
                content=ft.Text(message),
                actions=[ft.TextButton("OK", on_click=lambda e: close_dialog(dialog))]
            )
            page.overlay.append(dialog)
            dialog.open = True
            page.update()
        except ValueError as ve:
            dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text(str(ve)),
                actions=[ft.TextButton("OK", on_click=lambda e: close_dialog(dialog))]
            )
            page.overlay.append(dialog)
            dialog.open = True
            page.update()

    entry = ft.TextField(label="Ktb Lien Hna ...", width=300)
    download_button = ft.ElevatedButton(text="Clicki Hna", on_click=download_action)
    second_page = ft.Column([
        entry,
        download_button
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    page.add(first_page)
    page.add(second_page)
    second_page.visible = False
    page.update()

# Run the app
ft.app(target=main)
