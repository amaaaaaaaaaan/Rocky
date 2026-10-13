# Check memory stats
vm_stat | head -20

# Check if Ollama is running
ps aux | grep ollama

# Kill Ollama when done
pkill ollama

# Stop specific model
ollama stop llama3.2-vision

# Clear cache manually
sudo purge

# Start Ollama with memory release after each use
OLLAMA_KEEP_ALIVE=0 ollama serve

# Activate Rocky environment
source Rocky/bin/activate

# Install packages inside env
pip install ollama
pip install opencv-python

# Check installed packages
pip list