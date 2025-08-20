#!/usr/bin/env python3
"""
Simple script to start both services
Gateway (8080) and Registry (8081)
"""

import subprocess
import sys
import time
import os

def start_service(script_name, port, service_name):
    """Start a service in a subprocess"""
    try:
        print(f"[START] Starting {service_name} on port {port}...")
        process = subprocess.Popen([
            sys.executable, script_name
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(2)  # Give service time to start
        
        if process.poll() is None:  # Process is still running
            print(f"[START] {service_name} started successfully")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"[START] Failed to start {service_name}")
            print(f"Error: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"[START] Error starting {service_name}: {e}")
        return None

def main():
    """Start both services"""
    print("[MAIN] Starting K8s Service Mesh Simulation")
    print("=" * 50)
    
    processes = []
    
    # Start Registry (port 8081)
    registry_process = start_service("registry.py", 8081, "Service Registry")
    if registry_process:
        processes.append(("Service Registry", registry_process))
    
    # Start Gateway (port 8080)  
    gateway_process = start_service("gateway.py", 8080, "Service Mesh Gateway")
    if gateway_process:
        processes.append(("Service Mesh Gateway", gateway_process))
    
    if not processes:
        print("[MAIN] Failed to start any services")
        return
    
    print("\n" + "=" * 50)
    print("[MAIN] K8s Service Mesh Simulation Started!")
    print("=" * 50)
    print("[MAIN] Service Registry: http://localhost:8081")
    print("[MAIN] Service Gateway:  http://localhost:8080")
    print("[MAIN] API Docs:        http://localhost:8080/docs")
    print("=" * 50)
    print("Services running:")
    for name, _ in processes:
        print(f"  [RUNNING] {name}")
    print("\nPress Ctrl+C to stop all services")
    
    try:
        # Keep script running
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            for name, process in processes:
                if process.poll() is not None:
                    print(f"[WARNING] {name} stopped unexpectedly")
                    
    except KeyboardInterrupt:
        print("\n[MAIN] Stopping all services...")
        
        for name, process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"[STOP] {name} stopped")
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"[STOP] {name} force killed")
            except Exception as e:
                print(f"[STOP] Error stopping {name}: {e}")
        
        print("[MAIN] All services stopped")

if __name__ == "__main__":
    main()