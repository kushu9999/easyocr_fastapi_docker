FROM pytorch/pytorch

# if you forked EasyOCR, you can pass in your own GitHub username to use your fork
# i.e. gh_username=myname
ARG gh_username=JaidedAI
ARG service_home="/home/EasyOCR"

WORKDIR "$service_home"

# Configure apt and install packages
RUN apt-get update -y && \
    apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-dev \
    git \
    # cleanup
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists

# Clone EasyOCR repo
RUN git clone "https://github.com/$gh_username/EasyOCR.git" "$service_home" \
    && git remote add upstream "https://github.com/JaidedAI/EasyOCR.git" \
    && git pull upstream master

# Build
RUN python setup.py build_ext --inplace -j 4 \
    && python -m pip install -e .

COPY requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

