def print_lung_cancer_info():
    """Print information about lung cancer"""
    
    info = {
        "Definition": "Lung cancer is a malignant tumor that forms in the lungs.",
        "Types": [
            "Small Cell Lung Cancer (SCLC)",
            "Non-Small Cell Lung Cancer (NSCLC)"
        ],
        "Risk Factors": [
            "Smoking",
            "Secondhand smoke exposure",
            "Radon gas",
            "Family history",
            "Environmental toxins"
        ],
        "Symptoms": [
            "Persistent cough",
            "Chest pain",
            "Shortness of breath",
            "Hoarseness",
            "Coughing up blood"
        ],
        "Diagnosis Methods": [
            "Chest X-ray",
            "CT scan",
            "Biopsy",
            "PET scan"
        ],
        "Treatment Options": [
            "Surgery",
            "Chemotherapy",
            "Radiation therapy",
            "Targeted therapy",
            "Immunotherapy"
        ]
    }
    
    print("=" * 50)
    print("LUNG CANCER INFORMATION")
    print("=" * 50)
    
    for category, content in info.items():
        print(f"\n{category}:")
        if isinstance(content, list):
            for item in content:
                print(f"  - {item}")
        else:
            print(f"  {content}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    print_lung_cancer_info()