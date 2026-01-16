"""
Test script for drowsiness detector
Tests different scenarios and generates demo data
"""

import cv2
import numpy as np
from detector import DrowsinessDetector
import time

def test_with_webcam():
    """Test with live webcam - same as main detector test"""
    print("🎥 Testing with webcam...")
    detector = DrowsinessDetector()
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Cannot open webcam")
        return
    
    print("✅ Webcam ready. Press 'q' to quit")
    print("📋 Test checklist:")
    print("   1. Normal state (should show LOW)")
    print("   2. Close eyes for 2+ seconds (should show HIGH)")
    print("   3. Blink rapidly (should track blinks)")
    
    start_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        result = detector.detect_drowsiness(frame)
        
        # Show annotated frame
        cv2.imshow('Detector Test', result["frame"])
        
        # Print metrics every 3 seconds
        if time.time() - start_time > 3:
            print(f"\n📊 Current Metrics:")
            print(f"   Alert Level: {result['alert_level']}")
            print(f"   EAR: {result['metrics']['ear']}")
            print(f"   Eye Closed: {result['metrics']['eye_closed_duration']}s")
            print(f"   PERCLOS: {result['metrics']['perclos']:.1%}")
            start_time = time.time()
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Print final report
    print("\n" + "="*50)
    print("BIAS TESTING REPORT")
    print("="*50)
    report = detector.get_bias_testing_report()
    for key, value in report.items():
        if isinstance(value, list):
            print(f"\n{key}:")
            for item in value:
                print(f"  • {item}")
        else:
            print(f"{key}: {value}")


def test_with_video_file(video_path):
    """Test with pre-recorded video file"""
    print(f"🎬 Testing with video file: {video_path}")
    detector = DrowsinessDetector()
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"❌ Cannot open video: {video_path}")
        return
    
    frame_count = 0
    alerts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        result = detector.detect_drowsiness(frame)
        alerts[result["alert_level"]] += 1
        
        # Show every 30th frame to speed up
        if frame_count % 30 == 0:
            cv2.imshow('Video Test', result["frame"])
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n✅ Processed {frame_count} frames")
    print(f"Alert Distribution:")
    print(f"   LOW: {alerts['LOW']} frames ({alerts['LOW']/frame_count*100:.1f}%)")
    print(f"   MEDIUM: {alerts['MEDIUM']} frames ({alerts['MEDIUM']/frame_count*100:.1f}%)")
    print(f"   HIGH: {alerts['HIGH']} frames ({alerts['HIGH']/frame_count*100:.1f}%)")


def generate_demo_scenarios():
    """Generate demo data for testing without live camera"""
    print("🎭 Generating demo scenarios...")
    
    detector = DrowsinessDetector()
    
    scenarios = [
        {
            "name": "Normal Driving",
            "ear": 0.30,
            "eye_closed_duration": 0.2,
            "perclos": 0.05,
            "expected": "LOW"
        },
        {
            "name": "Mild Fatigue",
            "ear": 0.22,
            "eye_closed_duration": 1.5,
            "perclos": 0.16,
            "expected": "MEDIUM"
        },
        {
            "name": "Severe Drowsiness",
            "ear": 0.15,
            "eye_closed_duration": 2.5,
            "perclos": 0.25,
            "expected": "HIGH"
        }
    ]
    
    print("\n" + "="*60)
    print("DEMO SCENARIOS FOR PRESENTATION")
    print("="*60)
    
    for scenario in scenarios:
        print(f"\n📋 Scenario: {scenario['name']}")
        print(f"   EAR: {scenario['ear']}")
        print(f"   Eye Closed Duration: {scenario['eye_closed_duration']}s")
        print(f"   PERCLOS: {scenario['perclos']:.1%}")
        print(f"   Expected Alert: {scenario['expected']}")
        print(f"   ✓ Ready for demo")


def integration_test():
    """Test the integration function for Person B"""
    print("🔗 Testing integration with Person B's alert system...")
    
    from detector import get_drowsiness_data
    
    detector = DrowsinessDetector()
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Cannot open webcam")
        return
    
    print("✅ Testing simplified output format...")
    
    for i in range(10):
        ret, frame = cap.read()
        if not ret:
            break
        
        # This is what Person B will call
        data = get_drowsiness_data(frame, detector)
        
        print(f"\nFrame {i+1}:")
        print(f"  Alert Level: {data['alert_level']}")
        print(f"  Confidence: {data['confidence']}")
        print(f"  Metrics: {data['metrics']}")
        
        time.sleep(0.5)
    
    cap.release()
    print("\n✅ Integration test complete!")


if __name__ == "__main__":
    print("="*60)
    print("  VigilDrive AI - Detector Testing Suite")
    print("  Person A: Computer Vision Testing")
    print("="*60)
    print()
    print("Choose a test:")
    print("1. Test with webcam (live detection)")
    print("2. Test with video file")
    print("3. Generate demo scenarios")
    print("4. Test integration with Person B")
    print()
    
    choice = input("Enter choice (1-4): ")
    
    if choice == "1":
        test_with_webcam()
    elif choice == "2":
        video_path = input("Enter video file path: ")
        test_with_video_file(video_path)
    elif choice == "3":
        generate_demo_scenarios()
    elif choice == "4":
        integration_test()
    else:
        print("Invalid choice. Running webcam test by default...")
        test_with_webcam()

        