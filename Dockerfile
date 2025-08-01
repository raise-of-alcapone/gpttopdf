FROM python:3.11-slim

WORKDIR /app

# System dependencies (cached until Dockerfile changes)
RUN apt-get update && apt-get install -y \
    wget gnupg curl fonts-liberation libappindicator3-1 \
    libasound2 libatk-bridge2.0-0 libdrm2 libgtk-3-0 \
    libnspr4 libnss3 libxss1 libxtst6 xdg-utils \
    libxrandr2 libpangocairo-1.0-0 libatk1.0-0 \
    libcairo-gobject2 libgdk-pixbuf2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Create user FIRST (rarely changes)
RUN useradd -m -u 1000 appuser

# Python dependencies (cached until requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Playwright system dependencies (cached until Dockerfile changes)
RUN playwright install-deps chromium

# Install Chromium as root to cache in system location
# This way it survives user switches and gets cached
ENV PLAYWRIGHT_BROWSERS_PATH=/usr/local/lib/playwright
RUN mkdir -p $PLAYWRIGHT_BROWSERS_PATH && \
    playwright install chromium && \
    chmod -R 755 $PLAYWRIGHT_BROWSERS_PATH

# App code (changes frequently - put LAST for minimal rebuilds)
COPY . .
RUN chown -R appuser:appuser /app

# Switch to user for runtime
USER appuser

EXPOSE 5000
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:app"]
