#!/usr/bin/env python3
"""Capture HuggingFace Space logs and create shareable base64 URL"""
import requests
import base64
import gzip
import json
from datetime import datetime

SPACE_ID = "introspector/meta-meme"
HF_API = "https://huggingface.co/api"

def get_space_runtime():
    """Get space runtime status"""
    url = f"{HF_API}/spaces/{SPACE_ID}"
    response = requests.get(url)
    return response.json()

def get_space_logs():
    """Get space logs from SSE endpoint"""
    url = f"{HF_API}/spaces/{SPACE_ID}/events"
    
    try:
        response = requests.get(url, stream=True, timeout=10)
        logs = []
        
        for line in response.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                if decoded.startswith('data:'):
                    logs.append(decoded[5:].strip())
        
        return logs
    except Exception as e:
        return [f"Error fetching logs: {str(e)}"]

def capture_logs():
    """Capture all available log data"""
    print("📊 Capturing HuggingFace Space logs...")
    
    # Get runtime status
    runtime = get_space_runtime()
    
    # Extract error message if present
    error_msg = runtime.get('runtime', {}).get('errorMessage', 'No error')
    stage = runtime.get('runtime', {}).get('stage', 'Unknown')
    
    # Get live logs
    live_logs = get_space_logs()
    
    # Compile log data
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "space_id": SPACE_ID,
        "stage": stage,
        "error_message": error_msg,
        "live_logs": live_logs,
        "runtime": runtime.get('runtime', {})
    }
    
    return log_data

def create_shareable_url(log_data):
    """Compress and encode logs as base64 URL"""
    # Convert to JSON
    json_data = json.dumps(log_data, indent=2)
    
    # Compress with gzip
    compressed = gzip.compress(json_data.encode('utf-8'), compresslevel=9)
    
    # Encode as base64
    b64_encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
    
    # Create shareable URL
    url = f"https://meta-meme.streamlit.app/?logs={b64_encoded}"
    
    return url, len(json_data), len(url)

def main():
    # Capture logs
    log_data = capture_logs()
    
    # Create shareable URL
    url, original_size, compressed_size = create_shareable_url(log_data)
    
    # Save to file
    with open("hf_logs.json", "w") as f:
        json.dump(log_data, f, indent=2)
    
    with open("hf_logs_url.txt", "w") as f:
        f.write(url)
    
    # Print results
    print(f"\n✅ Logs captured!")
    print(f"Stage: {log_data['stage']}")
    print(f"Original size: {original_size:,} bytes")
    print(f"Compressed URL: {compressed_size:,} bytes")
    print(f"Compression: {compressed_size/original_size*100:.1f}%")
    print(f"\n📝 Saved to:")
    print(f"  - hf_logs.json (full logs)")
    print(f"  - hf_logs_url.txt (shareable URL)")
    print(f"\n🔗 Shareable URL:")
    print(url[:200] + "...")
    
    # Print error if present
    if log_data['error_message'] != 'No error':
        print(f"\n❌ Error Message:")
        print(log_data['error_message'][:500])

if __name__ == "__main__":
    main()
