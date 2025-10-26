

{0}------------------------------------------------

![](_page_0_Picture_0.jpeg)

*INNOVATING SOLUTIONS*

A **Thales** company

![](_page_0_Picture_3.jpeg)

![](_page_0_Picture_4.jpeg)

![](_page_0_Picture_5.jpeg)

**Deliverable Reference  :**  D3.5
**Title                  :**  Demonstration Procedures 

**Confidentiality Level :** PU

- **Lead Partner :** DLR
- **Abstract :** This document presents the specification of the demonstration test procedures covering the WP4 activities. Preliminary procedures are described for the integration and demonstration tests covering WP5
- **EC Grant N° :** 821996

**Project Officer EC**

**Project Officer EC :** Christos Ampatzis (REA)

![](_page_0_Picture_15.jpeg)

MOSAR is co-funded by the Horizon 2020 Framework Programme of the European Union

{1}------------------------------------------------

![](_page_1_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 1  
---
Demonstration Prodedures  

| DOCUMENT CHANGE RECORD |            |                       |                                                                   |                                                                                                                                                                                             |
|------------------------|------------|-----------------------|-------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Version                | Date       | Author                | Changed<br>Sections /<br>Pages                                    | Reason for Change / RID No                                                                                                                                                                  |
| 1.0.0                  | 16/06/2020 | Consortium            | All                                                               | First release for CDR milestone review                                                                                                                                                      |
| 1.1.0                  | 05/08/2020 | Space<br>Applications | Section 2.1,<br>test IDCT-A-2<br><br>Section 4.2.2,<br>Scenario 2 | Add power-off test on the WM, with attached<br>payload, as feedback to RID OG09-117<br>Add note about generation/detection and<br>action on fault detection, as feedback to RID<br>OG09-119 |

{2}------------------------------------------------

![](_page_2_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 2  
---
Demonstration Prodedures  

### Demonstration Procedures

| 1 |     |       | Introduction  6                                    |  |
|---|-----|-------|----------------------------------------------------|--|
|   | 1.1 |       | Purpose and Scope 6                                |  |
|   | 1.2 |       | Document Structure  7                              |  |
|   | 1.3 |       | Applicable Documents 7                             |  |
|   | 1.4 |       | Reference Documents 8                              |  |
|   | 1.5 |       | Acronyms 8                                         |  |
| 2 |     |       | Component Validation Test (Partners site, WP4)  10 |  |
|   | 2.1 |       | Walking Manipulator 10                             |  |
|   | 2.2 |       | B-HOTDOCK Standard Interface  15                   |  |
|   | 2.3 |       | Spacecraft Modules and Components  19              |  |
|   |     | 2.3.1 | cPDU  19                                           |  |
|   |     | 2.3.2 | R-ICU / FMC Board  20                              |  |
|   |     | 2.3.3 | Battery Subsystem  24                              |  |
|   |     | 2.3.4 | Thermal Subsystem 25                               |  |
|   | 2.4 |       | Design and Simulator Tools  28                     |  |
|   | 2.5 |       | Planner and Agent 29                               |  |
|   | 2.6 |       | MCC and PUS Service 30                             |  |
|   | 2.7 |       | Visual Subsystem 32                                |  |
| 3 |     |       | Integration Tests (On-site, end WP4-WP5)  38       |  |
|   | 3.1 |       | Sub-Systems Validation Tests  38                   |  |
|   |     | 3.1.1 | ST1 - Monitoring and Control Centre  38            |  |
|   |     | 3.1.2 | ST2 - Design and Simulation Tool 39                |  |
|   |     | 3.1.3 | ST3 – Planner and Simulation Tool 40               |  |
|   |     | 3.1.4 | ST4 - Servicer Spacecraft Bus (SVC)  42            |  |
|   |     | 3.1.5 | ST5 - Client Satellite Bus (CLT)  43               |  |
|   |     | 3.1.6 | ST6 - Spacecraft Modules (SM)  44                  |  |
|   |     | 3.1.7 | ST7 - Walking Manipulator  47                      |  |
|   |     | 3.1.8 | ST10-Visual Processing System  49                  |  |
|   | 3.2 |       | Integration Validation Tests 51                    |  |
|   |     | 3.2.1 | IT1 – WM Re-localization  51                       |  |
|   |     | 3.2.2 | IT2 – SM Re-localization  52                       |  |
|   |     | 3.2.3 | IT3 – Data Re-Routing 53                           |  |
|   |     | 3.2.4 | IT4 – Power Re-Routing  53                         |  |
|   |     | 3.2.5 | T5 – Software Reconfiguration 54                   |  |

{3}------------------------------------------------

![](_page_3_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 3  
---
Demonstration Prodedures  

|   |     | 3.2.6 | IT6 – Planned Operation  54                                  |                                                              
|---|-----|-------|--------------------------------------------------------------|
| 4 |     |       | Demonstration Scenarios (On-site, WP5) 56                    |                                                              
|   | 4.1 |       | Scenario 1 (S1): Initial Assembly of SMs from SVC to CLT  56 |                                                              
|   |     | 4.1.1 | Scenario Description  56                                     |                                                              
|   |     | 4.1.2 | Sequence of Operations 57                                    |                                                              
|   | 4.2 |       | Scenario 2 (S2): Replacement of a failed SM  57              |                                                              
|   |     | 4.2.1 | Scenario Description  57                                     |                                                              
|   |     | 4.2.2 | Sequence of Operations 58                                    |                                                              
|   | 4.3 |       | Scenario 3 (S3): Thermal transfer between two SMs  58        |                                                              
|   |     | 4.3.1 | Scenario Description  58                                     |                                                              
|   |     | 4.3.2 | Sequence of Operations 59                                    |                                                              
|   | 4.4 |       | Scenario 4 (S4): Automatic CLT Network Reconfiguration 59    |                                                              
|   |     | 4.4.1 | Scenario Description  59                                     |                                                              
|   |     | 4.4.2 | Sequence of Operations 60                                    |                                                              
|   | 4.5 |       | Scenario 5 (S5): Software Reconfiguration 60                 |                                                              
|   |     | 4.5.1 | Scenario Description  60                                     |                                                              
|   |     | 4.5.2 | Sequence of Operations 60                                    |                                                              
|   | 4.6 |       | Demonstrator Requirements Addressed by the Scenarios 60      |                                                              
| 5 |     |       | Demonstration Setup 62                                       |                                                              
|   | 5.1 |       | General Layout 62                                            |                                                              
|   | 5.2 |       | Demonstrator Components  64                                  |                                                              
|   |     | 5.2.1 | Ground Segment – Monitoring and Control Centre 64            |                                                              
|   |     | 5.2.2 | Space Segment  65                                            |                                                              
|   |     | 5.2.3 | Other Components  66                                         |                                                              
|   | 5.3 |       | Demonstrator Safety  66                                      |                                                              
| 6 |     |       | Annex  67                                                    |                                                              
|   | 6.1 |       | MOSAR Sequence of Manipulations Example 67                   |                                                              

{4}------------------------------------------------

![](_page_4_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 4  
---
Demonstration Prodedures  

# **List of Figures**

| Figure 1-1: MOSAR Demonstrator Global Architecture ................................................ 6      |
|------------------------------------------------------------------------------------------------------------|
| Figure 3-1: Routine 1 – WM re-localization between initial SI and Target SI .................... 51        |
| Figure 3-2: Routine 2 – SM re-localization ............................................................ 52 |
| Figure 4-1: MOSAR scenario 1 initial and final configuration ................................ 56           |
| Figure 4-2: MOSAR scenario 2 initial and final configuration ................................ 58           |
| Figure 5-1: MOSAR Setup View in SpaceApps Laboratory Environment ...................... 62                 |
| Figure 5-2: MOSAR Setup top layout ................................................................. 63    |
| Figure 5-3: MOSAR setup side layout ................................................................. 63   |
| Figure 5-4: MCC Setup and visualization screens ................................................ 64        |
| Figure 5-5: DC Bench power supply (Keysight or equivalent) ................................. 65            |

{5}------------------------------------------------

![](_page_5_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 5  
---
Demonstration Prodedures  

# **List of Tables**

| Table 1-1: High level functionalities demonstrated in MOSAR      | 7  |
|------------------------------------------------------------------|----|
| Table 6-1: Scenarios 1 and 2 step-by-step sequence of operations | 67 |

{6}------------------------------------------------

![](_page_6_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 6  
---
Demonstration Prodedures  

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 6  
---
Demonstration Prodedures  

# <span id="page-6-0"></span>**1 Introduction**

The testing validation campaign will consist of an extended series of tests ranging from components validation to the full setup/demonstration of the five selected scenarios foreseen in the activity. The purpose will be to illustrate all the main functionalities of modular spacecraft, including the ground support tools (design, simulation and planning), the operational concept of manipulator and spacecraft module relocation and resources re-allocation.

## <span id="page-6-1"></span>**Purpose and Scope**

The autonomous transfer and configuration of the SM follow an execution plan prepared and validated off-line, in the Monitoring and Control Centre (MCC), on the ground segment. The MCC includes a satellite design, modelling and validation tool, specifically targeting modular satellites applications. It also allows the automatic planning of the assembly or reconfiguration sequence that can be verified with a multi-physics simulator. All these elements are working iteratively together to prepare a valid execution plan that is finally uploaded to the spacecraft for execution. Based on the monitoring and feedback information received from the spacecraft during the operations (e.g. detected failed module), the MCC can update the execution plan. The MCC finally includes visualisation front-end to support the design, verification and monitoring activities during sequence execution.

![](_page_6_Figure_8.jpeg)

**Figure 1-1: MOSAR Demonstrator Global Architecture**

<span id="page-6-2"></span>The purpose of the ground laboratory demonstrator is to demonstrate the concept of modular spacecraft as presented above. System modularity can be defined at different levels:

- Hardware: with the possibility to re-configure the physical arrangement of the spacecraft and/or providing means to replace/upgrade specific functions.
- Software: with the possibility to re-configure node responsibilities and support the reconfiguration operations
- Data: with the possibility to re-route TM/TC and data transmission along the different nodes
- Power: with the possibility to re-route and control the power transmission along the nodes.

{7}------------------------------------------------

![](_page_7_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 7  
---
Demonstration Prodedures  

The MOSAR demonstrator shall allow verifying and validating the following high level functionalities relevant for future modular spacecraft missions ([VerR\_G101], with reference to the MOSAR mission's requirements [\[AD1\]\)](#page-7-3):

**Table 1-1: High level functionalities demonstrated in MOSAR**

<span id="page-7-2"></span>

| Requirements                       | High level functionalities                               |
|------------------------------------|----------------------------------------------------------|
| FuncR_S105                         | Design and creation of a re-configuration execution plan |
| FuncR_S106                         | Simulation of the execution plan                         |
| FuncR_S101                         | Manipulation and repositioning of SM                     |
| FuncR_S104, FuncR_S107             | Control and re-location of the WM                        |
| FuncR_S102                         | Update/upgrade of satellite functionalities              |
| FuncR_S119, FuncR_S121             | Data and power transfer between SM                       |
| FuncR_S110, FuncR_S120, FuncR_S122 | Resources re-allocation, data and power routing          |
| FuncR_S115                         | Heat management between SM                               |
| FuncR_S111                         | Failure detection and handling                           |

In [RD5](#page-8-2) a set of tests are described that will be performed on the integrated setup and/or during the final integration. The purpose is on confirming the readiness for the demonstration. These tests imply the availability of multiple components and also multiple partners at one location.

This chapter provides the description of the tests and demonstrations procedures that validate the project requirements, and more particular the ones under testing validation (see [RD1\)](#page-8-3). Some of these requirements are related to specific components, other ones to sub-systems or the full setup/demonstration.

### <span id="page-7-0"></span>**Document Structure**

In brief, the document is structured as follows:

- Chapter 2 Component Validation Test (Partners site, WP4)
- Chapter 3 Integration Tests (On-site, end WP4-WP5)
- Chapter 4 Demonstration Scenarios (On-site, WP5)

Chapter 5 Annex

### <span id="page-7-1"></span>**Applicable Documents**

- <span id="page-7-3"></span>AD1 Strategic Research Cluster "Space Robotics Technologies" – Collaboration Agreement
- AD2 MOSAR Consortium Agreement, version 1.0 (7-Nov-2018)
- AD3 MOSAR Grant Agreement (821996) (18-Jan-2019)
- AD4 MOSAR D1.4 System Requirements Document, MOSAR-WP1-D1.4-SA issue 1.0.0 (1-Sep-2019)

{8}------------------------------------------------

![](_page_8_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 8  
---
Demonstration Prodedures  

### <span id="page-8-0"></span>**Reference Documents**

- <span id="page-8-3"></span>RD1 MOSAR D1.4 System Requirements Document, MOSAR-WP1-D1.4-SA, issue 1.1.0
- RD2 MOSAR D2.1 OG1-5 Adaptations and Extensions Specifications, MOSAR-WP2-D2.1-GMV issue 1.0.0
- RD3 MOSAR D2.2 Non-building block components preliminary design, MOSAR-WP2-D2.2-SA, issue 1.0.0
- RD4 MOSAR D2.4 Preliminary Design Document, MOSAR-WP2-D2.4-SA issue 1.0.0
- <span id="page-8-2"></span>RD5 MOSAR D2.3 Test Demonstration Specification, MOSAR-WP2-D2.3-SA issue 1.1.0
- <span id="page-8-4"></span>RD6 MOSAR D3.6 Detailed Design Document (DDD), MOSAR-WP3-D3.6-SA issue 1.0.0

### <span id="page-8-1"></span>**Acronyms**

| BAT  | Battery System                                   |
|------|--------------------------------------------------|
| CDR  | Critical Design Review                           |
| CLT  | CLienT (satellite)                               |
| cPDU | centralized Power Distribution Unit              |
| EGSE | Electrical Ground Support Equipment              |
| ESA  | European Space Agency                            |
| FES  | Functional Engineering Simulator                 |
| FMC  | FPGA Mezzanine Card                              |
| ICD  | Interface Control Document                       |
| IDC  | Insulation Displacement Connector                |
| KPI  | Key Performance Indicators                       |
| DMS  | Data Management System                           |
| MAIT | Manufacturing, Assembly, Integration and Testing |
| MCC  | Monitoring and Control Center                    |
| MGSE | Mechanical Ground Support Equipment              |
| OBC  | On-Board Computer                                |
| OG   | Operational Grant                                |
| OSP  | Optical Sensor Payload                           |

{9}------------------------------------------------

![](_page_9_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 9  
---
Demonstration Prodedures  

| PDD | Preliminary Design Document |
|-----|-----------------------------|
| PDR | Preliminary Design Review   |
| PWS | Power System                |
| SI  | Standard Interface          |
| SVC | Service (spacecraft)        |
| THS | Thermal System              |
| TM  | Telemetry                   |
| TC  | Telecommand                 |
| TCP | Tool Center Point           |
| TRR | Test Readiness Review       |
| TTC | Telemetry and Telecommand   |
| WM  | Walking Manipulator         |

{10}------------------------------------------------

![](_page_10_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 10  
---
Demonstration Prodedures  

# <span id="page-10-0"></span>**2 Component Validation Test (Partners site, WP4)**

This section provides, for each developed component, the list of tests that will be done at the component level during WP4, before the final integration. This can be Unitary (component alone) or Combined (with another component) tests. The tests should focus either on project requirements associated specifically to the component or important characteristics that are required for the integration in the final demonstration. In general, these tests do not require colocations with partners.

## <span id="page-10-1"></span>**Walking Manipulator**

| ID                                                                      | CT-A-1                                                                          | Title                                                                                                                                                                                                                                                | WM Monitoring and Motion Control |      | Lead | DLR/SpaceApps |
|-------------------------------------------------------------------------|---------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------|------|------|---------------|
| Type                                                                    | Unitary                                                                         |                                                                                                                                                                                                                                                      | Pre-Requisite                    | N.A. |      |               |
| Purpose / Expected Result                                               |                                                                                 |                                                                                                                                                                                                                                                      |                                  |      |      |               |
| The WM is able to be controlled in the following modes, at 500 Hz:      |                                                                                 |                                                                                                                                                                                                                                                      |                                  |      |      |               |
|                                                                         | • Joint Control<br>• Cartesian Position Control<br>• Impedance Position Control |                                                                                                                                                                                                                                                      |                                  |      |      |               |
| and the WM parameters can be monitored (joint angles, current, torques) |                                                                                 |                                                                                                                                                                                                                                                      |                                  |      |      |               |
| Configuration:                                                          |                                                                                 | Procedure:                                                                                                                                                                                                                                           |                                  |      |      |               |
| - The WM is fixed on one extremity and free on the other side           |                                                                                 | - The operator initiates test sequences for each type of control methodology, by monitoring the physical motion of the arm (or interaction with environment for the impedance), the monitored variables and the update frequency of the control loop |                                  |      |      |               |
| - The WM Controller is used to perform the tests                        |                                                                                 |                                                                                                                                                                                                                                                      |                                  |      |      |               |
| Covered Requirements                                                    |                                                                                 |                                                                                                                                                                                                                                                      |                                  |      |      |               |
| FuncR_B103 (Joint position control)                                     |                                                                                 |                                                                                                                                                                                                                                                      |                                  |      |      |               |
| FuncR_B104 (Cartesian position control)                                 |                                                                                 |                                                                                                                                                                                                                                                      |                                  |      |      |               |
| FuncR_B104bis (Impedance control)                                       |                                                                                 |                                                                                                                                                                                                                                                      |                                  |      |      |               |

| ID                                                                                                                                                                                                                                               | CT-A-2  | Title                                                                                     | WM Power On/Off | Lead | DLR/SpaceApps |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|-------------------------------------------------------------------------------------------|-----------------|------|---------------|
| Type                                                                                                                                                                                                                                             | Unitary | Pre-Requisite                                                                             | N.A.            |      |               |
|                                                                                                                                                                                                                                                  |         | Purpose / Expected Result                                                                 |                 |      |               |
|                                                                                                                                                                                                                                                  |         | The WM is able to be powered on/off, keeping its current position (with use of WM brakes) |                 |      |               |
|                                                                                                                                                                                                                                                  |         | Procedure                                                                                 |                 |      |               |
| Configuration:<br>- The WM is fixed on one extremity and free on the other side or with a SM payload (or representative mass dummy)<br>- The WM power bus is connected to a 48V power supply<br>- The WM Controller is used to perform the tests |         |                                                                                           |                 |      |               |
| Procedure:<br>The operator powers on the WM through the 48V power supply and validates that the WM is keeping its current position.                                                                                                              |         |                                                                                           |                 |      |               |

- The operator powers on the WM, through the 48V power supply and validate that the WM is keeping its current position

- The operator monitors the WM TM

- The operator powers OFF the WM

- The operators verifies that the WM keeps its position

{11}------------------------------------------------

![](_page_11_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 11  
---
Demonstration Prodedures  

The procedure is repeated with free end and with an SM attached payload 

| Covered Requrements       | |
|---------------------------|-|
| FuncR_B106 (Power-on/off) | |

**Covered Requirements** FuncR\_B106 (Power-on/off)

**ID** CT-A-3 **Title** WM Lifting Capabilities **Lead** SpaceApps **Type** Unitary **Pre-Requisite** N.A. **Purpose / Expected Result** The WM is able to lift up to 10kg at the end-effector, in its workspace **Procedure** Configuration: - The WM is fixed on one extremity and free on the other side - A payload of 10kg is fixed at the end-effector - The WM power bus is connected to a 48V power supply - The WM Controller is used to perform the tests Procedure: - The operator powers on the WM, through the 48V - The WM is moved in different positions to validate its capability to move the attached mass in its workspace **Covered Requirements** PerfR\_B201 (Lifting capability)

| ID            | CT-A-4                        |
|---------------|-------------------------------|
| Title         | WM Faulty Behaviour Detection |
| Type          | Unitary                       |
| Pre-Requisite | N.A.                          |
| Lead          | DLR/SpaceApps                 |

**Purpose / Expected Result**

The WM is able to react and provide feedback about faulty behavior of the WM operations

**Procedure**

**Configuration:**

- The WM is fixed on one extremity and free on the other side
- The WM power bus is connected to a 48V power supply
- The WM Controller is used to perform the tests

**Procedure:**

- Different Faulty behaviour are simulated on the WM controller to verify the reaction of the WM as well as the update of the tracking variables
- Examples of faulty behaviour:
  - Joint Drive over-current
  - Joint over-torque / excess interaction forces
  - Variable over range
  - Others TBC

**Covered Requirements**

FuncR\_B105 (Fault detection)

| ID            | CT-A-5        |
|---------------|---------------|
| Title         | WM Weight     |
| Type          | Unitary       |
| Pre-Requisite | N.A.          |
| Lead          | DLR/SpaceApps |

{12}------------------------------------------------

![](_page_12_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 12  
---
Demonstration Prodedures  

| Purpose / Expected Result | Measure the weight of the WM                                   |
|---------------------------|----------------------------------------------------------------|
| Procedure                 | <p><b>Procedure:</b></p> <p>- Measure the weight of the WM</p> |
| Covered Requirements      | PhyR_B501 (WM Weight)                                          |

PhyR\_B501 (WM Weight)

| ID                                                                                         | CT-A-6   | Title         | WM HOTDOCK Control                                         | Lead | SpaceApps |
|--------------------------------------------------------------------------------------------|----------|---------------|------------------------------------------------------------|------|-----------|
| Type                                                                                       | Combined | Pre-Requisite | Both WM extremities are equipped with an active HOTDOCK SI |      |           |
| Purpose / Expected Result                                                                  |          |               |                                                            |      |           |
| The WM is able to monitor and control the extremities HOTDOCK SI through the local CAN bus |          |               |                                                            |      |           |
| Procedure                                                                                  |          |               |                                                            |      |           |
| <b>Configuration:</b>                                                                      |          |               |                                                            |      |           |
| - The WM Controller is used to perform the tests, with CAN communication to the HOTDOCK SI |          |               |                                                            |      |           |
| - The WM power bus is connected to a 48V power supply                                      |          |               |                                                            |      |           |
| <b>Procedure:</b>                                                                          |          |               |                                                            |      |           |
| - The operator verifies the CAN communication availability with both HOTDOCK SI            |          |               |                                                            |      |           |
| - The operator verifies the CAN TM from the two HOTDOCK SI                                 |          |               |                                                            |      |           |
| - The operator sends CAN TC to both HOTDOCK SI to validate operation of HOTDOCK:           |          |               |                                                            |      |           |
| - HOTDOCK state update (latching)                                                          |          |               |                                                            |      |           |
| - HOTDOCK power bus switch                                                                 |          |               |                                                            |      |           |
| Covered Requirements                                                                       |          |               |                                                            |      |           |
| IntR_B305 (WM local CAN network)                                                           |          |               |                                                            |      |           |
| FuncR_A105 (Components low level control)                                                  |          |               |                                                            |      |           |
| IntR_B304 bis (WM Interface switch)                                                        |          |               |                                                            |      |           |
| IntR_B307 (WM mechanical interface to SI)                                                  |          |               |                                                            |      |           |

| ID            | CT-A-7                                                                                          |
|---------------|-------------------------------------------------------------------------------------------------|
| Title         | WM Power Transfer                                                                               |
| Type          | Combined                                                                                        |
| Pre-Requisite | Both WM extremities are equipped with an active HOTDOCK SI, which are connected to a passive SI |
| Lead          | SpaceApps                                                                                       |

**Purpose / Expected Result**

A power of 0.5 kW (TBC) can be transferred through the WM

**Procedure**

**Configuration:**  
- The WM Controller is used to perform the tests, with CAN communication to the HOTDOCK SI  
- The WM power bus is connected to a 48V power supply  
- The power transfer interface of the passive HOTDOCK-A is connected to a 48V power supply  
- The power transfer interface of the passive HOTDOCK-B is connected to an electrical load

**Procedure:**  
- The operator switches on the WM power bus

- The operator switches on the 48V power supply

{13}------------------------------------------------

![](_page_13_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 13  
---
Demonstration Prodedures  

| - The operator enables the power relay of the HOTDOCK and verifies the power transfer through the WM. |
|-------------------------------------------------------------------------------------------------------|
| Covered Requirements                                                                                  |
| PerfR_B205 (Power Transfer)                                                                           |

| ID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | CT-A-8   | Title         | WM Start-Up, Initialization and Communication with OBC-S |                                                                                                                                                         |  | Lead | SpaceApps |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|---------------|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|--|------|-----------|
| Type                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Combined | Pre-Requisite |                                                          | Both WM extremities are equipped with an active HOTDOCK SI,<br>which are connected to a passive SI<br>OBC-S interface to WM controller through SpW/RMAP |  |      |           |
| Purpose / Expected Result                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |          |               |                                                          |                                                                                                                                                         |  |      |           |
| The WM is able to get power, start and initialize automatically after power-on, reaching a state ready for communication and<br>operations. The WM Controller is able to provide TM and get TC to/from the OBC-S, through its HOTDOCK SI.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |          |               |                                                          |                                                                                                                                                         |  |      |           |
| Procedure                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |          |               |                                                          |                                                                                                                                                         |  |      |           |
| Configuration:<br>- The OBC-S is connected by SpW to the WM Controller by the SpW bus through SpW bricks and the HOTDOCK SI<br>- The WM power bus is connected to a 48V power supply<br>Procedure:<br>- The power bus is switched ON<br>- The operator verifies on the OBC-S that the SpW communication with the WM controller is enabled<br>- The operator enables the housekeeping TM for the WM through RMAP TC<br>- The operator verifies that the housekeeping TM for the WM is received on the OBC-S<br>- The operator sends TC to the WM through RMAP TC:<br>- WM control commands<br>- WM configurations commands<br>- WM HOTDOCK SI control<br>- The operator verifies the action of the TC (e.g. TM update)<br>The test is repeated with the second extremity of the WM. |          |               |                                                          |                                                                                                                                                         |  |      |           |
| Covered Requirements                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |          |               |                                                          |                                                                                                                                                         |  |      |           |
| FuncR_A108 (Monitoring)<br>FuncR_B107 (WM start and initialization)<br>IntR_B301 (WM TM/TC)<br>IntR_B303 (WM Power)<br>FuncR_A104 (SVC high level control)<br>IntR_B306 (WM local control network)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |          |               |                                                          |                                                                                                                                                         |  |      |           |

{14}------------------------------------------------

![](_page_14_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 14  
---
Demonstration Prodedures  

| ID                                                                                                                                                                                                                                                                                    | CT-A-9   | Title         | WM connection to SVC/CLT HOTDOCK SI |                                                                                                        |  | Lead | SpaceApps |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|---------------|-------------------------------------|--------------------------------------------------------------------------------------------------------|--|------|-----------|
| Type                                                                                                                                                                                                                                                                                  | Combined | Pre-Requisite |                                     | Both WM extremities are equipped with an active HOTDOCK SI<br>Integrated SCV/CLT buses with HOTDOCK SI |  |      |           |
| Purpose / Expected Result                                                                                                                                                                                                                                                             |          |               |                                     |                                                                                                        |  |      |           |
| The WM is able to connect to the SI of the spacecraft mockup, independently through one of its own SI                                                                                                                                                                                 |          |               |                                     |                                                                                                        |  |      |           |
| Procedure                                                                                                                                                                                                                                                                             |          |               |                                     |                                                                                                        |  |      |           |
| Configuration:<br>- The WM Controller is used to perform the tests<br>- The WM power bus is connected to a 48V power supply                                                                                                                                                           |          |               |                                     |                                                                                                        |  |      |           |
| Procedure:<br>- The operator manually aligns one WM HOTDOCK SI to a HOTDOCK SI on the SCV/CLT<br>- The operator commands the WM to connect the WM HOTDOCK SI<br>- The operator validates the good mechanical connection and the continuity connection for the data and power transfer |          |               |                                     |                                                                                                        |  |      |           |
| Covered Requirements                                                                                                                                                                                                                                                                  |          |               |                                     |                                                                                                        |  |      |           |
| FuncR\_B101 (SM Connection)                                                                                                                                                                                                                                                           |


| ID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | CT-A-10  | Title         | WM connection to SM SI                                                                                                                                             |  |  | Lead | SpaceApps |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|--|------|-----------|
| Type                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Combined | Pre-Requisite | Both WM extremities are equipped with an active HOTDOCK SI<br>Integrated SM with HOTDOCK passive SI and R-ICU<br>OBC-S interface to WM controller through SpW/RMAP |  |  |      |           |
| <b>Purpose / Expected Result</b>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |          |               |                                                                                                                                                                    |  |  |      |           |
| The WM is able to connect to the SI of a SM, is able to power                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |          |               |                                                                                                                                                                    |  |  |      |           |
| <b>Procedure</b>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |          |               |                                                                                                                                                                    |  |  |      |           |
| <b>Configuration:</b><br>- The WM Controller is used to perform the tests<br>- The WM power bus is connected to a 48V power supply<br><br><b>Procedure:</b><br>- The SM SI and the WM SI are aligned<br>- The operator commands the WM to connect the WM HOTDOCK SI<br>- The operator validates the good mechanical connection<br>- The operator commands the WM to switch ON the power transfer of the HOTDOCK SI<br>- The operator validates the start-up of the SM<br>- The operator verifies on the OBC-S that the SpW communication with the SM R-ICU is enabled |          |               |                                                                                                                                                                    |  |  |      |           |
| <b>Covered Requirements</b>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |          |               |                                                                                                                                                                    |  |  |      |           |
| FuncR_B101 (SM Connection)<br>IntR_B302 (WM Data Transfer to SM)<br>IntR_B304 (WM Powers Transfer to SM)                                                                                                                                                                                                                                                                                                                                                                                                                                                              |          |               |                                                                                                                                                                    |  |  |      |           |

{15}------------------------------------------------

![](_page_15_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 15  
---
Demonstration Prodedures  

## <span id="page-15-0"></span>**B-HOTDOCK Standard Interface**

| ID            | CT-B-1            |
|---------------|-------------------|
| Title         | HOTDOCK TM and TC |
| Type          | Unitary           |
| Pre-Requisite | N.A.              |
| Lead          | SpaceApps         |

**Purpose / Expected Result**

Validate the TM / TC of HOTDOCK with OBC, through CAN

**Procedure**

**Configuration:**  
- Active HOTDOCK, powered by 24V power supply and controlled by OBC through CAN

**Procedure:**

- Check the reception of the different TM messages (Temperature, encoder position, state, proximity, orientation)
- Send the different TC to HOTDOCK and observe reaction (switch state, Emergency stop)

**Covered Requirements**

FuncR\_D109 (SI Telemetry)

| ID            | CT-B-2                                                                       |
|---------------|------------------------------------------------------------------------------|
| Title         | HOTDOCK Active to Passive Mechanical Connection, power and SpW Data transfer |
| Lead          | SpaceApps                                                                    |
| Type          | Unitary                                                                      |
| Pre-Requisite | N.A.                                                                         |

**Purpose / Expected Result**

An active HOTDOCK is able to connect to a passive HOTDOCK, and transfer power and SpW data

**Procedure**

**Configuration:**  
- Active HOTDOCK, powered by 24V power supply and controlled by OBC through CAN  
- Passive HOTDOCK  
- OBC with CAN and SpW interface (Spw Bricks)

**Procedure:**  
- The Active HOTDOCK is controlled to connect to the passive HOTDOCK  
- The operator validates the good mechanical connection and the conductivity between data/power interface lines  
- The operator measures the connection time  
- The operator tests and validates SpW data transfer through HOTDOCK, evaluate max data transfer  
- The operator tests and validates TM / TC (switch ON/OFF) of the power interface, power transfer through HOTDOCK, and evaluation of max power transfer (with or without power switch)  
- The operator validates the software based over-voltage and over-current protection (through switch off of the power relay of the active interface)  
- The Active HOTDOCK is controlled to disconnect from the passive HOTDOCK

**Covered Requirements**

FuncR\_D103 (Passive coupling)  
FuncR\_D104 (Passive de-coupling)  
FuncR\_D105 (protection)  
FuncR\_D106 (power interface switch)  
FuncR\_D107 (power interface TM)  
PerfR\_D203 (power transfer)  
PerfR\_D204 (data transfer rate)  
PhyR\_D603 (Connection time)

{16}------------------------------------------------

![](_page_16_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 16  
---
Demonstration Prodedures  

| ID            | CT-B-3                    |
|---------------|---------------------------|
| Title         | HOTDOCK Power Consumption |
| Type          | Unitary                   |
| Pre-Requisite | N.A.                      |
| Lead          | SpaceApps                 |

**Purpose / Expected Result**

Measure HOTDOCK power consumption, target <1A under 24V

**Procedure**

**Configuration:**

- Active HOTDOCK, powered by 24V power supply and controlled by OBC through CAN
- Passive HOTDOCK
- OBC with CAN and SpW interface (Spw Bricks)

**Procedure:**

- Measure HOTDOCK power consumption for the different mode of operations
**Covered Requirements**

| PhyR_D602 (Power Consumption) |
|-------------------------------|
|-------------------------------|

| ID            | CT-B-4                 |
|---------------|------------------------|
| Title         | HOTDOCK 90deg symmetry |
| Type          | Unitary                |
| Pre-Requisite | N.A.                   |
| Lead          | SpaceApps              |

**Purpose / Expected Result**

Validate that the HOTDOCK can support connection every 90 degrees (mechanical, data and power)

| <b>Procedure</b>                                                                                                                                                               |  |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|
| <b>Configuration:</b><br>- Active HOTDOCK, powered by 24V power supply and controlled by OBC through CAN<br>- Passive HOTDOCK<br>- OBC with CAN and SpW interface (Spw Bricks) |  |
| <b>Procedure:</b><br>- Test the mechanical connection, data and power transfer successively for each 90 degree rotation                                                        |  |
| <b>Covered Requirements</b>                                                                                                                                                    |  |
| DesR_D402 (90deg. Symmetry)                                                                                                                                                    |  |

| <b>ID</b>            | CT-B-5                      |
|----------------------|-----------------------------|
| <b>Title</b>         | HOTDOCK Mechanical Guidance |
| <b>Lead</b>          | SpaceApps                   |
| <b>Type</b>          | Unitary                     |
| <b>Pre-Requisite</b> | N.A.                        |

**Purpose / Expected Result**

Validate the capability of HOTDOCK Form-Fit to support the self-alignment, under manipulation of a robotic arm

**Procedure**

**Configuration:**  
- HOTDOCK interface connected to robotic arm end-effector (c.f. DLR test)  
- HOTDOCK interface on fixed structure

**Procedure:**

{17}------------------------------------------------

![](_page_17_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 17  
---
Demonstration Prodedures  

- Validate the approach and self-alignment of the two HOTDOCK interfaces, under control of the robotic arm. Evaluate guidance performances (ROA linear, angular) (c.f. DLR tests)

#### **Covered Requirements**

PerfR\_D202 (Mechanical guidance) DesR\_D404 (Mechanical guidance)

| ID                                                                                                                                                                                                                       | CT-B-6  | Title         | HOTDOCK Diagonal Engagement |      | Lead | SpaceApps |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|---------------|-----------------------------|------|------|-----------|
| Type                                                                                                                                                                                                                     | Unitary | Pre-Requisite |                             | N.A. |      |           |
| Purpose / Expected Result                                                                                                                                                                                                |         |               |                             |      |      |           |
| Validate the capability of HOTDOCK to perform diagonal engagement of at least 55 degrees                                                                                                                                 |         |               |                             |      |      |           |
| Procedure                                                                                                                                                                                                                |         |               |                             |      |      |           |
| <b>Configuration:</b><br>- HOTDOCK interface connected to robotic arm end-effector (c.f.DLR test)<br>- HOTDOCK interface on fixed structure                                                                              |         |               |                             |      |      |           |
| <b>Procedure:</b><br>- Validate the diagonal approach and alignment of the two HOTDOCK interfaces, under control of the robotic arm through pre-defined trajectory. Evaluate performances from different approach angles |         |               |                             |      |      |           |
| Covered Requirements                                                                                                                                                                                                     |         |               |                             |      |      |           |
| DesR_D403 (Diagonal Engagement)                                                                                                                                                                                          |         |               |                             |      |      |           |

| <b>ID</b>            | CT-B-7                     |
|----------------------|----------------------------|
| <b>Title</b>         | HOTDOCK Mechanical Loading |
| <b>Lead</b>          | SpaceApps                  |
| <b>Type</b>          | Unitary                    |
| <b>Pre-Requisite</b> | N.A.                       |

**Purpose / Expected Result**

Validate the mechanical loading performance of HOTDOCK for longitudinal force and bending moment

**Procedure**

**Configuration:**  
- Active HOTDOCK mechanically latched to passive HOTDOCK

**Procedure:**  
- Traction test and bending test on the Active/Passive mechanical connection

| <b>Covered Requirements</b>     |
|---------------------------------|
| PerfR_D201 (Mechanical loading) |

{18}------------------------------------------------

![](_page_18_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 18  
---
Demonstration Prodedures  

| ID                                                                                                                                                                                                                                                                                                                                       | CT-B-8   | Title         | HOTDOCK Active to Passive thermal connection and thermal transfer by fluid exchange |  | Lead | MAGSOAR / SpaceApps |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|---------------|-------------------------------------------------------------------------------------|--|------|---------------------|
| Type                                                                                                                                                                                                                                                                                                                                     | Combined | Pre-Requisite | Thermal subsystem                                                                   |  |      |                     |
| Purpose / Expected Result                                                                                                                                                                                                                                                                                                                |          |               |                                                                                     |  |      |                     |
| An active HOTDOCK is able to connect to a passive HOTDOCK through its thermal interface and transfer thermal power                                                                                                                                                                                                                       |          |               |                                                                                     |  |      |                     |
| Procedure                                                                                                                                                                                                                                                                                                                                |          |               |                                                                                     |  |      |                     |
| <b>Configuration:</b><br>- Thermal Active HOTDOCK, powered by 24V power supply and controlled by OBC through CAN<br>- Thermal Passive HOTDOCK<br>- OBC with CAN<br>- Thermal subsystem circuitry connected to each HOTDOCK                                                                                                               |          |               |                                                                                     |  |      |                     |
| <b>Procedure:</b><br>- The Active HOTDOCK is controlled to connect to the passive HOTDOCK<br>- The operator validates the good mechanical connection<br>- The operator tests and validates the thermal transfer by fluid exchange (through control of the thermal subsystem components), evaluation of the thermal transfer performances |          |               |                                                                                     |  |      |                     |
| Covered Requirements                                                                                                                                                                                                                                                                                                                     |          |               |                                                                                     |  |      |                     |
| FuncR_D103 (Passive coupling)<br>FuncR_D104 (Passive de-coupling)<br>PerfR_D205 (Thermal transfer performance)                                                                                                                                                                                                                           |          |               |                                                                                     |  |      |                     |

{19}------------------------------------------------

![](_page_19_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 19  
---
Demonstration Prodedures  

### <span id="page-19-0"></span>**Spacecraft Modules and Components**

| ID            | CT-C-1     |
|---------------|------------|
| Title         | SMs Weight |
| Type          | Unitary    |
| Pre-Requisite | N.A.       |
| Lead          | SITAEL     |

**Purpose / Expected Result**Measure the weight of the different mobile SMs

**Procedure***Procedure:*

- Measure the weight of the different mobile SMs

**Covered Requirements**PhyR\_C501 (SM Weight)

#### <span id="page-19-1"></span>**cPDU**

| ID            | CT-C-2                 |
|---------------|------------------------|
| Title         | cPDU DC/DC conversions |
| Type          | Unitary                |
| Pre-Requisite | Thermal subsystem      |
| Lead          | SpaceApps              |

**Purpose / Expected Result**

The cPDU is able to provide required voltage (24V, 12V) from the main 48V bus

**Procedure**

*Configuration:*

- cPDU, powered by 48V

*Procedure:*

- The cPDU is powered ON

- The different DC/DC conversion voltages are validated

**Covered Requirements**

Required function

| ID                                                                                                                                                                                                                                                                                                            | CT-C-3  | Title         | cPDU TM and TC, power routing control | Lead | SpaceApps |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|---------------|---------------------------------------|------|-----------|
| Type                                                                                                                                                                                                                                                                                                          | Unitary | Pre-Requisite | Thermal subsystem                     |      |           |
| Purpose / Expected Result                                                                                                                                                                                                                                                                                     |         |               |                                       |      |           |
| The cPDU is able to re-route power on different ports                                                                                                                                                                                                                                                         |         |               |                                       |      |           |
| Procedure                                                                                                                                                                                                                                                                                                     |         |               |                                       |      |           |
| <b>Configuration:</b><br>- cPDU, powered by 48V<br>- OBC with CAN interface, connected to cPDU<br>- Power supply connected to one input port of the cPDU                                                                                                                                                      |         |               |                                       |      |           |
| <b>Procedure:</b><br>- The cPDU is powered ON and the CAN communication is confirmed with the OBC<br>- Reception of CAN TM is validated<br>- CAN messages are sent to switch ON/OFF the other port of the cPDU (power re-distribution)<br>- CAN messages are sent to switch ON/OFF the DC/DC lines (12V, 24V) |         |               |                                       |      |           |
| Covered Requirements                                                                                                                                                                                                                                                                                          |         |               |                                       |      |           |
| FuncR_C104 bis (SM Power routing)<br>FuncR_C106 (SM switch ON/OFF)                                                                                                                                                                                                                                            |         |               |                                       |      |           |

{20}------------------------------------------------

![](_page_20_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 20  
---
Demonstration Prodedures  

### <span id="page-20-0"></span>**R-ICU / FMC Board**

| ID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | CT-D-1  | Title         | R-ICU SpW Routing                                | Lead | TAS-UK |  |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|---------------|--------------------------------------------------|------|--------|--|
| Type                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Unitary | Pre-Requisite | R-ICU/FMC Board<br>SpW Brick interfaced to R-ICU |      |        |  |
| Purpose / Expected Result                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |         |               |                                                  |      |        |  |
| The R-ICU and FMC board are able to transfer and route SpW data between different nodes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |         |               |                                                  |      |        |  |
| Procedure                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |         |               |                                                  |      |        |  |
| Configuration:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |         |               |                                                  |      |        |  |
| - SpW Brick connected to PC to represent OBC<br>- SpW Brick connected to R-ICU A<br>- R-ICU A connected to R-ICU B via SpW                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |         |               |                                                  |      |        |  |
| Procedure:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |         |               |                                                  |      |        |  |
| - R-ICUs are powered on<br>- R-ICU SpW IDs and router tables initialised to represent the test topology<br>- OBC writes data using RMAP to R-ICU A using SpW path addressing<br>- OBC checks for successful RMAP reply from R-ICU A<br>- OBC writes data using RMAP to R-ICU B using SpW path addressing<br>- OBC checks for successful RMAP reply from R-ICU B<br><br>- OBC writes data using RMAP to R-ICU A using SpW logical addressing<br>- OBC checks for successful RMAP reply from R-ICU A<br>- OBC writes data using RMAP to R-ICU B using SpW logical addressing<br>- OBC checks for successful RMAP reply from R-ICU B<br><br>- OBC performs continuous RMAP writes to R-ICU A to determine SpW throughput and RMAP write performance without TMTC handling present on the R-ICU<br>- OBC performs continuous RMAP reads to R-ICU A to determine SpW throughput and RMAP read performance without TMTC handling present on the R-ICU<br>- OBC performs continuous RMAP writes to R-ICU B to verify effect of SpW router latency on RMAP performance |         |               |                                                  |      |        |  |
| Covered Requirements                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |               |                                                  |      |        |  |
| PerfR_A201 (Sub-systems TM/TC data rate)<br>FuncR_C103 (SM data routing)<br>FuncR_C104 (SM data transmission)<br>FuncR_C105 (SM redundancy)<br>FuncR_D108 (Data Interface Support)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |         |               |                                                  |      |        |  |

| ID                                                                                                                                                               | CT-D-2  | Title         | R-ICU TMTC Handling                                                             |  | Lead | TAS-UK |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|---------------|---------------------------------------------------------------------------------|--|------|--------|
| Type                                                                                                                                                             | Unitary | Pre-Requisite | R-ICU/FMC Board<br>SpW Brick interfaced to R-ICU running OBC RMAP TMTC software |  |      |        |
| Purpose / Expected Result                                                                                                                                        |         |               |                                                                                 |  |      |        |
| Validate the RMAP TMTC and evaluate performance. OBC should be able to command R-ICU using RMAP telecommands<br>and read status information using RMAP telemetry |         |               |                                                                                 |  |      |        |
| Procedure                                                                                                                                                        |         |               |                                                                                 |  |      |        |
| Configuration:<br>- SpW Brick connected to PC to represent OBC                                                                                                   |         |               |                                                                                 |  |      |        |

{21}------------------------------------------------

![](_page_21_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 21  
---
Demonstration Prodedures  

- SpW Brick connected to R-ICU A

- UART cable connected to R-ICU A

#### Procedure:

-R-ICUs are powered on

-R-ICU SpW IDs and router tables initialised to represent the test topology

-R-ICU TMTC handling task and R-ICU control task are started

-OBC issues each R-ICU TC in turn and effects are verified through physical inspection (LEDs) or from UART output -OBC issues each R-ICU TM in turn and returned values are displayed for verification by cross check with the R-ICUs current state (physical inspection or UART output)

### **Covered Requirements**

PerfR\_A201 (Sub-systems TM/TC data rate) PerfR\_A202 (Sub-systems services data rate) PerfR\_C201 (SM data interface rate for TM/TC) PerfR\_C202 (SM data interface rate for service data) PerfR\_B204 (WMdata interface rate for service data)

PerfR\_B203 (WMdata interface rate for TM/TC)

| ID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | CT-D-3  | Title         | R-ICU TMTC Error Handling                                                         | Lead | TAS-UK |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|---------------|-----------------------------------------------------------------------------------|------|--------|
| Type                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Unitary | Pre-Requisite | R-ICU / FMC Board<br>SpW Brick interfaced to R-ICU running OBC RMAP TMTC software |      |        |
| Purpose / Expected Result                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |         |               |                                                                                   |      |        |
| A corrupted TMTC packet should not cause the TMTC handling to fail in such a way that affects the operation of the R-ICU or OBC TMTC software or stalls the network                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |         |               |                                                                                   |      |        |
| Procedure                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |         |               |                                                                                   |      |        |
| Configuration:<br>- SpW Brick connected to PC to represent OBC<br>- SpW Brick connected to R-ICU A<br>- R-ICU A connected to R-ICU B via SpW                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |         |               |                                                                                   |      |        |
| Procedure:<br>- R-ICUs are powered on<br>- R-ICU SpW IDs and router tables initialised to represent the test topology<br>- R-ICU TMTC handling task and R-ICU control task are started<br>- R-ICU A is set up to inject faults into RMAP header and data as the RMAP packet is routed.<br><br>- OBC issues TC requests to R-ICU B. R-ICU A injects a fault into the RMAP header.<br>- OBC should receive RMAP reply indicating CRC error in RMAP header<br><br>- OBC issues TC requests to R-ICU B. R-ICU A injects a fault into the RMAP data.<br>- OBC should receive RMAP reply indicating CRC error in RMAP data<br><br>- OBC issues TM requests to R-ICU B. R-ICU A injects a fault into the RMAP reply.<br>- OBC should receive RMAP reply indicating CRC error in RMAP reply<br><br>- OBC issues TC requests with invalid logical address<br>- R-ICU A should spill the packet and notify R-ICU that invalid SpW logical address was detected |         |               |                                                                                   |      |        |

{22}------------------------------------------------

![](_page_22_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 22  
---
Demonstration Prodedures  

- R-ICU B locks a TM memory area but does not release the lock

-OBC issues TM request to this memory area

-After timeout period, OBC should receive RMAP reply indicating NOT AUTHORISED error in RMAP header

**Covered Requirements**

FuncR\_D108 (Data Interface Support)

| ID                                                                                                                         | CT-D-4                           | Title         | R-ICU Component SW API | Lead                                                                                                    | TAS-UK |  |
|----------------------------------------------------------------------------------------------------------------------------|----------------------------------|---------------|------------------------|---------------------------------------------------------------------------------------------------------|--------|--|
| Type                                                                                                                       | Unitary                          | Pre-Requisite |                        | R-ICU / FMC Board<br>SpW Brick interfaced to R-ICU running OBC RMAP TMTC software<br>CAN test interface |        |  |
| Purpose / Expected Result                                                                                                  |                                  |               |                        |                                                                                                         |        |  |
| R-ICU TMTC handling and CAN drivers need to support multiple R-ICU software drivers using these interface simultaneously   |                                  |               |                        |                                                                                                         |        |  |
| Configuration                                                                                                              |                                  |               |                        |                                                                                                         |        |  |
| - SpW Brick connected to PC to represent OBC<br>- SpW Brick connected to R-ICU A<br>- R-ICU A connected to R-ICU B via SpW |                                  |               |                        |                                                                                                         |        |  |
| Procedure                                                                                                                  |                                  |               |                        |                                                                                                         |        |  |
| Covered Requirements                                                                                                       |                                  |               |                        |                                                                                                         |        |  |
|                                                                                                                            | IntR_C303 (SM R-ICU to SI TM/TC) |               |                        |                                                                                                         |        |  |

| ID            | CT-D-5                                                                          |
|---------------|---------------------------------------------------------------------------------|
| Title         | R-ICU Network Discovery and Configuration                                       |
| Type          | Unitary                                                                         |
| Pre-Requisite | R-ICU / FMC Board, SpW Brick interfaced to R-ICU running OBC RMAP TMTC software |
| Lead          | TAS-UK                                                                          |

**Purpose / Expected Result**

The OBC is able to read the SpW PnP information fields and this information represents the state of the network. OBC is able to configure the R-ICU routing tables.

**Configuration:**

- SpW Brick connected to PC to represent OBC
- SpW Brick connected to R-ICU A
- R-ICU A connected to R-ICU B via SpW

**Procedure:**

- R-ICUs are powered on
- R-ICU SpW IDs are set as per spacecraft configuration. Routing table entries are reset to NULLs
- R-ICU TMTC handling task is started

{23}------------------------------------------------

![](_page_23_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 23  
---
Demonstration Prodedures  

| -OBC issues SpW PnP: network information read TM request to R-ICU A SpW ID.                    |
|------------------------------------------------------------------------------------------------|
| -OBC should receive network status information of router of R-ICU A                            |
| -OBC issues SpW PnP: application information read TM request to R-ICU A SpW ID.                |
| -OBC should receive information about the components connected to the R-ICU A                  |
| -OBC uses network information field and SpW path addressing to request SpW PnP TM from R-ICU B |
| -OBC should receive network status information of router of R-ICU B                            |
| -OBC issues SpW PnP: application information read TM request to R-ICU B SpW ID.                |
| -OBC should receive information about the components connected to the R-ICU B                  |
| -OBC issues routing table set TC to R-ICU A to set up the path to R-ICU B                      |
| -OBC issues TM request to R-ICU B using SpW logical addressing                                 |
| -OBC should receive R-ICU B TM                                                                 |
| Covered Requirements                                                                           |
| FuncR_A111 (Modules Plug & Play detection)                                                     |
| FuncR_C105 (SM redundancy)                                                                     |
| FuncR_C108 (Identification Information)                                                        |
| FuncR_D108 (Data Interface Support)                                                            |
| DesR_A407 (Data Network)                                                                       |

| ID                                                                                                                                                                                                                                                                                                                                                                                                                                                         | CT-D-6   | Title         | Camera Rendering through SpW to OBC-C                                                           |  |  | Lead | TAS-UK |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|---------------|-------------------------------------------------------------------------------------------------|--|--|------|--------|
| Type                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Combined | Pre-Requisite | R-ICU / FMC Board<br>I3DS Framework<br>ZED Camera<br>OBC-C interfaced to R-ICU through SpW/RMAP |  |  |      |        |
| Purpose / Expected Result                                                                                                                                                                                                                                                                                                                                                                                                                                  |          |               |                                                                                                 |  |  |      |        |
| The R-ICU is able to interface the ZED Camera and transmit picture data to the OBC-C                                                                                                                                                                                                                                                                                                                                                                       |          |               |                                                                                                 |  |  |      |        |
| Procedure                                                                                                                                                                                                                                                                                                                                                                                                                                                  |          |               |                                                                                                 |  |  |      |        |
| Configuration:<br>- SpW Brick connected to PC to represent OBC<br>- SpW Brick connected to R-ICU<br>- ZED Camera attached to R-ICU<br>- UART cable connected to R-ICU                                                                                                                                                                                                                                                                                      |          |               |                                                                                                 |  |  |      |        |
| Procedure:<br>- R-ICUs are powered on<br>- R-ICU SpW IDs and router tables initialised to represent the test topology<br>- R-ICU TMTC handling task and R-ICU control task are started<br>- I3DS framework initialises and connects to Zed Camera<br>- OBC issues TC to configure Zed camera.<br>- Confirmation of Zed camera settings should be present on R-ICU UART<br>- OBC issues TM to read Zed camera frame.<br>- OBC should receive the image data |          |               |                                                                                                 |  |  |      |        |

{24}------------------------------------------------

![](_page_24_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 24  
---
Demonstration Prodedures  

-OBC polls Zed camera status TM and fetches frame TM if available -Optical payload maximum rate over the SpW network can be established

#### **Covered Requirements**

DesR\_A404 (OG4 Reuse)

PerfR\_A202 (Sub-systems services data rate)

PerfR\_C202 (SM data interface rate for service data)

| ID                                                                                                                                                                                                                                                                                                                                                                                             | CT-D-7   | Title         | SM Power On and TM to OBC-S                                             |  |  | Lead | TAS-UK |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|---------------|-------------------------------------------------------------------------|--|--|------|--------|
| Type                                                                                                                                                                                                                                                                                                                                                                                           | Combined | Pre-Requisite | R-ICU / FMC Board<br>cPDU<br>OBC-S interfaced to R-ICU through SpW/RMAP |  |  |      |        |
| Purpose / Expected Result                                                                                                                                                                                                                                                                                                                                                                      |          |               |                                                                         |  |  |      |        |
| The SM is able to start and initialize automatically after power-on, reaching a state ready for communication and operations'                                                                                                                                                                                                                                                                  |          |               |                                                                         |  |  |      |        |
| Procedure                                                                                                                                                                                                                                                                                                                                                                                      |          |               |                                                                         |  |  |      |        |
| <b>Configuration:</b><br>- cPDU, connected to switchable 48V power supply<br>- cPDU connected to R-ICU by CAN<br>- R-ICU connected to OBC-S through SpW / RMAP<br><br><b>Procedure:</b><br>- The cPDU is powered ON from power supply<br>- The start-up of the cPDU, R-ICU and good initialization are confirmed on the OBC-S via TM<br>- The reception of TM from R-ICU is validated on OBC-S |          |               |                                                                         |  |  |      |        |
| Covered Requirements                                                                                                                                                                                                                                                                                                                                                                           |          |               |                                                                         |  |  |      |        |
| FuncR_C107 (SM Start and initialization)<br>FuncR_C108 (Identification information)<br>FuncR_C109 (Status and fault detection)                                                                                                                                                                                                                                                                 |          |               |                                                                         |  |  |      |        |

#### <span id="page-24-0"></span>**Battery Subsystem**

| ID                                                                                                                                                                                                                                                                                                                                                              | CT-E-1  | Title         | Battery subsystem TM / TC | Lead | SpaceApps |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|---------------|---------------------------|------|-----------|
| Type                                                                                                                                                                                                                                                                                                                                                            | Unitary | Pre-Requisite | N.A.                      |      |           |
| Purpose / Expected Result                                                                                                                                                                                                                                                                                                                                       |         |               |                           |      |           |
| The battery subsystem can be interfaced to OBC through CAN communication                                                                                                                                                                                                                                                                                        |         |               |                           |      |           |
| Procedure                                                                                                                                                                                                                                                                                                                                                       |         |               |                           |      |           |
| Configuration:<br>- Battery subsystem powered by 24V/48V power supply<br>- OBC with CAN interface, connected to battery subsystem controller<br><br>Procedure:<br>- The battery subsystem is powered ON<br>- The CAN communication between the battery subsystem and the OBC is confirmed<br>- Validation of TM and TC with the battery subsystem, from the OBC |         |               |                           |      |           |
| Covered Requirements                                                                                                                                                                                                                                                                                                                                            |         |               |                           |      |           |

{25}------------------------------------------------

![](_page_25_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 25  
---
Demonstration Prodedures  

Required function

| ID            | CT-E-2                                   |
|---------------|------------------------------------------|
| Title         | Battery subsystem charging / discharging |
| Lead          | SpaceApps                                |
| Type          | Unitary                                  |
| Pre-Requisite | N.A.                                     |

**Purpose / Expected Result**

The battery subsystem can be charged and discharged

**Procedure**

**Configuration:**  
- Battery subsystem powered by 24V/48V power supply  
- Power supply to charge and electrical load to discharge, connected to the battery subsystem  
- OBC with CAN interface, connected to battery subsystem controller

**Procedure:**  
- The battery subsystem is powered ON  
- The CAN communication between the battery subsystem and the OBC is confirmed  
- Control of the battery subsystem through CAN command to charge/discharge the battery, validation by TM

**Covered Requirements**

Required function

#### <span id="page-25-0"></span>**Thermal Subsystem**

| ID                        | CT-F-1     | Title     | Thermal IF performance                                                                                                                                                                                                                                                                                                                                                      |      | Lead | MAG SOAR |
|---------------------------|------------|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------|------|----------|
| Type                      | Unitary    |           | Pre-Requisite                                                                                                                                                                                                                                                                                                                                                               | N.A. |      |          |
| Purpose / Expected Result |            |           | The standard interface shall provide a thermal interface to allow active transfer of thermal flow between two Spacecraft Modules The thermal interface shall allow a thermal flow rating of 2500 W The thermal interface shall enable thermal connection to the thermal module sub-system The pressure drop of the thermal IF will be quantified for different liquid flows |      |      |          |
| Configuration             |            |           | Hot site connected to thermal IF Cold site connected to thermal IF                                                                                                                                                                                                                                                                                                          |      |      |          |
| Procedure                 |            |           | The thermal IFs are mechanically linked Temperature sensors are implemented on input and output of the hot site Temperature sensors are implemented on input and output of the cold site Pressure sensors are implemented in the hydraulic circuit <b>These tests will be carried out at MAG SOAR facilities</b>                                                            |      |      |          |
| Covered Requirements      |            |           |                                                                                                                                                                                                                                                                                                                                                                             |      |      |          |
| FuncR_D102                | PerfR_D205 | IntR_D303 |                                                                                                                                                                                                                                                                                                                                                                             |      |      |          |

{26}------------------------------------------------

![](_page_26_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 26  
---
Demonstration Prodedures  

| ID                                                                                                                                                                                                                                                                                             | CT-F-2  | Title         | Demonstration of heat transfer in the thermal subsystem<br>(250 W) |  | Lead | MAG SOAR |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|---------------|--------------------------------------------------------------------|--|------|----------|
| Type                                                                                                                                                                                                                                                                                           | Unitary | Pre-Requisite | N.A.                                                               |  |      |          |
| Purpose / Expected Result                                                                                                                                                                                                                                                                      |         |               |                                                                    |  |      |          |
| • Demonstrate the capability of the thermal subsystem to transfer 250 W                                                                                                                                                                                                                        |         |               |                                                                    |  |      |          |
| Procedure                                                                                                                                                                                                                                                                                      |         |               |                                                                    |  |      |          |
| <b>Configuration:</b><br>- The thermal subsystem is closed and allow close loop circulation                                                                                                                                                                                                    |         |               |                                                                    |  |      |          |
| <b>Procedure:</b><br>- The thermal IFs are mechanically linked<br>- Temperature sensors are located in the input and output of the fan pipes<br>- Temperature sensors are located in the input and output of the heat generator<br>- Pressure sensors are implemented in the hydraulic circuit |         |               |                                                                    |  |      |          |
| Covered Requirements                                                                                                                                                                                                                                                                           |         |               |                                                                    |  |      |          |
| PerfR_D205                                                                                                                                                                                                                                                                                     |


| ID                                                                              | CT-F-3  | Title         | Demonstration of non-leakage strategy |  |  | Lead | MAG SOAR |
|---------------------------------------------------------------------------------|---------|---------------|---------------------------------------|--|--|------|----------|
| Type                                                                            | Unitary | Pre-Requisite | N.A.                                  |  |  |      |          |
| Purpose / Expected Result                                                       |         |               |                                       |  |  |      |          |
| Demonstrate the non-leakage control strategy proposed for the thermal subsystem |         |               |                                       |  |  |      |          |
| Procedure                                                                       |         |               |                                       |  |  |      |          |
| Configuration:                                                                  |         |               |                                       |  |  |      |          |
| - The thermal subsystem is closed and allow close loop circulation              |         |               |                                       |  |  |      |          |
| Procedure:                                                                      |         |               |                                       |  |  |      |          |
| - The thermal IFs are mechanically linked                                       |         |               |                                       |  |  |      |          |
| - Temperature sensors are implemented on input and output of the heat exchanger |         |               |                                       |  |  |      |          |
| - Temperature sensors are implemented on input and output of the cooler         |         |               |                                       |  |  |      |          |
| - Pressure sensors are implemented in the hydraulic circuit                     |         |               |                                       |  |  |      |          |
| - Transparent pipes will allow visual inspection of the fluid along the line    |         |               |                                       |  |  |      |          |
| Covered Requirements                                                            |         |               |                                       |  |  |      |          |
| Required function                                                               |         |               |                                       |  |  |      |          |

| ID                                                                                                               | CT-F-4  | Title | Orbital pump failure operation |      |  | Lead | MAG SOAR |
|------------------------------------------------------------------------------------------------------------------|---------|-------|--------------------------------|------|--|------|----------|
| Type                                                                                                             | Unitary |       | Pre-Requisite                  | N.A. |  |      |          |
| Purpose / Expected Result                                                                                        |         |       |                                |      |  |      |          |
| Demonstrate that after a hypothetical pump failure on orbit, the redundant pump can manage the power transferred |         |       |                                |      |  |      |          |
| Procedure                                                                                                        |         |       |                                |      |  |      |          |
| Configuration:                                                                                                   |         |       |                                |      |  |      |          |

{27}------------------------------------------------

![](_page_27_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 27  
---
Demonstration Prodedures  

| - The thermal subsystem is closed and allow close loop circulation                                                                                                                                                                                                                                                                                                          |                   |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| <b>Procedure:</b><br>- The thermal IFs are mechanically linked<br>- Temperature sensors are implemented on input and output of the heat exchanger<br>- Temperature sensors are implemented on input and output of the cooler<br>- Pressure sensors are implemented in the hydraulic circuit<br>- Transparent pipes will allow visual inspection of the fluid along the line |                   |
| Covered Requirements                                                                                                                                                                                                                                                                                                                                                        | Required function |

{28}------------------------------------------------

![](_page_28_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 28  
---
Demonstration Prodedures  

### <span id="page-28-0"></span>**Design and Simulator Tools**

| ID                                                                                                                                                                                                                                                                                                                                                                                                                               | CT-G-1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Title         | Design and Simulation tool procedure                                                         |  | Lead | DLR |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|----------------------------------------------------------------------------------------------|--|------|-----|
| Type                                                                                                                                                                                                                                                                                                                                                                                                                             | Pre-integrated                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Pre-Requisite | - Full parameter files for scenario and components<br>-WM controller and trajectory planner. |  |      |     |
| Purpose / Expected Result                                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |               |                                                                                              |  |      |     |
| The Design tool will check the scenario and important parameters for validity. The FES simulator will simulate the whole scenario and generate data plots and data results for further analysis.                                                                                                                                                                                                                                 |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |               |                                                                                              |  |      |     |
| Procedure                                                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |               |                                                                                              |  |      |     |
| Configuration:                                                                                                                                                                                                                                                                                                                                                                                                                   | - Set parameter files for components and scenario<br>- Initialize full setup of FES, WM controller and Trajectory planner                                                                                                                                                                                                                                                                                                                                                                                                                                |               |                                                                                              |  |      |     |
| Procedure:                                                                                                                                                                                                                                                                                                                                                                                                                       | - Start design toll form MATLAB/ Simulink<br>- Wait until analysis is finished.<br>- Check Design Toll log file for warnings and errors<br>- If everything is ok run full FES simulation, otherwise adjust parameters and/or scenario<br>- Run trajectory planner with the desired trajectory it will send commands to the WM controller which will communicate with the FES<br>- Wait until simulation is finished.<br>- Run evaluation Matlab script to generate data files and plots for the simulation<br>- Analyse the simulator outputs and plots, |               |                                                                                              |  |      |     |
| Covered Requirements                                                                                                                                                                                                                                                                                                                                                                                                             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |               |                                                                                              |  |      |     |
| FuncR_E104 (Task Planning and Simulation)<br>FuncR_E106 (Simulation of Reconfiguration)<br>FuncR_E109 (Manipulator Dynamics Simulation)<br>PerfR_E201 (Simulation Real-Time Performance)<br>PerfR_E202 (Number of SM in Simulation)<br>IntR_E301(Simulator Input Interfaces)<br>IntR_E302 (Simulator Output Interfaces)<br>IntR_E303 (Simulator Communication Interface)<br>IntR_E304 (Generation of plan for onboard execution) |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |               |                                                                                              |  |      |     |

{29}------------------------------------------------

![](_page_29_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 29  
---
Demonstration Prodedures  

### <span id="page-29-0"></span>**Planner and Agent**

| ID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | CT-H-1         | Title         | On-ground plan calculation (display driver)                                            |  |  | Lead | GMV |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|---------------|----------------------------------------------------------------------------------------|--|--|------|-----|
| Type                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Pre-integrated | Pre-Requisite | - Agent CFG files (agent and timelines).<br>- Planner PDDL model (problem and domain). |  |  |      |     |
| Purpose / Expected Result                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |                |               |                                                                                        |  |  |      |     |
| ERGO Agent will run perform a plan in E4 autonomy level using PUS Console and display driver. This plan will be saved and re-run using E3 autonomy level.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |                |               |                                                                                        |  |  |      |     |
| Procedure                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |                |               |                                                                                        |  |  |      |     |
| Configuration:<br>- Initialize PUS Console<br>- Initialize Agent in E4 autonomy level with Functional compiled with the Display RARM driver<br><br>Procedure:<br>- Send planner goal using PUS Service 200.<br>- An E4 plan is generated and executed.<br>- Wait until plan is finished.<br>- Reinitialize all the components to repeat with the generated goal in E3.<br>- Configure Agent to run in E3 autonomy level using Service 200.<br>- Send E3 plan goal using Service 23 and 200. Uploads and run previous plan.<br>- Wait until the same plan finishes.<br>- Check that same plan is executed following the same operation order. |                |               |                                                                                        |  |  |      |     |
| Covered Requirements                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                |               |                                                                                        |  |  |      |     |
| FuncR_A103<br>DesR_A401<br>DesR_A402<br>IntR_E304<br>FuncR_F105<br>FuncR_F106<br>IntR_F301<br>DesR_F401<br>ConfR_F801                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                |               |                                                                                        |  |  |      |     |

{30}------------------------------------------------

![](_page_30_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 30  
---
Demonstration Prodedures  

### <span id="page-30-0"></span>**MCC and PUS Service**

| ID            | CT-I-1             |
|---------------|--------------------|
| Title         | SW Reconfiguration |
| Type          | Pre-integrated     |
| Pre-Requisite | N/A                |
| Lead          | GMV                |

**Purpose / Expected Result**

OBC shall be able to enable and disable come on-board functions from SMs doing a re-configuration process.

**Procedure**
**Configuration:**

- Initialize PUS Console

- Define several reconfiguration modes enabling/disabling different SMs

**Procedure:**

- Use PUS Service 220 to set a reconfiguration mode.

- Using dummy "prints" to show the enable/disable status of each SM-XX.

- Check housekeeping parameters values for each SM to check the status flags.

**Covered Requirements**

FuncR\_A111

IntR\_A304

DesR\_A401

FuncR\_F101

ConfR\_F801

ConfR\_F802

| <b>ID</b>            | CT-I-2                    |
|----------------------|---------------------------|
| <b>Title</b>         | PUS-RMAP commanding chain |
| <b>Lead</b>          | GMV                       |
| <b>Type</b>          | Pre-integrated            |
| <b>Pre-Requisite</b> | N/A                       |

**Purpose / Expected Result**

PUS to command via RMAP and get TMs from dummy R-ICU functionality.

**Procedure**

**Configuration:**

- Initialize Image viewer
- TASTE simplified module

**Procedure:**

- Use PUS Service 210 to send TCs via RMAP to p.e. turn on a LED
- Check via Housekeeping (Service 3) different parameters requested to R-ICU are shown in PUS Console
- Check in PUS console that parameters acquired via RMAP are as expected

**Covered Requirements**

- FuncR\_A112
- DesR\_A401
- FuncR\_F102
- FuncR\_F103
- IntR\_F301

{31}------------------------------------------------

![](_page_31_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 31  
---
Demonstration Prodedures  

| ID            | CT-I-3             |
|---------------|--------------------|
| Title         | Camera acquisition |
| Type          | Pre-integrated     |
| Pre-Requisite | N/A                |
| Lead          | GMV                |

**Purpose / Expected Result**

SM-OSP using SPW driver is able to get a dummy image from the R-ICU and send it to ground via ZeroMQ using I3DS framework.

**Procedure**

**Configuration:**

- Initialize Image viewer
- TASTE simplified module
- Launch an I3DS address server in the MCC and the Client.

**Procedure:**

- R-ICU will generate dummy images
- Use PUS Service 210 to request an image. Via RMAP a dummy image will be read from R-ICU
- Requested image will be sent to ground using a publisher integrated in an I3DS node deployed in the Client through ZeroMQ protocol and received by a subscriber instantiated in ground and showed in a viewer tool

**Covered Requirements**

- FuncR\_A108
- FuncR\_F102
- FuncR\_F103
- FuncR\_F104
- IntR\_F301

{32}------------------------------------------------

![](_page_32_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 32  
---
Demonstration Prodedures  

### <span id="page-32-0"></span>**Visual Subsystem**

| ID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | VSA1.1               | Title         | Detection of simple cube object                                                                                                                                                                                                                                        | Lead | USTRATH |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------|---------|
| Type                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Software Integration | Pre-Requisite | The source stereo camera has been calibrated and camera calibration parameters are known,<br>The disparity computation has been calibrated and good reconstruction parameters are known.<br>Good algorithm parameters are known as result of previous experimentation. |      |         |
| Purpose / Expected Result                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |                      |               |                                                                                                                                                                                                                                                                        |      |         |
| A 3D reconstruction of the camera observed scene is visible in the output. If there are modules in the scene, these are detected<br>and their models are visible in the output. Any damage is also detected and is visible in the output by means of bounding boxes<br>around the region of anomaly. For each detected area of anomaly, a measure of the anomaly as average point-to-model distance is available; this is close to the real predicted damage. Processing time is also available.                                                |                      |               |                                                                                                                                                                                                                                                                        |      |         |
| Procedure                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |                      |               |                                                                                                                                                                                                                                                                        |      |         |
| Configuration:<br>- Print two 3D cubes (about same size as the spacecraft module), a undamaged ideal one, and a damaged one, with 1cm<br>average surface error on one face;<br>- Take two pictures from the stereo camera;<br>- Write down a DFPC configuration file.<br><br>Procedure:<br>- Execute a step-by-step integration test for DFPC instance 1.1 using a single model in input.<br>- Advance through the software steps until the final output is displayed.<br>- Take note of the detected anomaly, and the reported measured error. |                      |               |                                                                                                                                                                                                                                                                        |      |         |
| Inputs                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |                      |               |                                                                                                                                                                                                                                                                        |      |         |
| VSA1.1.1. Picture of a scene which does not contain any cube object;<br>VSA1.1.2 Pictures of a scene which contains the 3D printed undamaged cube within the shared view of the cameras;<br>VSA1.1.3 Pictures of a scene which contains the 3D printed damaged cube within the shared view of the cameras.<br><br>Covered Requirements<br>Surface Anomaly Detection of Spacecraft Modules<br>Surface Anomaly Detection of Walking Manipulator                                                                                                   |                      |               |                                                                                                                                                                                                                                                                        |      |         |

| ID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | VSA1.2         | Title                                                                                                                                                                                                                                                                                   | Detection of simple cube objects | Lead | USTRATH |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------|------|---------|
| Type                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Pre-integrated | Pre-Requisite                                                                                                                                                                                                                                                                           |                                  |      |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |                | The source stereo camera has been calibrated and camera<br>calibration parameters are known,<br><br>The disparity computation has been calibrated and good<br>reconstruction parameters are known.<br><br>Good algorithm parameters are known as result of previous<br>experimentation. |                                  |      |         |
| Purpose / Expected Result                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |                |                                                                                                                                                                                                                                                                                         |                                  |      |         |
| A 3D reconstruction of the camera observed scene is visible in the output. If there are modules in the scene, these are<br>detected and their models are visible in the output. Any damage is also detected and is visible in the output by means of<br>bounding boxes around the region of anomaly. For each detected area of anomaly, a measure of the anomaly as average<br>point-to-model distance is available, this is close to the real predicted damage. Processing time is also available. |                |                                                                                                                                                                                                                                                                                         |                                  |      |         |
| Procedure                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |                |                                                                                                                                                                                                                                                                                         |                                  |      |         |
| Configuration:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                |                                                                                                                                                                                                                                                                                         |                                  |      |         |
| - Print two 3D cubes (about same size as the spacecraft module),, a undamaged ideal one, and a damaged one, with 1cm<br>average surface error on one face;                                                                                                                                                                                                                                                                                                                                          |                |                                                                                                                                                                                                                                                                                         |                                  |      |         |

{33}------------------------------------------------

![](_page_33_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 33  
---
Demonstration Prodedures  

- Take two pictures from the stereo camera;

- Write down a DFPC configuration file.

Procedure:

- Execute a step-by-step integration test for DFPC instance 1.2 using a single model in input.
- Advance through the software steps until the final output is displayed.
- Take note of the detected anomaly, and the reported measured error.

Inputs

VSA1.2.1 Pictures of a scene which contains both 3D printed cubes within the shared view of the cameras.

**Covered Requirements**

Surface Anomaly Detection of Spacecraft Modules Surface Anomaly Detection of Walking Manipulator

| ID                                                                                                                                                                                                                                                                                                                                                                                                                                             | VSA1.3         | Title         | Detection of simple cube-like objects | Lead                                                                                                                                                                                                                                                                   | USTRATH |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|---------------|---------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| Type                                                                                                                                                                                                                                                                                                                                                                                                                                           | Pre-integrated | Pre-Requisite |                                       | The source stereo camera has been calibrated and camera calibration parameters are known,<br>The disparity computation has been calibrated and good reconstruction parameters are known.<br>Good algorithm parameters are known as result of previous experimentation. |         |
| Purpose / Expected Result                                                                                                                                                                                                                                                                                                                                                                                                                      |                |               |                                       |                                                                                                                                                                                                                                                                        |         |
| A 3D reconstruction of the camera observed scene is visible in the output. If there are modules in the scene, these are detected and their models are visible in the output. Any damage is also detected and is visible in the output by means of bounding boxes around the region of anomaly. For each detected area of anomaly, a measure of the anomaly as average point-to-model distance is available. Processing time is also available. |                |               |                                       |                                                                                                                                                                                                                                                                        |         |
| Procedure                                                                                                                                                                                                                                                                                                                                                                                                                                      |                |               |                                       |                                                                                                                                                                                                                                                                        |         |
| <b>Configuration:</b><br>- Print two 3D cubes and two 3D parallelepiped (about same size as the walking manipulator parts), one cube and one parallelepiped should be undamaged, and one cube and one parallelepiped should be damaged with 1cm average surface error on side;<br>- Take two pictures from the stereo camera;<br>- Write down a DFPC configuration file.                                                                       |                |               |                                       |                                                                                                                                                                                                                                                                        |         |
| <b>Procedure:</b><br>- Execute a step-by-step integration test for DFPC instance 1.3 using the two printed models in input;<br>- Advance through the software steps until the final output is displayed.<br>- Take note of the detected anomaly, and the reported measured error.                                                                                                                                                              |                |               |                                       |                                                                                                                                                                                                                                                                        |         |
| Inputs                                                                                                                                                                                                                                                                                                                                                                                                                                         |                |               |                                       |                                                                                                                                                                                                                                                                        |         |
| VSA1.3.1 Picture of a scene which does not contain any object;<br>VSA1.3.2 Pictures of a scene which contains the 3D printed undamaged cube and the 3D printed undamaged parallelepiped within the shared view of the cameras;<br>VSA1.3.3 Pictures of a scene which contains the 3D printed damaged cube and the 3D printed damaged parallelepiped within the shared view of the cameras.                                                     |                |               |                                       |                                                                                                                                                                                                                                                                        |         |
| Covered Requirements                                                                                                                                                                                                                                                                                                                                                                                                                           |                |               |                                       |                                                                                                                                                                                                                                                                        |         |
| Surface Anomaly Detection of Spacecraft Modules<br>Surface Anomaly Detection of Walking Manipulator                                                                                                                                                                                                                                                                                                                                            |                |               |                                       |                                                                                                                                                                                                                                                                        |         |

{34}------------------------------------------------

![](_page_34_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 34  
---
Demonstration Prodedures  

| ID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | VSA1.4                  | Title         | Detection of small cube objects |                                                                                                                                                                                                                                                                                 | Lead | USTRATH |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------|---------------|---------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------|---------|
| Type                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Software<br>Integration | Pre-Requisite |                                 | The source stereo camera has been calibrated and camera<br>calibration parameters are known,<br>The disparity computation has been calibrated and good<br>reconstruction parameters are known.<br>Good algorithm parameters are known as result of previous<br>experimentation. |      |         |
| Purpose / Expected Result                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |                         |               |                                 |                                                                                                                                                                                                                                                                                 |      |         |
| A 3D reconstruction of the camera observed scene is visible in the output. If there are modules in the scene, these are<br>detected and their models are visible in the output. Any damage is also detected and is visible in the output by means of<br>bounding boxes around the region of anomaly. For each detected area of anomaly, a measure of the anomaly as average<br>point-to-model distance is available, this is close to the real predicted damage. Processing time is also available.                                   |                         |               |                                 |                                                                                                                                                                                                                                                                                 |      |         |
| Procedure                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |                         |               |                                 |                                                                                                                                                                                                                                                                                 |      |         |
| Configuration:<br>- Print two 3D cubes (about same size as the interfaces), an undamaged ideal one, and a damaged one, with 5mm average<br>surface error on one face;<br>- Take two pictures from the stereo camera;<br>- Write down a DFPC configuration file.<br>Procedure:<br>- Execute a step-by-step integration test for DFPC instance 1.4 using a single model in input.<br>- Advance through the software steps until the final output is displayed.<br>- Take note of the detected anomaly, and the reported measured error. |                         |               |                                 |                                                                                                                                                                                                                                                                                 |      |         |
| Inputs:<br>VSA1.1.1. Picture of a scene which does not contain any cube object;<br>VSA1.1.2 Pictures of a scene which contains the 3D printed undamaged cube within the shared view of the cameras;<br>VSA1.1.3 Pictures of a scene which contains the 3D printed damaged cube within the shared view of the cameras.                                                                                                                                                                                                                 |                         |               |                                 |                                                                                                                                                                                                                                                                                 |      |         |
| Covered Requirements                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |                         |               |                                 |                                                                                                                                                                                                                                                                                 |      |         |
| Surface Anomaly Detection of Spacecraft Interfaces<br>Surface Anomaly Detection of Walking Manipulator Interfaces<br>Surface Anomaly Detection of Walking Manipulator                                                                                                                                                                                                                                                                                                                                                                 |                         |               |                                 |                                                                                                                                                                                                                                                                                 |      |         |

| ID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | VSA2.1               | Title         | Detection of a simple cube and its components                                                                                                                                                                                                                                | Lead | USTRATH |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------|---------|
| Type                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Software Integration | Pre-Requisite | The source stereo camera has been calibrated and camera<br>calibration parameters are known,<br>The disparity computation has been calibrated and good<br>reconstruction parameters are known.<br>Good algorithm parameters are known as result of previous experimentation. |      |         |
| Purpose / Expected Result                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |                      |               |                                                                                                                                                                                                                                                                              |      |         |
| A 3D reconstruction of the camera observed scene is visible in the output. If there are modules in the scene, these are<br>detected and their models are visible in the output. Any damage is also detected and is visible in the output by means of<br>bounding boxes around the region of anomaly. For each detected area of anomaly, a measure of the anomaly as average<br>point-to-model distance is available, this is close to the real predicted damage. Processing time is also available. |                      |               |                                                                                                                                                                                                                                                                              |      |         |
| Procedure                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |                      |               |                                                                                                                                                                                                                                                                              |      |         |
| Configuration:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                      |               |                                                                                                                                                                                                                                                                              |      |         |
| - Print two 3D almost-cubes (about same size as the interfaces). The cube should have a smaller cube attached to one face<br>(about the same size as the interfaces). One almost-cube should be an undamaged ideal one, the second almost-cube<br>should be a damaged one, with 1mm average surface error on one free face, and 5mm error on one free face of the smaller                                                                                                                           |                      |               |                                                                                                                                                                                                                                                                              |      |         |

attached cube;

{35}------------------------------------------------

![](_page_35_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 35  
---
Demonstration Prodedures  

- Take two pictures from the stereo camera;

- Write down a DFPC configuration file.

Procedure:

- Execute a step-by-step integration test for DFPC instance 2.1 using a single model in input.
- Advance through the software steps until the final output is displayed.
- Take note of the detected anomaly, and the reported measured error.

Inputs:

VSA1.1.1. Picture of a scene which does not contain the almost-cube object;

VSA1.1.2 Pictures of a scene which contains the 3D printed undamaged cube within the shared view of the cameras;

VSA1.1.3 Pictures of a scene which contains the 3D printed damaged cube within the shared view of the cameras.

#### **Covered Requirements**

Surface Anomaly Detection of Spacecraft Modules and their Interfaces. Surface Anomaly Detection of Walking Manipulator and its Interfaces.

| ID                        | VSA2.2               | Title         | Detection of simple cube objects and their components |                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Lead | USTRATH |
|---------------------------|----------------------|---------------|-------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------|---------|
| Type                      | Software Integration | Pre-Requisite |                                                       | The source stereo camera has been calibrated and camera calibration parameters are known,<br>The disparity computation has been calibrated and good reconstruction parameters are known.<br>Good algorithm parameters are known as result of previous experimentation.                                                                                                                                                                                     |      |         |
| Purpose / Expected Result |                      |               |                                                       | The source stereo camera has been calibrated and camera calibration parameters are known,<br>The disparity computation has been calibrated and good reconstruction parameters are known.<br>Good algorithm parameters are known as result of previous experimentation.                                                                                                                                                                                     |      |         |
| Procedure                 |                      |               |                                                       | <b>Configuration:</b><br>- Print two 3D almost-cubes (about same size as the interfaces). The cube should have a smaller cube attached to one face (about the same size as the interfaces), One almost-cube should be an undamaged ideal one, the second almost-cube should be a damaged one, with 1mm average surface error on one free face, and 5mm error on one free face of the smaller attached cube;<br>- Take two pictures from the stereo camera; |      |         |

- Write down a DFPC configuration file.

Procedure:

- Execute a step-by-step integration test for DFPC instance 2.2 using a single model in input.
- Advance through the software steps until the final output is displayed.
- Take note of the detected anomaly, and the reported measured error.

Inputs:

VSA1.2.1 Pictures of a scene which contains both 3D printed cubes within the shared view of the cameras.

#### **Covered Requirements**

Surface Anomaly Detection of Spacecraft Modules and their Interfaces. Surface Anomaly Detection of Walking Manipulator and its Interfaces.

{36}------------------------------------------------

![](_page_36_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 36  
---
Demonstration Prodedures  

| ID                        | VSA2.3                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Title | Detection of simple cube-like objects and their components |                                                                                                                                                                                                                                                                        |  | Lead | USTRATH |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|------|---------|
| Type                      | Software Integration                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |       | Pre-Requisite                                              | The source stereo camera has been calibrated and camera calibration parameters are known,<br>The disparity computation has been calibrated and good reconstruction parameters are known,<br>Good algorithm parameters are known as result of previous experimentation. |  |      |         |
| Purpose / Expected Result | A 3D reconstruction of the camera observed scene is visible in the output. If there are modules in the scene, these are detected and their models are visible in the output. Any damage is also detected and is visible in the output by means of bounding boxes around the region of anomaly. For each detected area of anomaly, a measure of the anomaly as average point-to-model distance is available. Processing time is also available.                                                                                                                                                                                                                                                          |       |                                                            |                                                                                                                                                                                                                                                                        |  |      |         |
| Procedure                 | <b>Configuration:</b><br>- Print two 3D almost-cubes (about same size as a walking manipulator component) and 3D almost-parallelepiped (about the same size as the walking manipulator component). The cube and the parallelepiped should have a smaller cube attached to one face (about the same size as the interfaces), One almost-cube and one almost-parallelepiped should be an undamaged ideal one, the second almost-cube and the second almost-parallelepiped should be a damaged one, with 1mm average surface error on one free face, and 5mm error on one free face of the smaller attached cube;<br>- Take two pictures from the stereo camera<br>- Write down a DFPC configuration file. |       |                                                            |                                                                                                                                                                                                                                                                        |  |      |         |
|                           | <b>Procedure:</b><br>- Execute a step-by-step integration test for DFPC instance 2.3 using the two printed models in input;<br>- Advance through the software steps until the final output is displayed.<br>- Take note of the detected anomaly, and the reported measured error.                                                                                                                                                                                                                                                                                                                                                                                                                       |       |                                                            |                                                                                                                                                                                                                                                                        |  |      |         |
| Inputs:                   | VSA2.3.1. Picture of a scene which does not contain any object;<br>VSA2.3.2 Pictures of a scene which contains the 3D printed undamaged cube and the 3D printed undamaged parallelepiped within the shared view of the cameras;<br>VSA2.3.3 Pictures of a scene which contains the 3D printed damaged cube and the 3D printed damaged parallelepiped within the shared view of the cameras.                                                                                                                                                                                                                                                                                                             |       |                                                            |                                                                                                                                                                                                                                                                        |  |      |         |
| Covered Requirements      | Surface Anomaly Detection of Spacecraft Modules<br>Surface Anomaly Detection of Walking Manipulator                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |       |                                                            |                                                                                                                                                                                                                                                                        |  |      |         |

| ID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | VSA3.1                  | Title                     | Detection of reconfiguration anomalies                                                                                                                                                                                                                                          |  | Lead | USTRATH |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|------|---------|
| Type                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Software<br>Integration | Pre-Requisite             | The source stereo camera has been calibrated and camera<br>calibration parameters are known,<br>The disparity computation has been calibrated and good<br>reconstruction parameters are known.<br>Good algorithm parameters are known as result of previous<br>experimentation. |  |      |         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |                         | Purpose / Expected Result |                                                                                                                                                                                                                                                                                 |  |      |         |
| A 3D reconstruction of the camera observed scene is visible in the output. If at least two cubes are present and their relative<br>position is possible in the reconfiguration pattern, the full reconfiguration pattern is displayed as an ideal model in the<br>scene. Represented pattern modules will have different colors. Green modules represent correctly detected modules in the<br>correct pattern position. Red modules represent correctly detected but their pattern position is within a tolerable error range<br>from the detected position. Blue modules represented non-detected modules. |                         |                           |                                                                                                                                                                                                                                                                                 |  |      |         |

{37}------------------------------------------------

![](_page_37_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 37  
---
Demonstration Prodedures  

**Procedure**

#### Configuration:

- Print three 3D undamaged cubes (about same size as the spacecraft modules);

- Prepare a configuration pattern of the cubes (positions of the cube in a 3D coordinate system);
- Take two pictures from the stereo camera;
- Write down a DFPC configuration file.

#### Procedure:

- Execute a step-by-step integration test for DFPC instance 3.1 using a single model in input.
- Advance through the software steps until the final output is displayed.
- Take note of the detected anomaly, and the reported measured error.

#### Inputs:

VSA3.1.1: Pictures of a scene with one module;

VSA3.1.2: Pictures of a scene with two modules in an incorrect relative position according to the pattern, all modules should stay within the field of view all both cameras;

VSA3.1.3: Pictures of a scene with two modules in a correct relative position according to the pattern, all modules should stay within the field of view all both cameras;

VSA3.1.4: Pictures of a scene with three modules, two modules are in a correct position, the third is in an incorrect position (above the tolerance threshold), all modules should stay within the field of view all both cameras;

VSA3.1.5: Pictures of a scene with three modules, two modules are in a correct position, the third is in an incorrect position (within the tolerance threshold), all modules should stay within the field of view all both cameras;

VSA3.1.6: Pictures of a scene with the three modules in the correct pattern position, all modules should stay within the field of view all both cameras.

#### **Covered Requirements**

Reconfiguration Anomaly Detection

{38}------------------------------------------------

![](_page_38_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 38  
---
Demonstration Prodedures  

# <span id="page-38-0"></span>**3 Integration Tests (On-site, end WP4-WP5)**

We describe our testing strategy for the integration phase in the final demonstrator. This is based on the assumption that all individual components have been tested in the previous phases.

## <span id="page-38-1"></span>**Sub-Systems Validation Tests**

The full demonstration scenarios are built from a sequence of autonomous operations managed by the different components of the MOSAR setup. Before demonstrating these scenarios, the purpose of the sub-systems validation tests is to validate and verify the good operations of the individual sub-systems. Whenever possible, these tests are done before integrating in the final set-up. The sub-system tests include: The design and simulation tool

- The monitoring and control centre
- The design and Simulation tool
- The planner and the simulation interface
- The Servicer Spacecraft Bus (SVC)
- The client satellite bus (CLT)
- The spacecraft modules
- The walking manipulator
- The visual processing system

### <span id="page-38-2"></span>**ST1 - Monitoring and Control Centre**

The purpose of the tests on the Monitoring and Control Centre is to validate the possibility for the operator to control and monitor the other components of MOSAR through the Monitoring and Control console. This section will be limited to the initial configuration of the MCC setup, while the TM/TC of the other sub-subsystems will be described in the corresponding sections.

| Step  | Description and Goal                                                                                                                                                      | Procedure<br>Short description / reference of test set-up (EGSE/MGSE) and<br>the procedure to execute the test.                                                                                                                                                                                                                                       |
|-------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|       | Setup for on-ground plan computation                                                                                                                                      |                                                                                                                                                                                                                                                                                                                                                       |
| ST1-1 | Start the Monitoring and Control Console<br>The operator can visualize the GUI of the PUS<br>Console application.                                                         | Launch the PUS Console GUI application (instance for on-ground plan computation) in the MMC computer The application waits for the start-up of the OBC-S and OBC-C SW                                                                                                                                                                                 |
| ST1-2 | Start the Simulator<br>The operator can visualize the GUI of the<br>Simulator.                                                                                            | Launch the Simulator in the MMC computer                                                                                                                                                                                                                                                                                                              |
| ST1-3 | Start the MCC instance of the Agent SW<br>The operator runs the MCC instance of the<br>Agent SW, and verifies that the connections<br>between components are established. | Launch the application in the MCC computer Verify in the terminal output of the Agent SW that the connection to the PUS Console has been established, and vice versa Verify in the terminal output of the Agent SW that the connection with the Simulator has been established Verify that the PUS Console displays TM data produced by the Simulator |
|       | Setup for plan execution                                                                                                                                                  |                                                                                                                                                                                                                                                                                                                                                       |
| ST1-4 | Start the Monitoring and Control Console                                                                                                                                  | Launch the PUS Console GUI application (instance for on-plan execution) in the MMC computer                                                                                                                                                                                                                                                           |

{39}------------------------------------------------

![](_page_39_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 39  
---
Demonstration Prodedures  

| The operator can visualize the GUI of the PUS<br>Console application. |                                                                                                                                            | The application waits for the start-up of the OBC-S and<br>OBC-C SW |                                                                                                                                                                                                                                                                                               |
|-----------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ST1-5                                                                 | Start the OBC-C SW<br>The operator runs the OBC-C application.                                                                             | •                                                                   | Launch the OBC-C application<br>(note: the OBC-C can be accessed via SSH from the MCC)                                                                                                                                                                                                        |
| ST1-6                                                                 | Start the OBC-S SW<br>The operator runs the OBC-S application, and<br>verifies that the connections between<br>components are established. | •<br>•<br>•                                                         | Launch the OBC-S application<br>(note: the OBC-S can be accessed via SSH from the MCC)<br>Verify in the terminal output of each OBC-S, OBC-C and<br>PUS Console that the connections have been established<br>Verify that the PUS Console displays TM data produced by<br>the OBC-C and OBC-S |

These tests (and correlated ones after) address the following demonstration requirements (in integrated state):

**Requirements**

<span id="page-39-0"></span>IntR\_F301 (PUS services)

### **ST2 - Design and Simulation Tool**

The purpose of the tests on the Design and Simulation tool is to validate the possibility for the analyst to define the configuration of a spacecraft and to check this configuration regarding assembly constraints, resources utilization and steady state operations of the spacecraft.

| Step  | Description and Goal                                                                                                                                                                                                                                                                                                                                      | Procedure<br>Short description / reference of test set-up (EGSE/MGSE)<br>and the procedure to execute the test.                                                                                                                                                                        |
|-------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ST2-1 | Build spacecraft configuration<br>The analyst is able to describe the<br>spacecraft configuration (text based<br>structure) and the design tool can validate<br>the syntax of the description (structure,<br>components references, naming….).                                                                                                            | <br>Set scenario and component parameters in<br>configuration files<br><br>Initialize Design Tool in Matlab/Simulink<br><br>Check output of Design Tool on screen or in log<br>file                                                                                                 |
| ST2-2 | Visualize spacecraft configuration<br>The spacecraft configuration can be loaded<br>in the Simulator and the analyst can<br>visualize the spacecraft state (support to the<br>design phase)                                                                                                                                                               | <br>Set scenario and component parameters in<br>configuration files<br><br>Start FES with required sub components (WM<br>controller)<br><br>Simplified visualization directly in Matlab Simulink<br>using FES<br><br>Advanced visualization requires SIMvis                        |
| ST2-3 | Validate spacecraft design step 1 –<br>Design Tool<br>The design tool can perform initial check of<br>the spacecraft configuration regarding<br>assembly constraints (SM<br>positions/orientations, SI mating…)                                                                                                                                           | <br>Set scenario and component parameters in<br>configuration files<br><br>Initialize Design Tool in Matlab/Simulink<br><br>Check output of Design Tool on screen or in log<br>file                                                                                                 |
| ST2-4 | Validate spacecraft design step 2 –<br>Simulation Tool<br>The simulation tool can validate the<br>spacecraft configuration performance, with<br>multi-physics simulation, regarding steady<br>state operations (power, thermal, data<br>resources and management)<br>(The test can be performed for different<br>environmental conditions, e.g. LEO, Lab) | <br>Set scenario and component parameters in<br>configuration files<br><br>Start FES with required sub components (WM<br>controller, trajectory planner)<br><br>Run full FES simulation<br><br>Run scripts for output analysis and plotting of data<br><br>Analyze data and plots |

{40}------------------------------------------------

![](_page_40_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 40  
---
Demonstration Prodedures  

| ST2-5                                                                                                                              | Generate goal description for the Planner<br>The desired spacecraft configuration is saved for input to the Planner. |
|------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| • The user runs Matlab script to create a TC file that can be sent to the Agent SW for execution (JSON file with embedded macros). |                                                                                                                      |

These tests address the following demonstration requirements (in integrated state):

| Requirements                                     |
|--------------------------------------------------|
| FuncR_E101 (Design and Simulation Tool Purpose)  |
| FuncR_E102 (Design Software)                     |
| FuncR_E105 (Simulation Topics)                   |
| FuncR_E108 (Environmental Conditions Simulation) |

#### <span id="page-40-0"></span>**ST3 – Planner and Simulation Tool**

The purpose of the tests on the planner and simulation tool is to validate the possibility for the system to build a valid and verified plan that can be uploaded to the Space Segment for operations.

| Step  | Description and Goal                                                                                                                                                                                                                                                                                                                                         | Procedure                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|-------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ST3-1 | Load spacecraft configuration<br>The analyst can load a spacecraft<br>configuration description in the Planner tool                                                                                                                                                                                                                                          | •<br>Prerequisites:<br>o The on-ground setup has been started<br>following ST1-1 to 3<br>o The TC file describing the goal spacecraft<br>configuration has been created following ST2<br>•<br>The analyst loads the TC file in the PUS Console GUI;<br>this launches the calculation and execution of the plan<br>against the Simulator, with re-planning enabled                                                                                                                                                                                                                                                                                                                                               |
| ST3-2 | Build reconfiguration plan<br>Based on the description of two spacecraft<br>configurations, the Planner can build a<br>reconfiguration plan with a sequence of WM,<br>SM relocation (simple case description). The<br>plan can be visualized by the analyst.                                                                                                 | •<br>The analyst verifies that an initial plan has been<br>computed, by observing the PUS 200 TM emitted by<br>the Agent and visualized in the PUS Console                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ST3-3 | Test reconfiguration and feedback<br>The FES can simulate the system<br>reconfiguration in closed loop interaction<br>with the ground instance of ERGO (plan<br>decomposition) and the Functional Layer<br>(ground versions of controllers and drivers).<br>The FES can provide feedback to the<br>Planner about the success or not of the plan<br>execution | •<br>Prerequisites:<br>o Set parameter files for components and<br>scenario<br>o Initialize full setup of FES, WM controller and<br>Trajectory planner<br>•<br>Procedure:<br>o Start design tool from MATLAB/ Simulink<br>o Wait until analysis is finished<br>o Check Design Tool log file for warnings and errors<br>o If everything is ok run full FES simulation,<br>otherwise adjust parameters and/or scenario<br>o Run trajectory planner with the desired trajectory it<br>will send commands to the WM controller which<br>will communicate with the FES<br>o Wait until simulation is finished.<br>o Generate data files and plots for the simulation<br>•<br>Analyse the simulator outputs and plots |
| ST3-4 | Reconfiguration Visualization<br>The analyst can visualize the spacecraft<br>reconfiguration operations on the Simulator                                                                                                                                                                                                                                     | •<br>Prerequisites:<br>o Full simulation run with FES, trajectory<br>planner and WM controller                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |

{41}------------------------------------------------

![](_page_41_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 41  
---
Demonstration Prodedures  

|       |                                                                                                                                                                                                                                               | o<br>Adjust FES evaluation script in MATLAB for<br>times at which the configuration should be<br>visualized<br>o<br>Run FES evaluation script in MATLAB. It will<br>generate a plot for each of the configured<br>time steps.<br><br>Full continuous visualization (optional) requires SimVIS<br>and all geometry data files and is generated directly<br>while simulating using the FES. |
|-------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ST3-5 | Reconfiguration Monitoring<br>The analyst can visualize the spacecraft<br>components and simulation state<br>parameters through the GUI of the MCC<br>during the spacecraft reconfiguration                                                   | <br>The analyst monitors the evolution of the system<br>parameters through the PUS service 3 (housekeeping<br>TM)<br><br>The analyst monitors the plan execution and re<br>planning events through the PUS service 200 (Agent<br>management)                                                                                                                                             |
| ST3-6 | Iteration<br>The above sequence from ST2-1 to ST2-4 is<br>repeated with a more complex example,<br>leading to a failure of the plan execution in<br>the simulation.<br>The Planner can iterate with the FES to find<br>a valid plan execution | <br>The analyst monitors the failure of plan execution, the<br>re-planning and the attempt to execute the new plan<br>through the PUS service 200 (re-planning starts from<br>the current state of the system, not from the initial state)                                                                                                                                                |
| ST3-7 | Plan Saving<br>Following a successful plan execution, the<br>Planner can save the valid plan for future<br>uploading to the onboard Autonomy Agent<br>of the OBC-S. The analyst can have access<br>to the file                                | <br>The analyst retrieves the successful plan execution<br>record from the Agent output files<br><br>The successful plan execution record is transformed<br>into a plan TC file for execution at E3 autonomy level by<br>the on-board system                                                                                                                                             |

| Requirements                                         |
|------------------------------------------------------|
| FuncR_E104 (Task Planning and Simulation)            |
| FuncR_E106 (Simulation of Reconfiguration)           |
| FuncR_E109 (Manipulator Dynamics Simulation)         |
| PerfR_E201 (Simulation Real-Time Performance)        |
| PerfR_E202 (Number of SM in Simulation)              |
| IntR_E301(Simulator Input Interfaces)                |
| IntR_E302 (Simulator Output Interfaces)              |
| IntR_E303 (Simulator Communication Interface)        |
| IntR_E304 (Generation of plan for onboard execution) |

{42}------------------------------------------------

![](_page_42_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 42  
---
Demonstration Prodedures  

### <span id="page-42-0"></span>**ST4 - Servicer Spacecraft Bus (SVC)**

The purpose of the tests on the SVC is to validate the connection to and the operations of its components that include the OBC-S, the R-ICU and the cPDU, respectively for the data and power transfer management through the passive HOTDOCK interfaces.

The tests include the following steps:

| Step  | Description and Goal                                                                                                                                                                                                | Procedure<br>Short description / reference of test set-up (EGSE/MGSE) and<br>the procedure to execute the test.                                                                                                                                                                  |
|-------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ST4-1 | SVC Start-up<br>The operator can have remote access to<br>the OBC-S (e.g. SSH) and confirm the<br>connection to the R-ICU (from the OBC-S)<br>and the start of the TTC service.                                     | <b>•</b><br>The SVC is powered-on from EGSE<br><b>•</b><br>The operator launches the OBC-S SW on the terminal<br>(SSH)                                                                                                                                                           |
| ST4-2 | MCC Monitoring<br>The operator can visualize and monitor on<br>the MCC the parameters of the SVC that<br>includes the OBC-S, the R-ICU and the<br>cPDU (through the TTC service of the<br>OBC-S)                    | <b>•</b><br>The operator visualizes enables the generation of<br>housekeeping TM reports using the PUS 3 service; note<br>that only when the counterpart applications at the MCC<br>and OBC-C are started, the OBC-S SW initialization will<br>complete and TM will be generated |
| ST4-3 | MCC Commanding<br>The operator can send telecommands<br>from the MCC and validate the control of<br>the SVC components that includes the<br>OBC-S, the R-ICU and the cPDU (through<br>the TTC service of the OBC-S) | <b>•</b><br>The operator uses the PUS Console GUI and PUS<br>service 210 (mission-specific) to issue component TCs;<br>the APID for OBC-S is used as TC destination                                                                                                              |
| ST4-4 | Execution Plan Loading<br>The operator can upload an execution<br>plan from the MCC to the OBC-C                                                                                                                    | <b>•</b><br>The operator loads the TC file generated in ST3-9; this<br>file contains a set of TC[200,3] telecommands that<br>represent the plan to be executed at E3 autonomy level                                                                                              |

| Requirements                                         |
|------------------------------------------------------|
| IntR_E304 (Generation of plan for onboard execution) |
| FuncR_A104 (SVC high level control)                  |
| FuncR_A105 (Components low level control)            |
| FuncR_A108 (Monitoring)                              |

{43}------------------------------------------------

![](_page_43_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 43  
---
Demonstration Prodedures  

### <span id="page-43-0"></span>**ST5 - Client Satellite Bus (CLT)**

The purpose of the tests on the CLT is to validate the connection to and the operations of its components that include the R-ICU, the cPDU, respectively for the data and power transfer management through the CLT HOTDOCK interfaces, from which one is active. The R-ICU is connected to the OBC-S (SVC) spW network, which represent the docking data interface between the SVC and the CLT (considered as permanent in the MOSAR demonstrator).

The tests include the following steps:

| Step              | Description and Goal                                                                                                                                                                                                            | Procedure<br>Short description / reference of test set-up (EGSE/MGSE)<br>and the procedure to execute the test.                                                                                                                                                           |
|-------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Initial Condition | The SVC is powered on with TM/TC with the<br>MCC and spW data connection to the CLT<br>SpW network (data docking interface)                                                                                                     |                                                                                                                                                                                                                                                                           |
| ST5-1             | CLT Start-up<br>The CLT is powered on and the operator<br>can confirm the connection to the CLT R-<br>ICU, by remote access to the OBC-S                                                                                        | •<br>The operator launches the OBC-C SW on the terminal                                                                                                                                                                                                                   |
| ST5-2             | MCC Monitoring<br>The operator can visualize and monitor on<br>the MCC the parameters of the CLT that<br>includes the R-ICU, the cPDU and the<br>active HOTDOCK SI (through the TTC<br>service of the OBC-S)                    | •<br>The operator visualizes enables the generation of<br>housekeeping TM reports using the PUS 3 service;<br>note that only when the counterpart applications at the<br>MCC and OBC-S are started, the OBC-C SW<br>initialization will complete and TM will be generated |
| ST5-3             | MCC Commanding<br>The operator can send telecommands from<br>the MCC and validate the control of the CLT<br>components that includes the R-ICU, the<br>cPDU and the active HOTDOCK SI (through<br>the TTC service of the OBC-S) | •<br>The operator uses the PUS Console GUI and PUS<br>service 210 (mission-specific) to issue component TCs;<br>the APID for OBC-C is used as TC destination                                                                                                              |

| Requirements                              |
|-------------------------------------------|
| FuncR_A104 (SVC high level control)       |
| FuncR_A105 (Components low level control) |
| FuncR_A108 (Monitoring)                   |

{44}------------------------------------------------

![](_page_44_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 44  
---
Demonstration Prodedures  

### <span id="page-44-0"></span>**ST6 - Spacecraft Modules (SM)**

The purpose of the validation tests on the SM is to validate, for each SM, the correct operation of the internal components, that includes the generic elements as the R-ICU, cPDU and SI, and the specific payloads (as available on each SM), in order to be usable for the other validation tests (c.f. WM) and the demonstration.

There is two configurations of SM in the system. Two SM (SM1-DMS and SM2-PWS) are permanently fixed on the CLT structure with data and power connections between them and with the CLT components. The other SM are movable and can be interfaced with the spacecraft through the HOTDOCK SI. For this set of tests, the mobile SM will be manipulated manually by the operator for alignment with the active HOTDOCK SI of the CLT, before initiating their connection.

The tests are split between the generic components validation (described once here, but applied on all SM) and the specific payload validation (except the thermal fluid transfer, covered by the demonstration scenarios).

|                                                                                                                                                                                                                                             |                                                                                                                                                                                                                                                                                                                                                                                               | Procedure                                                                                                                                                                                                                                                                                 |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Step                                                                                                                                                                                                                                        | Description and Goal                                                                                                                                                                                                                                                                                                                                                                          | Short description / reference of test set-up (EGSE/MGSE) and<br>the procedure to execute the test.                                                                                                                                                                                        |
|                                                                                                                                                                                                                                             | Initial Condition<br>For mobile SM, the SM is connected<br>through the active HOTDOCK of the CLT<br>(powered-off), with the possibility to<br>transfer power and data                                                                                                                                                                                                                         |                                                                                                                                                                                                                                                                                           |
| ST6-1                                                                                                                                                                                                                                       | SM Start-up<br>The SM is powered on by activating the<br>corresponding power line from the CLT<br>cPDU. The internal SM R-ICU shall<br>automatically power on and establish a<br>SpW link with the CLT R-ICU. The<br>operator can confirm the availability of the<br>SM R-ICU by monitoring the CLT R-ICU<br>parameters (connected ports) on the<br>MCC.                                      | <br>The operator issues the TC[210,X] to enable power to the<br>SM<br><br>the presence in the network of the new SM is detected<br>and the SW is automatically reconfigured<br><br>the operator to command the reconfiguration of the SW to<br>enable the TM using the PUS TC[2X0,Y]   |
| ST6-2                                                                                                                                                                                                                                       | CLT R-ICU Routing<br>The operator can send a TC to the OBC-S<br>(with the MCC or through remote access)<br>and configure the data routing of the CLT<br>R-ICU (enabling routing of packets from<br>SM R-ICU).                                                                                                                                                                                 | <br>The operator issues the TC[210,X] to configure the<br>routing table of the CLT-R-ICU [depending on automatic<br>reconfiguration]                                                                                                                                                     |
| ST6-3                                                                                                                                                                                                                                       | SM R-ICU Configuration<br>The operator can send a TC to the OBC-S<br>(with the MCC or through remote access)<br>and configure the SM R-ICU (service<br>exposition and logical address allocation)                                                                                                                                                                                             | <br>The operator issues the TC[210,X] to configure the<br>routing table of the SM [depending on automatic<br>reconfiguration]                                                                                                                                                            |
| ST6-4                                                                                                                                                                                                                                       | MCC Monitoring<br>The operator can visualize and monitor on<br>the MCC the parameters of the SM that<br>includes the R-ICU, the cPDU and the<br>active HOTDOCK SI (through the TTC<br>service of the OBC-S)                                                                                                                                                                                   | <br>The operator visualizes and enables the generation of<br>housekeeping TM reports using the PUS 3 service                                                                                                                                                                             |
| ST6-5                                                                                                                                                                                                                                       | MCC Commanding<br>The operator can send telecommands<br>from the MCC and validate the control of<br>the SM components that includes the R-ICU                                                                                                                                                                                                                                                 | <br>The operator uses the PUS Console GUI and PUS<br>service 210 (mission-specific) to issue component TCs;<br>the APID for OBC-C is used as TC destination, and SM<br>and HOTDOCK IDs are passed as parameters.                                                                         |
| Step                                                                                                                                                                                                                                        | Description and Goal                                                                                                                                                                                                                                                                                                                                                                          | Procedure<br>Short description / reference of test set-up (EGSE/MGSE) and<br>the procedure to execute the test.                                                                                                                                                                           |
|                                                                                                                                                                                                                                             | Initial Condition<br>For each test, it is expected that the SM is<br>connected and powered-on. It has a<br>TM/TC connection with the MCC, through<br>the OBC-S TTC service                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                           |
| ST6-6                                                                                                                                                                                                                                       | SM2-PWS Thermal Payload MCC<br>Monitoring (Part 1)<br>The operator can visualize and monitor on<br>the MCC the parameters of the SM2-PWS<br>Thermal payload (through the TTC service<br>of the OBC-S). This test doesn't cover<br>fluid transfer to another module (covered<br>by scenario 3)                                                                                                 | See ST6-4. List of parameters to observe is TBD.                                                                                                                                                                                                                                          |
| ST6-7                                                                                                                                                                                                                                       | SM2-PWS Thermal Payload MCC<br>Control (Part 1)<br>The operator can send telecommands<br>from the MCC and validate the control of<br>SM2-PWS Thermal payload (through the<br>TTC service of the OBC-S). This test<br>doesn't cover fluid transfer to another<br>module (covered by scenario 3)<br>Note: The power TC functions are<br>managed by the cPDU, covered in the<br>generic SM tests | See ST6-5. List of commands to issue is TBD.                                                                                                                                                                                                                                              |
| ST6-8                                                                                                                                                                                                                                       | SM3-BAT Battery Payload MCC<br>Monitoring<br>The operator can visualize and monitor on<br>the MCC the parameters of the SM3-BAT<br>Thermal payload (through the TTC service<br>of the OBC-S).                                                                                                                                                                                                 | See ST6-4. List of parameters to observe is TBD.                                                                                                                                                                                                                                          |
| ST6-9                                                                                                                                                                                                                                       | SM3-BAT Battery Payload MCC Control<br>The operator can send telecommands<br>from the MCC and validate the control of<br>SM3-BAT Thermal payload (through the<br>TTC service of the OBC-S).                                                                                                                                                                                                   | See ST6-5. List of commands to issue is TBD.                                                                                                                                                                                                                                              |
| ST6-9                                                                                                                                                                                                                                       | SM4-THS Thermal Payload MCC<br>Monitoring (Part 2)<br>The operator can visualize and monitor on<br>the MCC the parameters of the SM4-THS<br>Thermal payload (through the TTC service<br>of the OBC-S). This test doesn't cover<br>fluid transfer to another module (covered<br>by scenario 3)                                                                                                 | See ST6-4. List of parameters to observe is TBD.                                                                                                                                                                                                                                          |
| ST6-10                                                                                                                                                                                                                                      | SM4-THS Thermal Payload MCC<br>Control (Part 2)<br>The operator can send telecommands<br>from the MCC and validate the control of<br>SM4-THS Thermal payload (through the<br>TTC service of the OBC-S).                                                                                                                                                                                       | See ST6-5. List of commands to issue is TBD.                                                                                                                                                                                                                                              |
| The operator can send telecommands<br>from the MCC and validate the control of<br>SM4-THS Thermal payload (through the<br>TTC service of the OBC-S). This test<br>doesn't cover fluid transfer to another<br>module (covered by scenario 3) |                                                                                                                                                                                                                                                                                                                                                                                               |                                                                                                                                                                                                                                                                                           |
| ST6-11                                                                                                                                                                                                                                      | SM5/6 Optical Payload MCC Monitoring<br>The operator can visualize and monitor on<br>the MCC the parameters of the SM5/6<br>Optical payload                                                                                                                                                                                                                                                   | See ST6-4. List of parameters to observe is TBD.                                                                                                                                                                                                                                          |
| ST6-12                                                                                                                                                                                                                                      | SM5/6 Optical Payload MCC Control<br>The operator can send telecommands<br>from the MCC and validate the control of<br>SM5/6-OSP Optical payload (through the<br>TTC service of the OBC-S).                                                                                                                                                                                                   | See ST6-5. List of commands to issue is TBD.                                                                                                                                                                                                                                              |
| ST6-13                                                                                                                                                                                                                                      | SM5/6 Optical Payload Data<br>The operator can visualize on the MCC<br>the image frames coming from the<br>OSP5/6 Optical payload (through the<br>Payload Relay service of the OBC-S).                                                                                                                                                                                                        | The operator launches the image visualization tool in the<br>MCC, and checks the output to verify that the connection<br>to the image relay in the OBC-C is establishedThe operator commands the camera to capture an image<br>using TC[210,X]The operator visualizes the images captured |

{45}------------------------------------------------

![](_page_45_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 45  
---
Demonstration Prodedures  

| ICU, the cPDU and the active HOTDOCK SI (through the TTC service of the OBC-C) |  |
|--------------------------------------------------------------------------------|--|
|--------------------------------------------------------------------------------|--|

The sub-system tests will use the OBC-S of the SVC to ensure the TM/TC link with the MCC. However, during the scenarios, it is the client satellite OBC-C (located in the SM1-DMS) that will perform the TM/TC during nominal operations. This will require the switching of the SpW network management between the reconfiguration and nominal operation phase. Tests related to the SM1- DMS are covered in section [3.2.5.](#page-54-0) The specific payload tests include the following steps:

{46}------------------------------------------------

![](_page_46_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 46  
---
Demonstration Prodedures  

| Requirements                                    |
|-------------------------------------------------|
| FuncR_A104 (SVC high level control)             |
| FuncR_A105 (Components low level control)       |
| FuncR_A108 (Monitoring)                         |
| FuncR_A111 (Modules Plug & Play detection )     |
| FuncR_C104 (SM data transmission)               |
| FuncR_C104 bis (SM power routing configuration) |
| FuncR_C106 (SM power-on/off)                    |
| FuncR_C107 (SM start and initialization)        |
| FuncR_C108 (Identification information)         |
| FuncR_C109 (Fault detection)                    |
| IntR_C301 (SM power)                            |
| IntR_C302 (SM R-ICU power Up)                   |
| IntR_C303 (SM R-ICU to SI TM/TC)                |
| ConfR_C801 (Demonstrator SM Configurations)     |
| FuncR_F104 (Large data transfer over SpaceWire) |

{47}------------------------------------------------

![](_page_47_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 47  
---
Demonstration Prodedures  

### <span id="page-47-0"></span>**ST7 - Walking Manipulator**

The purpose of the validation tests on the WM is to validate its correct operation, its interfaces with the OBC and MCC for TM/TC, to ensure it is ready for the demonstrations.

|       |                                                                                                                                                                                                                                                                                                                                                                             | Procedure                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|-------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Step  | Description and Goal                                                                                                                                                                                                                                                                                                                                                        | Short description / reference of test set-up (EGSE/MGSE) and<br>the procedure to execute the test.                                                                                                                                                                                                                                                                                                                                                                                                                  |
|       | Initial Condition<br>The WM is connected through an<br>HOTDOCK of the CLT or SVC and<br>powered-off, with the possibility to transfer<br>power and data                                                                                                                                                                                                                     |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ST6-1 | WM Start-up<br>The WM is powered on by activating the<br>corresponding power line from the CLT<br>cPDU (with the MCC). The internal WM<br>Controller shall automatically power on<br>and establish a SpW link with the CLT R<br>ICU. The operator can confirm the<br>availability of the SM R-ICU by monitoring<br>the CLT R-ICU parameters (connected<br>ports) on the MCC | <br>The operator enables power transfer to the WM using a<br>TC[210,X] TC<br><br>[TBC depending on automatic network reconfiguration]<br>The operator configures the SpW routing table of the SVC<br>and CLT R-ICU using TC[210,X]<br><br>The operator enables the housekeeping TM for the WM<br>using PUS service 3<br><br>The operator verifies that the housekeeping TM for the<br>WM is received and displayed in the PUS console                                                                           |
| ST6-2 | WM Configuration<br>The operator can send a TC to the OBC-S<br>(with the MCC or through remote access)<br>and configure the WM Controller (service<br>exposition and logical address allocation)                                                                                                                                                                            | <br>By an external command the WM Controller (WM OBC) is<br>activated and put in operational mode.<br>o<br>Activates interface to ERGO/Planner<br>o<br>Activates interface to EtherCAT<br>o<br>TBD                                                                                                                                                                                                                                                                                                                 |
| ST6-4 | WM Monitoring<br>The operator can visualize and monitor on<br>the MCC the parameters of the WM that<br>includes its own parameters and the two<br>active HOTDOCK SI (through the TTC<br>service of the OBC-S)                                                                                                                                                               | <br>The operator visualizes the housekeeping TM for the WM<br>and the rest of the components in the PUS Console                                                                                                                                                                                                                                                                                                                                                                                                    |
| ST6-5 | WM Low-Level Commands<br>The operator can send telecommands and<br>validate the control of the WM, that<br>includes:<br><br>Cartesian position command<br><br>Impedance mode control<br><br>Mode of operation<br><br>Administrative commands<br><br>Operations of the two<br>HOTDOCK SI (requiring a<br>switch of the robot base)                                      | <br>start action; stop action<br><br>command counter to detect a new command<br><br>command id to select the desired action:<br>o<br>Power<br>o<br>Controller<br>o<br>joint trajectory list<br>o<br>Cartesian motion<br>o<br>interface command<br><br>command control mode<br>o<br>Torque control<br>o<br>Position control<br><br>List of joint configurations for transfer motion<br><br>Goal pose for approach/docking operation<br><br>HOTDOCK commanding is through the same TCs<br>than the SM HOTDOCKS |
| ST6-6 | OBC-S WM High-Level Commands<br>The operator can send telecommands<br>from the MCC to the OBC-S to initiate the<br>high-level trajectory commands<br>implemented during the spacecraft<br>reconfiguration operations and validate the<br>behavior of the WM, that includes:                                                                                                 | <br>The WM is moving based on given a series of joint<br>position sets<br><br>The WM is moving impedance controlled based on<br>on a Cartesian goal pose.                                                                                                                                                                                                                                                                                                                                                         |

{48}------------------------------------------------

![](_page_48_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 48  
---
Demonstration Prodedures  

 Move Cartesian Position Move Cartesian Impedance

| Requirements                              |
|-------------------------------------------|
| FuncR_A104 (SVC high level control)       |  
| FuncR_A105 (Components low level control) |  
| FuncR_A108 (Monitoring)                   |   
| FuncR_B101 (SM connection)                |    
| FuncR_B103 (Joint position control)       |    
| FuncR_B104 (Cartesian position control)   |    
| FuncR_B104 bis (Impedance control)        |    
| FuncR_B105 (Fault detection)              |    
| FuncR_B106 (Power-on/off)                 |    
| FuncR_B107 (WM start and initialization)  |    
| IntR_B301 (WM TM/TC)                      |    
| IntR_B303 (WM power)                      |    
| IntR_B305 (WM local CAN network)          |    
| IntR_B306 (WM local control network)      |    
| IntR_B307 (WM mechanical interface to SI) |    

{49}------------------------------------------------

![](_page_49_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 49  
---
Demonstration Prodedures  

### <span id="page-49-0"></span>**ST10-Visual Processing System**

The test purpose is to verify whether the vision processing system is able to validate the shape of the spacecraft modules, hardware interfaces and walking manipulator, and to highlight any deviation from the expected ideal surface model. Processing time will be monitored in order to validate usability requirement. We will also evaluate whether some common defects are detectable.

| Step                                                                                                                                                                                                                  | Description and Goal                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Procedure<br><span style="font-size: smaller;">Short description / reference of test set-up<br/>(EGSE/MGSE) and the procedure to execute the test.</span>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | ID | Title                                                  | Description                                                                                          |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----|--------------------------------------------------------|------------------------------------------------------------------------------------------------------|
| <b>Initial Condition</b><br>The walking manipulator is ready to start operating on the satellite.<br>There is a damaged spacecraft module with a damaged interface. The damaged interface is visible from the camera. |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |    | Validation of Module Shape and Interfaces              | [DEVIATION]<br>Detect modules, their interfaces and highlight surface defects.                       |
| Steps 7.1-7.4                                                                                                                                                                                                         | 3D Reconstruction<br>The vision system is activated, the camera starts recording images and the software outputs initial results.<br>A partial representation of the scene is available on the output screen throughout the whole demonstration. The output changes if and only if there is actually some movement occurring on the demonstrator.<br>Any detected object will be highlighted by showing its model within the reconstructed cloud.<br>Any detected defect will be highlighted in an image or a point cloud. Damaged area will be highlighted with a bounding box in the point cloud.<br>The processing frequency is visible on the output screen. | If you are using the PTC camera bring the cameras to maximum zoom level.<br>Start either instance 1.2 or instance 1.3 of Module Anomaly Detection Program, or Instance 2.2 or Instance 2.3 of Interface Anomaly Detection Program.<br>Depending on the instance you started observe whether the following is true:<br>Instance 1.2: spacecraft modules and related damage should be detected;<br>Instance 1.3: walking manipulator modules and related damage should be detected;<br>Instance 2.2: spacecraft modules, their interfaces and related damage should be detected;<br>Instance 2.3: walking manipulator modules, their interfaces and related damage should be detected.<br>Repeat four times, once for each program instance. |    | Validation of Walking Manipulator Shape and Interfaces | [DEVIATION]<br>Detect walking manipulator components, their interfaces and highlight surface defects |
| Steps 7.5-7.6 (only for PTC cameras)                                                                                                                                                                                  | Selective Zooming<br>A partial representation of the scene is available on the output screen throughout the demonstration. The output changes if and only if there is actually some movement occurring on the scenario.<br>An interface will be highlighted by showing its model within the reconstructed cloud.<br>Damaged areas will be highlighted with a bounding box in the point cloud.<br>The processing frequency is visible on the output screen.                                                                                                                                                                                                       | Halt the current software instance.<br>Control the camera to focus on a visible interface.<br>Start Instance 1.4 Module Anomaly Detection for Selective Zooming Program.<br>Observe the interface and related damage is correctly detected.<br>Repeat twice, once with a non-damaged interface and once with a damaged interface.                                                                                                                                                                                                                                                                                                                                                                                                          |    | Validation of module configuration                     | [DEVIATION]<br>Detect modules and highlight final configuration defects                              |
| Steps 7.7-7.8                                                                                                                                                                                                         | Reconfiguration Validation<br>A partial representation of the scene is available on the output screen throughout the demonstration. The output changes if and only if there is actually some movement occurring on the demonstrator.<br>If at least two spacecraft modules are in the expected configuration, the final expected demonstration will be visible in the point cloud, and any difference with the real configuration will be highlighted. Specifically, spacecraft modules detected in the right position will be in green.                                                                                                                         | Halt the current software instance.<br>If you are using the PTC camera bring the cameras to maximum zoom level.<br>Start instance 3.1 Reconfiguration Anomaly Detection Program.<br>Repeat twice, once mid-way through the configuration, once at the end of the reconfiguration.                                                                                                                                                                                                                                                                                                                                                                                                                                                          |    | Selective Zooming                                      | [DEVIATION]<br>Detect interface defects with higher accuracy.                                        |

{50}------------------------------------------------

![](_page_50_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 50  
---
Demonstration Prodedures  

| | space module detected in a wrong position will be in red, and missing will be in blue. | |
|-|----------------------------------------------------------------------------------------|-|

Tests do not exhaust the set of all possible detects, due to the limitation on the number of components that can be manufactured. We will test whether some defects are reliably detectable, but we will not be able to assess what the smallest detectable defect is.

These tests address the following demonstration requirements:

There are some deviations on demonstrator requirements. Originally, the specified validation / demonstration tests were linked to the demonstrator testing requirements, as defined in [AD1.](#page-7-3) During the preliminary design phases, some of these requirements have been reviewed / descoped.

{51}------------------------------------------------

![](_page_51_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 51  
---
Demonstration Prodedures  

### <span id="page-51-0"></span>**Integration Validation Tests**

Following the sub-systems validation, the next phase will target to validate integrated systems. This will cover the main routine of operation, as defined in the DDD [\[RD6\]](#page-8-4), which are recurrent sequences of actions requested by the planner. It will also address other operations that implicate several components of the system and relevant for the final demonstration.

During the tests, the operator can observe the telemetry of the components implemented on the MCC.

### <span id="page-51-1"></span>**IT1 – WM Re-localization**

The purpose of this test is to validate the possibility for the WM to re-localize itself along the structure of the spacecraft, as illustrated in [Figure 3-1.](#page-51-2) This is a routine defined in [RD6.](#page-8-4)

The following initial conditions need to be full-filed to start the sequence:

- The WM SI-A is connected to the Initial SI, with power and data transmission
- The WM is powered on, is able to communicate with the OBC-S by SpW and is ready for operations
- The Target SI is able to provide power and data communication with the OBC-S
- The Target SI can be reached by the WM SI-B (following the required trajectory)

The test is successful if, at the end of the sequence, the WM is connected to the other SI and able to be interfaced with the MCC for TM/TC.

![](_page_51_Figure_15.jpeg)

![](_page_51_Figure_16.jpeg)

<span id="page-51-2"></span>On top of the requirements presented in section [3.1,](#page-38-1) this test address the following demonstration requirements:

| ID            | Title               | Description                                                                                            |
|---------------|---------------------|--------------------------------------------------------------------------------------------------------|
| FuncR_A107    | WM relocation       | The WM shall be able to reposition itself by using the SI of<br>the functional modules or the platform |
| IntR_B304 bis | WM interface switch | The WM shall be able to switch power and data interface<br>between the two SI extremities              |

{52}------------------------------------------------

![](_page_52_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 52  
---
Demonstration Prodedures  

### <span id="page-52-0"></span>**IT2 – SM Re-localization**

The purpose of this test is to validate the possibility for the WM to re-localize as SM between two different position/orientations on the SVC or CLT, as illustrated in [Figure 3-2.](#page-52-1) This is a routine defined in [RD6.](#page-8-4)

The following initial conditions need to be full-filed to start the sequence:

- SM powered-off
- The WM SI-A is connected to another SI (spacecraft or module), with power and data transmission
- The WM is powered on, is able to communicate with the OBC-S by SpW and is ready for operations
- The position of the WM and SM allow performing the desired trajectory between the initial and final position of the SM.

The test is successful if, at the end of the sequence, the SM has been moved to another connection point and is able to be monitored/commanded from the MCC.

The test can be repeated for different configuration of the SMs, including configuration with two and three simultaneous HOTDOCK connections.

![](_page_52_Figure_13.jpeg)

<span id="page-52-1"></span>**Figure 3-2: Routine 2 – SM re-localization**

{53}------------------------------------------------

![](_page_53_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 53  
---
Demonstration Prodedures  

On top of the requirements presented section [3.1,](#page-38-1) this test address the following demonstration requirements:

| ID         | Title                              | Description                                                                                                                                                                                                            |
|------------|------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FuncR_A109 | Spacecraft reconfiguration         | The system shall be able to re-configure the CLT (e.g. SM<br>exchange) in case of a defect (e.g. malfunction of a SM)                                                                                                  |
| FuncR_B102 | SM manipulation                    | The WM shall be able to move and assemble the functional<br>modules in a 3-dimensional way                                                                                                                             |
| PerfR_B201 | WM payload capability              | The WM shall be able to manipulate a payload of 7kg all<br>around his workspace                                                                                                                                        |
| IntR_B302  | WM data transfer                   | The WM shall be able to transmit TM/TC and data from the<br>SVC OBC with the SM connected at its SI                                                                                                                    |
| IntR_D301  | Mechanical Interface to Components | The standard interface shall provide a mechanical<br>connection to the modules, spacecraft bus or robotic<br>base/end-effector manipulator, compatible with the<br>mechanical loads transferred through the interface. |
| IntR_B304  | WM power transfer                  | The WM shall be able to transmit power to the SM<br>connected at its SI                                                                                                                                                |

### <span id="page-53-0"></span>**IT3 – Data Re-Routing**

The purpose of this test is to demonstrate the capability for the system to re-route data transmission between different modules.

The following initial conditions need to be full-filed to start the sequence:

- The SM1-DMS and CLT are operational and connected to the OBC-S by the SpW network
- One payload SM is connected simultaneously with the CLT and SM1 SI (using the two active HOTDOCK)
- The SM1 is powered on and configured such that it gets power from the CLT SI and data from the SM1-DMS.

The test is successful if, at the end of the sequence, the payload SM gets data directly from the CLT SI and can be disconnect from the SM1-DMS, while keeping TM/TC from the MCC.

On top of the requirements presented section [3.1,](#page-38-1) this test addresses the following demonstration requirements:

| ID         | Title                         | Description                                                                                                                                                                                             |
|------------|-------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FuncR_A110 | System redundancy             | The system shall be able to re-route and reallocate<br>resources (e.g. power, data, computational power, etc.) in<br>case of a defect (e.g. interconnector of an APM)                                   |
| FuncR_C103 | SM data routing configuration | The baseline functionality of a Spacecraft Module shall<br>include the ability to externally configure the SM's data<br>routing function between the Standard Interfaces and<br>services provided by SM |

### <span id="page-53-1"></span>**IT4 – Power Re-Routing**

The purpose of this test is to demonstrate the capability for the system to re-route power transmission between different modules.

{54}------------------------------------------------

![](_page_54_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 54  
---
Demonstration Prodedures  

The following initial conditions need to be full-filed to start the sequence:

- The SM1-DMS and CLT are operational and connected to the OBC-S by the SpW network
- One payload SM is connected simultaneously with the CLT and SM1 SI (using the two active HOTDOCK)
- The SM1 is powered on and configured such that it gets power from the SM1-DMS and data from the CLT.

The test is successful if, at the end of the sequence, the payload SM gets power directly from the CLT SI and can be disconnect from the SM1-DMS, while keeping TM/TC from the MCC.

On top of the requirements presented section [3.1,](#page-38-1) this test address the following demonstration requirements:

| ID         | Title             | Description                                                                                                                                                           |
|------------|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FuncR_A110 | System redundancy | The system shall be able to re-route and reallocate<br>resources (e.g. power, data, computational power, etc.) in<br>case of a defect (e.g. interconnector of an APM) |

### <span id="page-54-0"></span>**T5 – Software Reconfiguration**

The purpose of this test is to demonstrate the capability for the system to:

- Switch the responsibility of the SpW network management between the OBC-S and the OBC-C, and vice-versa (to switch between the nominal and reconfiguration operations)
- Update the CLT software in order to take into account new connected module/functionalities.

The first test is successful if the selected OBC can perform TM/TC with the spacecraft components

The second test is successful if the new module can get TM/TC from the MCC.

| ID         | Title                                            | Description                                                                                                                                                                     |
|------------|--------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FuncR_F101 | Extension of TASTE for<br>reconfigurable systems | The TASTE framework shall be extended to support<br>modelling and code generation for software systems that can<br>switch between different configurations known at design time |

### <span id="page-54-1"></span>**IT6 – Planned Operation**

All the above integration tests have been performed by manual TC from the operator through the MCC (or potentially direct access to the components). The purpose of this test is to illustrate the capability for the system to perform the same operations, autonomously, by the execution of a sequence of operations commanded by the ERGO Agent.

Integration tests IT1 to IT4 will be repeated with the following sequence:

- 1. Definition of the initial and final spacecraft model
- 2. Building of the reconfiguration plan
- 3. Execution of the reconfiguration plan by the OBC-S ERGO Agent
- 4. Monitoring of the system parameters in the MCC

The test will target simple scenario cases, such that the FES is not mandatory and an "easy" valid plan can be found.

{55}------------------------------------------------

![](_page_55_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 55  
---
Demonstration Prodedures  

The test will be successful if the four integration tests can be replicated, reaching the same final configuration.

Additional tests can be performed to validate the management of issue during the execution of the plan. Three levels are envisaged:

- Function layer level, with specific procedure, as for instance to retry the operation
- Planner level, with a replanning of the operations to take into account a problem
- MCC / user level, with information to the user, such that he can red-define the strategy

This aspect will be investigated during the detailed design phase, and the validation plan will be updated according to the selected strategies(s)

On top of the requirements presented section [3.1,](#page-38-1) this test address the following demonstration requirements:

| ID         | Title                          | Description                                                                                                                                                                                 |
|------------|--------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FuncR_A112 | Fault detection                | The SVC OBC shall be able to react to a faulty behavior<br>detected by the SM, WM or SI                                                                                                     |
| FuncR_F105 | ERGO robotic arm driver for WM | A robotic arm driver component shall be developed to<br>execute the robot plan actions on the WM and return the<br>observations needed by the Agent to manage the execution<br>of the plan. |
| FuncR_F106 | ERGO Agent for plan execution  | An instance of the ERGO Agent shall be deployed on the<br>OBC to command and monitor the execution of the robotic<br>reconfiguration plan generated on ground.                              |

{56}------------------------------------------------

![](_page_56_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 56  
---
Demonstration Prodedures  

# <span id="page-56-0"></span>**4 Demonstration Scenarios (On-site, WP5)**

The purpose of the MOSAR demonstrator is to illustrate five representative scenarios of modular spacecraft assembly and re-configuration operations. The baseline scenario is the one of a Servicer Spacecraft (SVC) transporting a cargo of Spacecraft Modules (SM) and a dedicated Walking Manipulator (WM), performing a number of operations with the transfer of SM from and to the Client Spacecraft (CLT) by the manipulator.

## <span id="page-56-1"></span>**Scenario 1 (S1): Initial Assembly of SMs from SVC to CLT**

### <span id="page-56-2"></span>**Scenario Description**

Objective: demonstrating the assembly of several SMs originally mounted on the SVC onto the CLT spacecraft bus, including both the placement of SMs on the CLT itself and on other SMs.

Initial Conditions: the initial configuration of the SMs is represented in [Figure 4-1-](#page-56-3)left

- two SM are already installed on the CLT (fixed position for the demonstrations), the SM1- DMS (OBC) and SM2-PWS (power module)
- the four other SM are stored on the SVC
- the WM is stowed in parking position on the SVC
- the system is ready for assembly operations

#### Success Conditions:

- the desired SMs are mounted onto the CLT, as illustrated in [Figure 4-1-](#page-56-3)right
- the newly mounted SMs are powered on and operational
- it should be possible to receive data / telemetry from each deployed SM and send commands to each of them, including video/picture rendering from the optical payload modules

![](_page_56_Figure_18.jpeg)

<span id="page-56-3"></span>**Figure 4-1: MOSAR scenario 1 initial and final configuration**

{57}------------------------------------------------

![](_page_57_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 57  
---
Demonstration Prodedures  

### <span id="page-57-0"></span>**Sequence of Operations**

The first scenario illustrates the typical sequence of operations that is proposed by the MOSAR operational concept. It includes the following steps:

- 1. Model of the initial spacecraft configuration (SVC and CLT)
- 2. Model of the final target spacecraft configuration (SVC and CLT)
- 3. Validation of the (initial) and final configuration according to system constraints
- 4. Build of the initial reconfiguration plan
- 5. Validation of the initial reconfiguration plan with the FES and the Functional layer
- 6. Successive Iteration on the re-configuration plan, while a valid plan is not found
- 7. Storing of the validated execution plan (the analyst could be informed that no valid plan can be found, meaning that the design model shall be reviewed)
- 8. Uploading of the validation plan on the OBC-S (on-board autonomous agent)
- 9. Configuration of the SVC/CLT SpW network, such that the OBC-S (SVC) has the hand on the control of the components (WM, SI, R-ICU, cPDU)
- 10. Execution and monitoring of the execution plan by the OBC-S Agent. It will consist in a sequence of operations and routines of WM and SM re-localization to transit from the initial to the final configuration.

If the execution is successful, the OBC-S informs the MCC operator and the spacecraft network is reconfigured to allow the CLT to manage the components (e.g. SM TM/TC).

If the execution is not a success, three cases can be envisaged:

- Function layer level, with specific procedure, as for instance to retry the operation
- Planner level, with a replanning of the operations to take into account a problem
- MCC / user level, with information to the user, such that he can red-define the strategy

### <span id="page-57-1"></span>**Scenario 2 (S2): Replacement of a failed SM**

#### <span id="page-57-2"></span>**Scenario Description**

Objective: demonstrating the detection and replacement of a failing module by an equivalent working module. This will be illustrated in the current scenario by the replacement of one of the optical payload modules by the second one.

Initial Conditions:

- the WM is stowed in parking position
- the CLT is assembled with the 6 SMs (final configuration of scenario 1) and operational [\(Figure 4-2-](#page-58-3)Left)
- the maintenance operation is ready to be carried out

#### Success Conditions:

- the faulty module should be brought back in the cargo area of the SVC
- the new optical SM has been mounted onto the same location of the failed SM on the CLT [\(Figure 4-2-](#page-58-3)Right)
- the newly replaced SMs should be powered and operational, i.e. recovery of functionality

{58}------------------------------------------------

![](_page_58_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 58  
---
Demonstration Prodedures  

![](_page_58_Figure_4.jpeg)

**Figure 4-2: MOSAR scenario 2 initial and final configuration**

### <span id="page-58-3"></span><span id="page-58-0"></span>**Sequence of Operations**

The sequence of operations for the scenario 2 will be initiated with the detection of a faulty behaviour in the SM5-OSP module (mounted on the top left of the CLT structure). This faulty behaviour will be triggered manually and detected by the Client OBC-C.

We currently consider to use an error status in the I3DS telemetry which indicates an unrepairable fault with the ZED camera (sensor failure). This will be propagated to the operator on the MCC that will then trigger a plan generation to replace the module.

It is not considered to use the visual system for this purpose, as their will be no direct link between it and the MCC monitoring

This will initiate the following sequence of actions:

- The CLT OBC-C will command to switch off the SM5-OSP module by opening all the power lines feeding the module (non-critical module isolation).
- The CLT OBC-C will inform the operator through the MCC about the issue (also visually displayed on the screen).
- The operator will request the analyst to provide a new spacecraft model, proposing the replacement of the faulty module with the SM6-OSP.
- The sequence of operations, as described in the first scenario is iterated based on the current and new final spacecraft configuration.

One objective of this scenario is to keep the spacecraft and the other SM operational during the replacement operations.

### <span id="page-58-1"></span>**Scenario 3 (S3): Thermal transfer between two SMs**

### <span id="page-58-2"></span>**Scenario Description**

Objective: demonstrating the active cooling of a SM producing heat (SM2-PWS) by a dedicated thermal handling module (SM4-THS)

Initial Conditions:

{59}------------------------------------------------

![](_page_59_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 59  
---
Demonstration Prodedures  

 the THS and the PWS modules are mechanically coupled and operational (final configuration of scenario 1)

Success Conditions:

- a heat transfer should be observed between the 2 modules (through telemetry reading with heat probes on the 2 sides).
- No leaks should have been observed.

### <span id="page-59-0"></span>**Sequence of Operations**

At the opposite of the two other demonstrations, this scenario doesn't require the operations of the ground segment simulator and planner, as the configuration remains static.

The system will be operated through the MCC user interface to perform TM/TC operations with the SM2-PWS and SM4-THS thermal payloads.

It will basically consist of the following sequence of actions:

- The temperature of the two modules is monitored on the MCC
- The heater in the SM2-PWS is switched on by the operator.
- The fluid transfer between SM2-PWS and SM4-THS is enabled by the operator (pump and valves commands).
- The fan (forced convection) is enabled on the SM4-THS.

AT each step, the temperature of both SM is monitored.

### <span id="page-59-1"></span>**Scenario 4 (S4): Automatic CLT Network Reconfiguration**

### <span id="page-59-2"></span>**Scenario Description**

Objective: demonstrating the ability of the SpaceWire network to automatically detect and adapt to faulty interfaces without the need of the SVC-OBC to be attached to reconfigure the network.

Initial Conditions: the configuration of the SMs represents a constructed spacecraft. The SVC is disconnected from the CLT.

- The optical SM is located at least one SM away from the OBC.
- The optical SM is part of a grid of SMs of a size of at least 2x2 (to provide two distinct network paths from the OBC to the optical SM).
- The network is configured such that the OBC can communicate with any SM in the network using logical addressing.
- All network links are active and running
- The OBC-CLT is running the application, constantly fetching image frames from the optical SM.

### Success Conditions:

- The faulty link is detected by the CLT-OBC
- The network topology is rediscovered with the faulty link excluded
- A new valid network mapping is found
- The network is reconfigured successfully, traffic starts to resume to and from the CLT-OBC and the optical SM.

{60}------------------------------------------------

![](_page_60_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 60  
---
Demonstration Prodedures  

### <span id="page-60-0"></span>**Sequence of Operations**

This scenario starts from the spacecraft constructed and operating nominally. The process is started by failing a link via the R-ICU debug interface.

- 1. Ensure that spacecraft is assembled and running the optical payload operation.
- 2. Fail one of the active links carrying the payload data between the CLT-OBC and the optical SM by commanding the SpaceWire link to DISABLED using the R-ICU debug interface.
- 3. CLT-OBC detects error due to receiving EEP or RMAP reply timeout.
- 4. CLT-OBC automatically initiates SpW-PnP network discovery sequence and rediscovers the network layout.
- 5. CLT-OBC runs network mapping algorithm on results of SpW PnP discovery to find shortest routing paths between nodes and CLT-OBC.
- 6. CLT-OBC uses RMAP to update the routing tables of all SpW routers in the network
- 7. CLT-OBC switches back to nominal mode
- 8. Optical payload operation continues using the discovered redundant network path.

Telemetry from the R-ICU debug port (USB UART) can be used to track this sequence, however when ran autonomously it is anticipated to be too fast to for an operator to interact with.

### <span id="page-60-1"></span>**Scenario 5 (S5): Software Reconfiguration**

#### <span id="page-60-2"></span>**Scenario Description**

Objective: demonstrating the ability of the TASTE approach to ease reconfigurable software development and anticipate scheduling issues at design time.

Initial Conditions:

- A TASTE model represents a simplified version of the CLT software and associated hardware.
- Active software functions correspond to the initial SMs in place

Success Conditions:

- Active software functions correspond to the final SMs in place
- The delay to reach the final software configuration is less than the given deadline

#### <span id="page-60-3"></span>**Sequence of Operations**

- Initial and final configurations are defined into the TASTE model
- The corresponding AADL "Concurrency View" is generated
- Scheduling analysis is performed at AADL model level
- C source code is generated and compiled
- A run-time scenario is executed

### <span id="page-60-4"></span>**Demonstrator Requirements Addressed by the Scenarios**

On top of the requirements presented sections [3.1](#page-38-1) an[d 3.2,](#page-51-0) these demonstrations address the following demonstration requirements:

| ID         | Title                | Description                                                                                                                                    | Scenarios |
|------------|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| FuncR_A101 | Demonstrator purpose | The MOSAR demonstrator shall illustrate the repair<br>and update of modular spacecraft by manipulation<br>and repositioning of SM with the WM. | S1, S2    |

{61}------------------------------------------------

![](_page_61_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 61  
---
Demonstration Prodedures  

| FuncR_A103 | Plan execution                | The SVC OBC shall execute autonomously the<br>assembly/ reconfiguration plan prepared by the<br>design and simulation tool                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | S1, S2     |
|------------|-------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
| FuncR_A106 | WM modules<br>operations      | The WM shall be able to add and replace SM<br>(ASM/APM) by using SI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | S1, S2     |
| FuncR_A109 | Spacecraft<br>reconfiguration | The system shall be able to re-configure the CLT<br>(e.g. SM exchange) in case of a defect (e.g.<br>malfunction of a SM)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | S2         |
| FuncR_A110 | System redundancy             | The system shall be able to re-route and reallocate<br>resources (e.g. power, data, computational power,<br>etc.) in case of a defect (e.g. interconnector of an<br>APM)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | S2, S4     |
| DesR_D403  | Diagonal Engagement           | The standard interface shall allow diagonal<br>engagement up to 55 deg                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | S1         |
| VerR_G101  | Validation purpose            | The MOSAR demonstrator shall allow to verify and<br>validate the following functionalities relevant for<br>future modular spacecraft missions:<br>• Creation of a re-configuration execution plan<br>(FuncR_S105)<br>• Simulation of the execution plan (FuncR_S106)<br>• Manipulation and repositioning of SM<br>(FuncR_S101)<br>• Control and re-location of the WM (FuncR_S104,<br>FuncR_S107)<br>• Update/upgrade of satellite functionalities<br>(FuncR_S102)<br>• Data and power transfer between SM<br>• Heat management between SM (FuncR_S115)<br>• Failure detection and handling (FuncR_S111)<br>• Resources re-allocation, data and power routing<br>(FuncR_S110) | S1, S2, S3 |
| VerR_G102  | Validation sequence           | The validation shall include the following<br>sequence:<br>1. Calibrate/verify the simulation tool<br>2. Simulate the reconfiguration process and<br>generate a valid robot execution plan<br>3. Execute the plan on the demonstrator setup                                                                                                                                                                                                                                                                                                                                                                                                                                   | S1, S2     |

{62}------------------------------------------------

![](_page_62_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 62  
---
Demonstration Prodedures  

# <span id="page-62-0"></span>**5 Demonstration Setup**

This section presents the setup and layout for the MOSAR demonstrator that includes the ground segment with the MCC and the space segment with the servicer and client satellite.

### <span id="page-62-1"></span>**General Layout**

The MOSAR demonstrator setup will be installed in the Space Applications Laboratory. [Figure 5-1](#page-62-2) and [Figure 5-2](#page-63-0) illustrates respectively the MOSAR setup 3D implementation view and top view layout. These views don't highlight yet the integration of the visual subsystem that will be refined during WP4. The following view is based on the estimated size of the servicer and client satellite bus.

![](_page_62_Figure_8.jpeg)

<span id="page-62-2"></span>**Figure 5-1: MOSAR Setup View in SpaceApps Laboratory Environment**

{63}------------------------------------------------

![](_page_63_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 63  
---
Demonstration Prodedures  

![](_page_63_Figure_4.jpeg)

![](_page_63_Figure_5.jpeg)

<span id="page-63-0"></span>![](_page_63_Figure_6.jpeg)

<span id="page-63-1"></span>**Figure 5-3: MOSAR setup side layout**

{64}------------------------------------------------

![](_page_64_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 64  
---
Demonstration Prodedures  

### <span id="page-64-0"></span>**Demonstrator Components**

The MOSAR demo setup can be mainly divided in two main groups that are the Ground Segment (MCC) and the Space Segment. On top of this, other side components are also integrated. This section lists the main components of each part.

### <span id="page-64-1"></span>**Ground Segment – Monitoring and Control Centre**

The MCC setup will be composed of three computers:

- The Design and FES PC, able to support the preparation of the spacecraft design and the simulation in communication with the planner. It is based on a standard PC (x86) with decent CPU and graphical performance, with Windows OS, running MATLAB/Simulink (design tool) and the DLR FES software.
- The Planning PC, running the Planner Agent (in association with the FES) to find a valid sequence of operation to re-configure the spacecraft. It will run on a standard PC (x86), with Linux OS (Ubuntu 18.04 or above), running ESROCOS and ERGO.
- The Monitoring and Control PC, to allow monitoring and controlling the demo setup. It will run on a standard PC (x86), with Linux OS (Ubuntu 18.04 or above), running ESROCOS and the PUS Console/Service. This unit could potentially be merged with the Planning PC.

These three computers will be interconnect on the same Ethernet network in order to enable the communication between them (e.g. UDP between FES and Planner) and with the Space Segment (PUS service between MCC and spacecraft OBCs to represent the data link).

The MCC will use the existing Space Applications Monitoring and Control infrastructure [\(Figure 5-4\)](#page-64-2). It is composed of a screen wall (3x55'' curved UHD Samsung), a large desk and series of smaller (touch) PC screens. A sub-set of these elements will be enough for the MOSAR setup application.

<span id="page-64-2"></span>![](_page_64_Picture_13.jpeg)

**Figure 5-4: MCC Setup and visualization screens**

{65}------------------------------------------------

![](_page_65_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 65   
---
Demonstration Prodedures  

### <span id="page-65-0"></span>**Space Segment**

Most of the Space Segment components are described in [RD6.](#page-8-4) It includes:

- The Servicer and Client Satellite platforms equipped with HOTDOCK standards interfaces. The servicer includes the OBC-S, which is responsible to manage the spacecraft re-configuration operations, with communication to the MCC and with the internal components of the Space Segment setup. It is based on an Intel NUC board, running ESROCOS/ERGO on top of a Linux operating system (Ubuntu 18.04). The OBC-S is powered through the nominal spacecraft power bus.
- The spacecraft modules that represent different functionalities of the client satellite. The SM1 module includes the OBC-C, which is responsible to manage the spacecraft nominal operations, with communication to the MCC and with the internal components of the Space Segment setup. It is based on an Intel NUC board, running ESROCOS/ERGO on top of a Linux operating system (Ubuntu 18.04). The OBC-S is powered through the nominal spacecraft power bus.

Most of the components embedded in the modules are powered through the nominal power bus. Some specific components, like the thermal heater is directly powered through the main supply. It is also always envisageable to power the two OBCs, also from the main supply, as backup solution.

- The walking manipulator that can move along the two spacecraft and manipulate the modules. It includes its own OBC, which is not interfaced through the standard Setup Ethernet network, but through the SpW link (due to its movable nature). It has however an Ethernet plug to enable direct connection to it, mainly for debugging purpose.
- The EGSE that provide the electrical components required to operate the system. This includes:
  - o The 48V bench power supply (range 600W-1kW) to provide the main power bus to the Space Segment (e.g. Keysight Technologies Digital Bench N6701C or equivalent)
  - o The Ethernet Switch that interconnects the FES, Planner, Monitoring and OBCs computers)
  - o The power plugs to connect side components to the main supply

![](_page_65_Picture_14.jpeg)

### **Figure 5-5: DC Bench power supply (Keysight or equivalent)**

<span id="page-65-1"></span> The Visual Subsystem, as described in [RD6.](#page-8-4) In order to support different scene configuration and lighting an occultation system will be considered around the setup. This is under investigation. The proposed approach would be to implement mate black curtains from the ceiling, around the setup (inside the safe zone). This is offering the advantage to present soft limits, in regards to WM operations and motions.

{66}------------------------------------------------

![](_page_66_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 66  
---
Demonstration Prodedures  

### <span id="page-66-0"></span>**Other Components**

Beside the ground and space segments, other components will be considered during the integration and demonstration activities:

- Each partner will provide specific tools to support low-level control of their components in support to the integration activities. This includes hardware and software that are used during their own local integration (not part of the demo setup).
- Standard electrical and mechanical tools and equipment to support the integration phase (e.g. multimeter, …)
- Safety equipment and devices as described in the following section
- Cameras for pictures and video recording along the integration and demonstration phases.

### <span id="page-66-1"></span>**Demonstrator Safety**

The main safety hazard of the setup is the operations of the Walking Manipulator when it is moving or manipulating the spacecraft modules. The purpose of the safety measure is to protect the human operators working around the setup, and as much as possible also the integrity of the setup hardware. Although the motion of the arm will be slow, different strategies will be implemented on the demonstration setup to ensure the safety of the operations:

- Electrical emergency stops will be integrated on the EGSE power line, accessible from the MCC, as well as from one or two other locations around the setup (e.g. also with a mobile switch, that can be worn by an operator). In case of major failure of the operations, that would allow to fully power off the space segment.
- Soft safety measures will be implemented at software level, based for instance on the interaction force/torque sensing on the WM. Other strategies will also be considered. The WM is equipped with brakes, which ensures it is keeping its position when powered-off.
- The reachability area of the WM (including manipulated SM) will be protected by security bands, such that the operator doesn't enter the area. The typical protection zone is illustrated in [Figure](#page-63-0)  [5-2.](#page-63-0) At this stage, we would like to not consider rigid protection such that the area can be better accommodated when the setup is not operational. We are currently evaluating the possibility to implement more active sensors (e.g. infrared/laser barrier), but the practicalities, efficiency and cost need to be evaluated.
- A flashing light will be installed near the Space Segment setup, to inform operators when the setup is powered-on.

{67}------------------------------------------------

![](_page_67_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 67  
---
Demonstration Prodedures  

# <span id="page-67-0"></span>**6 Annex**

### <span id="page-67-1"></span>**MOSAR Sequence of Manipulations Example**

The following table provides a possible step-by-step sequence of operations. covering the scenarios 1 and 2.

<span id="page-67-2"></span>

| Step 0: Initial Position                              | Step 0: Initial Position                              |
|-------------------------------------------------------|-------------------------------------------------------|
| Image: Robot at initial position with blocks arranged | Image: Robot at initial position with blocks arranged |
| Step 1: WM-A to CLT-B                                 | Step 1: WM-A to CLT-B                                 |
| Image: Robot moving from WM-A to CLT-B                | Image: Robot moving from WM-A to CLT-B                |
| Step 2: WM-B to SM3-BAT                               | Step 2: WM-B to SM3-BAT                               |
| Image: Robot moving from WM-B to SM3-BAT              | Image: Robot moving from WM-B to SM3-BAT              |

### **Table 6-1: Scenarios 1 and 2 step-by-step sequence of operations**

{68}------------------------------------------------

![](_page_68_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 68  
---
Demonstration Prodedures  

![](_page_68_Figure_4.jpeg)

![](_page_68_Figure_5.jpeg)

{69}------------------------------------------------

![](_page_69_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 69  
---
Demonstration Prodedures  

![](_page_69_Figure_4.jpeg)

{70}------------------------------------------------

![](_page_70_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 70  
---
Demonstration Prodedures  

![](_page_70_Figure_4.jpeg)

{71}------------------------------------------------

![](_page_71_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 71  
---
Demonstration Prodedures  

![](_page_71_Figure_4.jpeg)

{72}------------------------------------------------

![](_page_72_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 72  
---
Demonstration Prodedures  

![](_page_72_Figure_4.jpeg)

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* End of Document \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

End of Document

---

{73}------------------------------------------------

![](_page_73_Picture_0.jpeg)

Reference: MOSAR-WP3-D3.5-DLR  
Version: 1.1.0  
Date: 05-Aug-2020  
Page: 73  
---
Demonstration Prodedures  