import enum
from typing_extensions import TypedDict

class ReportType(enum.Enum):
    Blood_Test_Reports = "Blood Test Reports" # Regular checkups for things like sugar levels, iron, etc.
    Urine_Test_Results = "Urine Test Results" # Checks for infections or other issues.
    Hormone_Levels = "Hormone Levels" # Pregnancy-related hormones (like hCG).
    Genetic_Tests = "Genetic Tests" # Early tests for any potential genetic conditions.
    Ultrasound_Scans = "Ultrasound Scans Reports" # Regular baby scans (3D, 4D) showing development.
    Babys_Reports = "Baby's Reports" # Measuring how the baby is growing (height, weight and more).
    Blood_Flow_Check_Doppler_Reports = "Doppler Reports" # Reports on the blood flow to the baby and placenta.
    Vaccination_Records = "Vaccination Records"
    Doctor_Prescriptions_and_Reports = "Doctor Prescriptions and Reports" # Recommendations or advice from your doctor.
    Delivery_Reports = "Delivery Reports" # Information about the delivery and post-birth care.
    Other_Reports_and_Scans  = "Other Reports and Scans" # Rest all details

class ReportContent(TypedDict):
    report_type: ReportType
    report_content: list[str]