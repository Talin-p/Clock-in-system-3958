# Live Bar Graph with Google Sheets Integration

This project is a **standalone HTML application** that displays a **live-updating bar graph** based on data from a Google Sheet. Each bar represents a person with their name, profile image, and accumulated time in seconds.

## Features

* **Google Sheets Integration**

  * Reads data (Name, TimeSeconds, ImageURL) directly from a published Google Sheet (CSV format).
  * Automatically fetches and updates entries once every 24 hours.

* **Dynamic Bar Graph**

  * Bars grow in real-time to represent elapsed time
  * Rows reorder automatically so the highest time always appears at the top.
  * Each bar shows both a graphical bar and a formatted time label (h/m/s).

* **Controls**

  * **Pause / Resume All** – Stops or resumes time tracking for all participants.
  * **Pause / Resume Individual** – Control each participant’s timer separately.
  * **Export Times** – Downloads all current data as a CSV file.

* **Customization**

  * **Background & Bar Colors** – Change global background or bar colors using color pickers.
  * **Individual Bar Colors** – Click a bar to assign it a unique color.

## How It Works

1. The HTML file fetches a CSV export from Google Sheets.
2. The sheet must contain three columns:

   * `Name`
   * `TimeSeconds`
   * `ImageURL`
3. Data is parsed and rendered dynamically into rows with name, image, bar, and time.
4. Timers update every second, while the Google Sheet is polled once every 24 hours for changes.

## Setup

1. Publish your Google Sheet to the web and copy its CSV link.
2. Replace the `GOOGLE_SHEET_CSV_URL` in the script with your own sheet link.
3. Open the HTML file in any browser (desktop or mobile).

## Exporting Data

* Click **Export Times** to download a snapshot of the current times as `times.csv`.

---
