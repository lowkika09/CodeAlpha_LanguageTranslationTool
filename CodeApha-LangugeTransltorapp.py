import tkinter as tk
from tkinter import ttk, messagebox
import requests


# -----------------------------
# Languages
# -----------------------------
LANGUAGES = {
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "French": "fr",
    "German": "de",
    "Spanish": "es"
}


# -----------------------------
# Translation Function
# -----------------------------
def translate_text():

    text = input_text.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning(
            "Warning",
            "Please enter some text."
        )
        return

    source = LANGUAGES[source_combo.get()]
    target = LANGUAGES[target_combo.get()]

    # Same language
    if source == target:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, text)
        return

    # Show loading message
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "Translating...")
    root.update()

    try:

        # MyMemory Translation API
        url = "https://api.mymemory.translated.net/get"

        params = {
            "q": text,
            "langpair": source + "|" + target
        }

        response = requests.get(
            url,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        # -----------------------------
        # Get main translation
        # -----------------------------
        translated = data.get(
            "responseData",
            {}
        ).get(
            "translatedText",
            ""
        )

        # -----------------------------
        # If main translation is empty,
        # check matches
        # -----------------------------
        if not translated:

            matches = data.get("matches", [])

            for match in matches:

                translated = match.get(
                    "translation",
                    ""
                )

                if translated:
                    break

        # -----------------------------
        # Display translation
        # -----------------------------
        if translated:

            output_text.delete("1.0", tk.END)

            output_text.insert(
                tk.END,
                translated
            )

        else:

            output_text.delete("1.0", tk.END)

            output_text.insert(
                tk.END,
                "No translation found."
            )

    # -----------------------------
    # Internet timeout
    # -----------------------------
    except requests.exceptions.Timeout:

        output_text.delete("1.0", tk.END)

        output_text.insert(
            tk.END,
            "Error: Server took too long to respond."
        )

    # -----------------------------
    # Internet connection
    # -----------------------------
    except requests.exceptions.ConnectionError:

        output_text.delete("1.0", tk.END)

        output_text.insert(
            tk.END,
            "Error: Please check your internet connection."
        )

    # -----------------------------
    # HTTP error
    # -----------------------------
    except requests.exceptions.HTTPError as e:

        output_text.delete("1.0", tk.END)

        output_text.insert(
            tk.END,
            "HTTP Error:\n" + str(e)
        )

    # -----------------------------
    # Other errors
    # -----------------------------
    except Exception as e:

        output_text.delete("1.0", tk.END)

        output_text.insert(
            tk.END,
            "Error:\n" + str(e)
        )


# -----------------------------
# Copy Translation
# -----------------------------
def copy_translation():

    text = output_text.get(
        "1.0",
        tk.END
    ).strip()

    if not text:

        messagebox.showwarning(
            "Warning",
            "There is no translation to copy."
        )

        return

    root.clipboard_clear()

    root.clipboard_append(text)

    root.update()

    messagebox.showinfo(
        "Copied",
        "Translation copied successfully!"
    )


# -----------------------------
# Main Window
# -----------------------------
root = tk.Tk()

root.title(
    "Language Translation Tool"
)

root.geometry(
    "700x650"
)

root.resizable(
    False,
    False
)


# -----------------------------
# Title
# -----------------------------
title = tk.Label(
    root,
    text="Language Translation Tool",
    font=("Arial", 24, "bold")
)

title.pack(pady=20)


# -----------------------------
# Source Language
# -----------------------------
tk.Label(
    root,
    text="Source Language",
    font=("Arial", 12, "bold")
).pack()

source_combo = ttk.Combobox(
    root,
    values=list(LANGUAGES.keys()),
    state="readonly",
    width=30
)

source_combo.set("English")

source_combo.pack(pady=8)


# -----------------------------
# Target Language
# -----------------------------
tk.Label(
    root,
    text="Target Language",
    font=("Arial", 12, "bold")
).pack()

target_combo = ttk.Combobox(
    root,
    values=list(LANGUAGES.keys()),
    state="readonly",
    width=30
)

target_combo.set("Telugu")

target_combo.pack(pady=8)


# -----------------------------
# Input Text
# -----------------------------
tk.Label(
    root,
    text="Enter Text",
    font=("Arial", 12, "bold")
).pack(pady=(15, 5))

input_text = tk.Text(
    root,
    height=7,
    width=70,
    font=("Arial", 12)
)

input_text.pack()


# -----------------------------
# Translate Button
# -----------------------------
translate_button = tk.Button(
    root,
    text="Translate",
    command=translate_text,
    font=("Arial", 12, "bold"),
    padx=30,
    pady=8
)

translate_button.pack(pady=15)


# -----------------------------
# Output Label
# -----------------------------
tk.Label(
    root,
    text="Translated Text",
    font=("Arial", 12, "bold")
).pack()


# -----------------------------
# Output Text
# -----------------------------
output_text = tk.Text(
    root,
    height=7,
    width=70,
    font=("Arial", 12)
)

output_text.pack(pady=5)


# -----------------------------
# Copy Button
# -----------------------------
copy_button = tk.Button(
    root,
    text="Copy Translation",
    command=copy_translation,
    font=("Arial", 11, "bold"),
    padx=25,
    pady=7
)

copy_button.pack(pady=12)


# -----------------------------
# Start Program
# -----------------------------
root.mainloop()