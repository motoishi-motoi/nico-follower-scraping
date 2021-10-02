FROM python
RUN apt-get update && apt-get install -y sudo ssh
WORKDIR /opt
RUN apt install -y gnupg && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    apt clean && \
    rm -rf ~/var/lib/apt/lists/ && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get install -y fonts-ipafont-gothic --no-install-recommends && \
    pip install selenium chromedriver-binary~=$(/usr/bin/google-chrome --version | perl -pe 's/([^0-9]+)([0-9]+\.[0-9]+).+/$2/g')
WORKDIR /mnt/src
CMD ["bash"]