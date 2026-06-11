# 1. Start with a "clean" Python environment
FROM python:3.11-slim

# 2. Install the "Construction Tools" (C++ Compiler)
RUN apt-get update && apt-get install -y \
    g++ \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# 3. Set the "Living Room" of our container
WORKDIR /app

# 4. Copy your project files into the container
COPY . /app

# 5. Install the AI Libraries (Torch)
RUN pip install --no-cache-dir torch torchvision pybind11

# 6. Build the C++ Engine INSIDE the container
RUN g++ -O3 -Wall -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) \
    banana_module.cpp -o banana_engine.so

# 7. Tell the container what to do when it starts
CMD ["python", "warehouse_master.py"]

