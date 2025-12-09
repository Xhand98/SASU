# -------- Stage 1: Build dependencies --------
FROM python:3.11-alpine AS builder

# Install only necessary build tools
RUN apk add --no-cache gcc musl-dev libffi-dev python3-dev cargo

# Set workdir
WORKDIR /bot

# Copy only files needed for dependency install
COPY requirements.txt .

# Install packages into a temporary directory
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# -------- Stage 2: Final image --------
FROM python:3.11-alpine

# Set working directory
WORKDIR /bot

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy the rest of your project
COPY . .

# Comment out `audioop` which isn't available on Alpine
RUN sed -i 's/^import audioop/# import audioop/' /usr/local/lib/python3.11/site-packages/discord/player.py

# Replace buggy NewSimpleSQL with your fixed version
COPY ./lib/fixes/SimpleSQLite.py /usr/local/lib/python3.11/site-packages/NewSimpleSQL/SimpleSQLite.py

# Optional: Run database setup before main
# CMD ["sh", "-c", "python db/dbsetup.py && python main.py"]

# If you don't need setup, just run the bot
CMD ["python", "main.py"]
