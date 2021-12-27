FROM python:3

WORKDIR /app

# Copy application files
COPY destroy_git_branch_builds.py /usr/local/bin/destroy_git_branch_builds.py
COPY run_app.sh /usr/local/bin/run_app

# Create non-root user and install dependencies
RUN useradd -m app
USER app

# Install and add tfenv to non-root user path
RUN git clone https://github.com/tfutils/tfenv.git ~/.tfenv
RUN echo 'export PATH="$HOME/.tfenv/bin:$PATH"' >> ~/.bash_profile

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["/usr/local/bin/run_app"]
