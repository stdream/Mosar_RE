

{0}------------------------------------------------

![](_page_0_Picture_0.jpeg)

![](_page_0_Picture_3.jpeg)

![](_page_0_Picture_4.jpeg)

![](_page_0_Picture_5.jpeg)

| Deliverable Reference | :<br>D1.4                                                                                                                                                                                                |
|-----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Title                 | :<br>System Requirements Document                                                                                                                                                                        |
| Confidentiality Level | :<br>PU                                                                                                                                                                                                  |
| Lead Partner          | :<br>Space Applications Services                                                                                                                                                                         |
| Abstract              | :<br>This document presents<br>the system requirements<br>for MOSAR that were derived from the application<br>and technology review, and the analysis of the<br>operational and demonstration scenarios. |
| EC Grant<br>N°        | :<br>821996                                                                                                                                                                                              |
| Project Officer EC    | :<br>Christos Ampatzis (REA)                                                                                                                                                                             |
|                       |                                                                                                                                                                                                          |

![](_page_0_Picture_7.jpeg)

MOSAR is co-funded by the Horizon 2020 Framework Programme of the European Union

{1}------------------------------------------------

{2}------------------------------------------------

![](_page_2_Picture_0.jpeg)

| DOCUMENT APPROVAL SHEET          |      |                                                                                                                                                                                |            |  |
|----------------------------------|------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|--|
|                                  | Name | Organization                                                                                                                                                                   | Date       |  |
| Prepared and<br>cross-review by: |      | Space Applications Services<br>Thales Alenia Space France<br>Thales Alenia Space UK<br>SITAEL<br>GMV<br>University of Strathclyde<br>German Aerospace Centre (DLR)<br>MAG SOAR | 28/06/2019 |  |

{3}------------------------------------------------

![](_page_3_Picture_0.jpeg)

| DOCUMENT CHANGE RECORD |            |                                 |                                                                                  |                                                                                                 |
|------------------------|------------|---------------------------------|----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| Version                | Date       | Author                          | Changed<br>Sections / Pages                                                      | Reason for Change / RID No                                                                      |
| 0.9.0                  | 28/06/2019 | Partners                        | All                                                                              | Initial delivery for SRR review                                                                 |
| 1.0.0                  | 01/09/2019 | Space<br>Applications<br>USTRAT | Section 2.2.1<br>48<br>Section 2.2.2<br>(FuncR_S118)<br>OG09-49<br>Section 2.2.3 | Added section based on RID OG09-<br>Comment removed based on RID<br>Edited based on RID OG09-50 |
|                        |            |                                 | (PerfR_S201/202)<br>Section 2.2.7<br>Section 3.3.1<br>(FuncR_A113-<br>116, B103) | Edited based on RID OG09-51<br>Edited based on RID OG09-53                                      |

{4}------------------------------------------------

![](_page_4_Picture_0.jpeg)

# **Contents**

| 1 |     |                                     | Introduction  8                                                |  |  |  |  |
|---|-----|-------------------------------------|----------------------------------------------------------------|--|--|--|--|
|   | 1.1 | Purpose and Scope 8                 |                                                                |  |  |  |  |
|   | 1.2 | Document Structure  8               |                                                                |  |  |  |  |
|   | 1.3 |                                     | Applicable Documents 8                                         |  |  |  |  |
|   | 1.4 |                                     | Reference Documents 8                                          |  |  |  |  |
|   | 1.5 |                                     | Acronyms 9                                                     |  |  |  |  |
| 2 |     |                                     | Modular Spacecraft Requirements 10                             |  |  |  |  |
|   | 2.1 | Mission Overview  10                |                                                                |  |  |  |  |
|   | 2.2 |                                     | Space Scenarios Requirements 12                                |  |  |  |  |
|   |     | 2.2.1                               | Formalism 12                                                   |  |  |  |  |
|   |     | 2.2.2                               | S100: Functional requirements [FuncR] 13                       |  |  |  |  |
|   |     | 2.2.3                               | S200: Performance requirements [PerfR]  20                     |  |  |  |  |
|   |     | 2.2.4                               | S300: Interface requirements [IntRD] 21                        |  |  |  |  |
|   |     | 2.2.5                               | S400: Design requirements [DesR] 22                            |  |  |  |  |
|   |     | 2.2.6                               | S500: Physical and resource requirements [PhyR] 23             |  |  |  |  |
|   |     | 2.2.7                               | S600: Environmental and Operational requirements [OpR] 23      |  |  |  |  |
|   |     | 2.2.8                               | S700: Safety requirements [SafR] 25                            |  |  |  |  |
|   |     | 2.2.9                               | S800: Configuration and implementation requirements [ConfR] 29 |  |  |  |  |
| 3 |     | MOSAR Demonstrator Requirements  31 |                                                                |  |  |  |  |
|   | 3.1 |                                     | Demonstrator Overview 31                                       |  |  |  |  |
|   | 3.2 | Formalism 32                        |                                                                |  |  |  |  |
|   | 3.3 |                                     | System Requirements [Axxx]  33                                 |  |  |  |  |
|   |     | 3.3.1                               | A100: Functional requirements [FuncR] 33                       |  |  |  |  |
|   |     | 3.3.2                               | A200: Performance requirements [PerfR]  37                     |  |  |  |  |
|   |     | 3.3.3                               | A300: Interface requirements [IntR]  39                        |  |  |  |  |
|   |     | 3.3.4                               | A400: Design requirements [DesR] 40                            |  |  |  |  |
|   |     | 3.3.5                               | A500: Physical and resource requirements [PhyR] 42             |  |  |  |  |
|   |     | 3.3.6                               | A600: Environmental and Operational requirements [OpR] 42      |  |  |  |  |
|   |     | 3.3.7                               | A700: Safety requirements [SafR] 43                            |  |  |  |  |
|   |     | 3.3.8                               | A800: Configuration and implementation requirements [ConfR] 43 |  |  |  |  |
|   | 3.4 |                                     | Walking Manipulator Requirements [Bxxx]  45                    |  |  |  |  |
|   |     | 3.4.1                               | B100: Functional requirements [FuncR] 45                       |  |  |  |  |
|   |     | 3.4.2                               | B200: Performance requirements [PerfR]  47                     |  |  |  |  |
|   |     | 3.4.3                               | B300: Interface requirements [IntR]  48                        |  |  |  |  |
|   |     | 3.4.4                               | B400: Design requirements [DesR] 50                            |  |  |  |  |

{5}------------------------------------------------

![](_page_5_Picture_0.jpeg)

|     | 3.4.5                                         | B500: Physical and resource requirements [PhyR] 52             |  |  |
|-----|-----------------------------------------------|----------------------------------------------------------------|--|--|
|     | 3.4.6                                         | B600: Environmental and Operational requirements [OpR] 52      |  |  |
|     | 3.4.7                                         | B700: Safety requirements [SafR] 52                            |  |  |
|     | 3.4.8                                         | B800: Configuration and implementation requirements [ConfR] 52 |  |  |
| 3.5 |                                               | Spacecraft Modules Requirements [Cxxx]  53                     |  |  |
|     | 3.5.1                                         | C100: Functional requirements [FuncR] 53                       |  |  |
|     | 3.5.2                                         | C200: Performance requirements [PerfR]  55                     |  |  |
|     | 3.5.3                                         | C300: Interface requirements [IntR]  56                        |  |  |
|     | 3.5.4                                         | C400: Design requirements [DesR] 57                            |  |  |
|     | 3.5.5                                         | C500: Physical and resource requirements [PhyR] 60             |  |  |
|     | 3.5.6                                         | C600: Environmental and Operational requirements [OpR] 61      |  |  |
|     | 3.5.7                                         | C700: Safety requirements [SafR] 61                            |  |  |
|     | 3.5.8                                         | C800: Configuration and implementation requirements [ConfR] 61 |  |  |
| 3.6 |                                               | Standard Interfaces Requirements [Dxxx]  62                    |  |  |
|     | 3.6.1                                         | D100: Functional requirements [FuncR] 62                       |  |  |
|     | 3.6.2                                         | D200: Performance requirements [PerfR]  64                     |  |  |
|     | 3.6.3                                         | D300: Interface requirements [IntR]  66                        |  |  |
|     | 3.6.4                                         | D400: Design requirements [DesR] 67                            |  |  |
|     | 3.6.5                                         | D500: Physical requirements [PhyR] 68                          |  |  |
|     | 3.6.6                                         | D600: Environmental and Operational requirements [OpR] 69      |  |  |
|     | 3.6.7                                         | D700: Safety requirements [SafR] 70                            |  |  |
|     | 3.6.8                                         | D800: Configuration and implementation requirements [ConfR] 70 |  |  |
| 3.7 | Planner and Simulator Requirements [Exxx]  71 |                                                                |  |  |
|     | 3.7.1                                         | E100: Functional requirements [FuncR] 71                       |  |  |
|     | 3.7.2                                         | D200: Performance requirements [PerfR]  73                     |  |  |
|     | 3.7.3                                         | D300: Interface requirements [IntR]  73                        |  |  |
|     | 3.7.4                                         | D400: Design requirements [DesR] 74                            |  |  |
|     | 3.7.5                                         | D500: Physical and resource requirements [PhyR] 75             |  |  |
|     | 3.7.6                                         | D600: Environmental and Operational requirements [OpR] 75      |  |  |
|     | 3.7.7                                         | D700: Safety requirements [SafR] 75                            |  |  |
|     | 3.7.8                                         | D800: Configuration and implementation requirements [ConfR] 75 |  |  |
| 3.8 |                                               | Software Requirements [Fxxx]  76                               |  |  |
|     | 3.8.1                                         | F100: Functional requirements [FuncR]  76                      |  |  |
|     | 3.8.2                                         | F200: Performance requirements [PerfR]  77                     |  |  |
|     | 3.8.3                                         | F300: Interface requirements [IntR] 78                         |  |  |
|     | 3.8.4                                         | F400: Design requirements [DesR]  78                           |  |  |

{6}------------------------------------------------

![](_page_6_Picture_0.jpeg)

| 4   |  |       | Conclusions 83                                                  |  |  |
|-----|--|-------|-----------------------------------------------------------------|--|--|
| 3.9 |  |       | Validation Requirements [Gxxx] 80                               |  |  |
|     |  | 3.8.8 | F800: Configuration and implementation requirements [ConfR]  79 |  |  |
|     |  | 3.8.7 | F700: Safety requirements [SafR]  78                            |  |  |
|     |  | 3.8.6 | F600: Environmental and Operational requirements [OpR]  78      |  |  |
|     |  | 3.8.5 | F500: Physical and resource requirements [PhyR] 78              |  |  |
|     |  |       |                                                                 |  |  |

{7}------------------------------------------------

![](_page_7_Picture_0.jpeg)

# **List of Figures**

| Figure 2-1 - Schematic view of a MOSAR-like mission 11 |  |
|--------------------------------------------------------|--|
| Figure 3-1: MOSAR Demonstrator Concept 31              |  |

{8}------------------------------------------------

![](_page_8_Picture_0.jpeg)

# **List of Tables**

| Table 1: Example of requirement  12 |  |
|-------------------------------------|--|
| Table 2: Example of requirement  32 |  |

{9}------------------------------------------------

![](_page_9_Picture_0.jpeg)

# <span id="page-9-0"></span>**1 Introduction**

# <span id="page-9-1"></span>**1.1 Purpose and Scope**

The purpose of this document is to provide the system requirements for MOSAR that are derived from the from the SRC Compendium document, the analysis of the modular spacecraft applications and relevant technology review (including previous OGs building blocks), the MOSAR operational concept and the demonstration scenarios.

The document is mainly divided in two parts. The first part addresses the extraction of requirements associated with future space mission scenarios of modular spacecraft applications. They are mainly derived from the analysis of the most promising use cases of On-orbit reconfiguration and the associated technological needs [\(RD2-](#page-9-5)D1.2). These requirements are considered as guidelines for the development of the MOSAR demonstrator, to target a good representativeness of future missions.

The second part addresses more specifically the technical requirements of the MOSAR demonstrator that will be designed, developed and tested during this activity. The requirements are described at system level, for each of the main sub-systems and for the validation phase.

# <span id="page-9-2"></span>**1.2 Document Structure**

This document is structured as follows:

- **Section 1** Introduction
- **Section 2** Modular Spacecraft Requirements
- **Section 3** MOSAR Demonstrator Requirements

# <span id="page-9-3"></span>**1.3 Applicable Documents**

- <span id="page-9-7"></span>AD1 SRC – Guidance Document for H2020 Work Programe 2018-2020 (SPACE-12-TEC-2018)
- AD2 MOSAR Consortium Agreement, version 1.0 (7th November 2018)
- <span id="page-9-6"></span>AD3 MOSAR Grant Agreement (821996) (18th January 2019)
- AD4 MOSAR Proposal; H2020-SPACE-2018-2020 (SEP-210504862)

# <span id="page-9-4"></span>**1.4 Reference Documents**

- <span id="page-9-9"></span>RD1 MOSAR-WP1-D1.1-GMV OG1-5 Building Block Update Documentation Package
- <span id="page-9-5"></span>RD2 MOSAR-WP1-D1.2-TASF Report on MOSAR Applicable Technologies Review
- <span id="page-9-8"></span>RD3 MOSAR-WP1-D1.3-DLR Operational Concept

{10}------------------------------------------------

![](_page_10_Picture_0.jpeg)

# <span id="page-10-0"></span>**1.5 Acronyms**

| APM       | Active Payload Module                                                               |
|-----------|-------------------------------------------------------------------------------------|
| ASM       | Active System Module                                                                |
| CAN       | Controller Area Network                                                             |
| CLT       | Client (spacecraft)                                                                 |
| DDS       | Data Distribution Service                                                           |
| ERGO      | European Robotic Goal-Oriented Autonomous Controller                                |
| ESA       | European Space Agency                                                               |
| ESROCOS   | European Space Robotics Control and Operating System                                |
| FES       | Functional Engineering Simulator                                                    |
| FM        | Functional Module                                                                   |
| GEO       | Geostationary Earth Orbit                                                           |
| GTO       | Geostationary Transfer Orbit                                                        |
| I3DS      | Integrated 3D Sensors                                                               |
| InFuse    | Infusing Data Fusion in Space Robotics                                              |
| LEO       | Low Earth Orbit                                                                     |
| MCC       | Monitoring and Control Center                                                       |
| MOSAR     | Modular Spacecraft Assembly and Reconfiguration                                     |
| OBC       | On-Board Computer                                                                   |
| OG        | Operational Grant                                                                   |
| PERASPERA | Plan the European Roadmap and its Activities for Space Exploitation of Robotics and |
|           | Autonomy                                                                            |
| PUS       | Packet Utilization Standard                                                         |
| R-ICU     | Reduced Instrument Control Unit                                                     |
| SI        | Standard Interface                                                                  |
| SIROM     | Standard Interface for Robotic Manipulation of Payloads in Future Space Missions    |
| SM        | Spacecraft Modules                                                                  |
| SpW       | SpaceWire                                                                           |
| SRC       | Strategic Research Cluster                                                          |
| SVC       | Servicer (spacecraft)                                                               |
| TASTE     | The ASSERT Set of Tools for Engineering                                             |
| TBC       | To be Confirmed                                                                     |
| TBD       | To be Defined                                                                       |
| TC        | Telecommand                                                                         |
| TM        | Telemetry                                                                           |
| WM        | Walking Manipulator                                                                 |
|           |                                                                                     |

{11}------------------------------------------------

![](_page_11_Picture_0.jpeg)

# <span id="page-11-0"></span>**2 Modular Spacecraft Requirements**

# <span id="page-11-1"></span>**2.1 Mission Overview**

The selection of the MOSAR space mission application has to be done in perspective with the other space mission applications selected for PULSAR and for EROSS:

- PULSAR space mission will consist in assembling a large telescope at Earth-Sun L2 point using a robotic manipulator, with all the telescope and platform elements packaged in a single launch.
- EROSS space mission will consist in the in-space servicing of a LEO satellite, with refueling and units replacement, using state-of-the-art robotic arm and equipment.

Following the analysis of [RD2,](#page-9-5) a mission concept is proposed that exploits at best the benefits of the modular approach, that is realistically feasible in the short/mid-term and that is commercially oriented towards the reduction of costs and the maximization of profit.

The proposed MOSAR space mission application consists in upgrading, reconfiguring and repairing an operational GEO telecommunication satellite.

The satellite, in its original configuration, will have an initial telecommunication payload capacity and will be assembled and tested on-ground, but it will feature key design concepts to meet the mission objective:

# **Modular design:**

The satellite original configuration will be based on the conventional all-integrated platform, but will feature some specific modules, removable from the outside of the satellite, dedicated to power generation (solar array + power conditioning) and payloads.

# **Scalable design:**

The satellite original configuration will allow in-space connection of additional modules through standard interfaces at the outside of the satellite.

The mission is divided into 3 different phases:

Phase 1: launch of satellite with initial capacity

The satellite is assembled and tested on-ground and is launched fully integrated into a GTO. The satellite then uses its own propulsion system to raise its orbit to reach its GEO position slot.

After in-orbit tests and commissioning, the satellite is capable to deliver an initial capacity (e.g. high throughput internet connection).

Phase 2: capacity increase + upgrade of payload + addition of hosted payload

After several years in-orbit (approximately 5 years), there is a need coming from the market to upgrade the payload (removal of obsolete technologies) and to add telecommunication capacity to the existing satellite, while also adding an hosted payload for meteorology on the Earth pointing panel to increase financial revenues and profitability.

{12}------------------------------------------------

![](_page_12_Picture_0.jpeg)

Dedicated modules (power generation module, payload modules, hosted payload module) will be manufactured, tested on-ground and launched into GTO (can be a co-passenger with another GEO satellite). A servicer equipped with a robotic arm and positioned near the GTO injection point, will then capture the modules, bring them to the satellite operational orbit (i.e. perform an orbit raising and insertion into GEO slot of its client) where it will assemble them with the following sequence:

- o Addition of power generation module and in-orbit tests for verification of performances
- o Removal and storage of obsolete payload modules
- o Replacement of obsolete payload modules and in-orbit tests for verification of performances
- o Addition of telecommunication payload modules and in-orbit tests for verification of performances
- o Addition of hosted payload module and in-orbit tests for verification of performances

## Phase 3: replacement of failed battery + addition of deorbiting propulsion kit

After additional years of operations, failure of parts subjected to ageing (e.g. battery, thrusters) occurred preventing the satellite from operating nominally and performing specific station keeping maneuvers (e.g. E/W or N/S).

Dedicated modules (battery module, propulsion kit) are manufactured, tested on-ground and launched as co-passenger to another GTO mission. As for Phase 2, a servicer will capture and bring them to the satellite operational orbit and perform the modules exchange.

![](_page_12_Figure_13.jpeg)

<span id="page-12-0"></span>**Figure 2-1 - Schematic view of a MOSAR-like mission.**

{13}------------------------------------------------

![](_page_13_Picture_0.jpeg)

This mission concept is proposed as an example, to guide the development of the demonstrator. However it should not limit in any way the applicability of MOSAR to any other kind of mission.

MOSAR is a project aiming at demonstrating a set of key technologies that are considered essential for the development of future applications of On-Orbit Servicing and On-Orbit Assembly. The objectives of MOSAR include [\(AD3\)](#page-9-6):

- Review, extension and integration of common robotic building blocks: ESROCOS, ERGO and InFuse software building blocks; I3DS perception suite and SIROM standard interface.
- Development of a repositionable walking manipulator, enabling a cost-effective solution for actuation on a wide workspace without escalation of size and performance of the robot.
- Elaboration of a concept for modular spacecraft: identifying key design choices and highlighting recommendations for development of standards for design and operation of future modular space vehicles.

The first two objectives should be generic and independent from any specific mission, as the final purpose is to develop a standard that is unique and re-usable across different missions. As for the third objective, the applicability of the modular approach to different missions is discussed in [RD2,](#page-9-5) highlighting the main advantages that modularity would bring to specific applications and the main design and operation requirement that would need to be fulfilled.

# <span id="page-13-0"></span>**2.2 Space Scenarios Requirements**

MOSAR does not target a specific mission in particular, but rather aims at demonstrating key functionalities that are intended to be generic and applicable to very different scenarios. Therefore, it has been preferred not to restrain MOSAR applicability to a given mission, but to present general requirements that can be common to multiple missions. These requirements are not expected to be fully verified in the context of the current project. They should be considered as guidelines for the developments in the current activity to favor compatibility with future mission goals and requirements.

# <span id="page-13-1"></span>**2.2.1 Formalism**

The following section details the space scenarios requirements following the structure exemplified in this table:

<span id="page-13-2"></span>

| YY_uniqueID | Title                               | LEVEL |
|-------------|-------------------------------------|-------|
| STATEMENT   | Requirement Statement               |       |
| COVERS      | Origin                              |       |
| COMMENT     | Additional comment and explanations |       |

## **Table 1: Example of requirement**

The top row of the table includes:

- Unique ID: identificator with the structure YY\_uniqueID
  - YY: type of the requirement Functional requirements (FuncR), Performance requirements (PerfR), Interface requirements (IntR), …
  - uniqueID: unique reference with 4 characters:
    - The first character is a "S", for Space Scenarios Requirements
    - The next number identifies the type of requirement inside the subsystem

{14}------------------------------------------------

![](_page_14_Picture_0.jpeg)

- The next two numbers identify a number assigned to each requirement in that category
- Title: highlighting the topic of the requirement
- LEVEL: indicates the level of importance of the requirement (mandatory / desirable / optional)

The rest of the table includes the following fields:

- STATEMENT: clear and concise description of the requirement
- COVERS: gives indication about the origin/scope of the requirements (specific user requirement or user case, partner expertise, project constraint, etc.)
- COMMENT: provides rationale or additional comments about the requirement

# <span id="page-14-0"></span>**2.2.2 S100: Functional requirements [FuncR]**

| FuncR_S101 | Satellite repair and update                                                                                                                                    | Mandatory |
|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | The MOSAR technology shall allow repair and update of modular spacecraft by<br>manipulation and repositioning of functional modules with a robotic manipulator |           |
| COVERS     | Mission analysis RD2<br>Guidelines AD1-OG9-R02                                                                                                                 |           |
| COMMENT    |                                                                                                                                                                |           |

| FuncR_S102 | Mission tasks update                                                                                                                                                               | Mandatory |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | The modular spacecraft shall be reconfigurable and should be able to use new<br>functionalities brought by additional functional modules, in order to perform new mission<br>tasks |           |
| COVERS     | Mission analysis RD2<br>Guidelines AD1-OG9-R05                                                                                                                                     |           |
| COMMENT    |                                                                                                                                                                                    |           |

| FuncR_S103 | Functional modules replacement                                                                                                                | Mandatory |
|------------|-----------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | The robotic manipulator shall be able to add and replace whole functional modules<br>(ASM/APM) by using the interconnectors of these modules. |           |
| COVERS     | Mission analysis RD2<br>Guidelines AD1-OG9-R01                                                                                                |           |
| COMMENT    |                                                                                                                                               |           |

{15}------------------------------------------------

![](_page_15_Picture_0.jpeg)

| STATEMENT | The robotic manipulator shall be able to reposition itself by using the<br>interconnectors/structure of the functional modules or the spacecraft |
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| COVERS    | Mission analysis RD2<br>Guidelines AD1-OG9-R03                                                                                                   |
| COMMENT   |                                                                                                                                                  |

| FuncR_S105 | Design software                                                                                                               | Mandatory |
|------------|-------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | A design software shall be able to create a robotic compatible servicing / reconfiguration<br>plan for the modular spacecraft |           |
| COVERS     | Operational Concept RD3<br>Guidelines AD1-OG9-R12                                                                             |           |
| COMMENT    |                                                                                                                               |           |

| FuncR_S106 | Simulation software                                                                                                           | Mandatory |
|------------|-------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | A simulation software shall be able to simulate the system with all related robotics<br>elements following the execution plan |           |
| COVERS     | Operational Concept RD3<br>Guidelines AD1-OG9-R12                                                                             |           |
| COMMENT    |                                                                                                                               |           |

{16}------------------------------------------------

![](_page_16_Picture_0.jpeg)

| FuncR_S107 | Robot high-level control                                                                                                                              | Mandatory |
|------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | The modular spacecraft shall perform the high-level control of the robot, by the<br>execution and monitoring of the reconfiguration plan (task level) |           |
| COVERS     | Operational Concept RD3<br>Guidelines AD1-OG9-R04                                                                                                     |           |
| COMMENT    | The high-level control of the robot can also be managed by the servicer satellite<br>(depending on the servicing or local reconfiguration scenario)   |           |

| FuncR_S108 | Robot low-level control                                                                                 | Mandatory |
|------------|---------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | The robotic manipulator shall ensure its low-level control for the execution of the high<br>level tasks |           |
| COVERS     | Operational Concept RD3<br>Guidelines AD1-OG9-R04                                                       |           |
| COMMENT    |                                                                                                         |           |

| FuncR_S109 | Functional module monitoring                                                                                              | Mandatory |
|------------|---------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | The modular spacecraft shall be able to monitor the status of essential parameters of<br>each connected functional module |           |
| COVERS     | Mission analysis RD2<br>Guidelines AD1-OG9-R12                                                                            |           |
| COMMENT    |                                                                                                                           |           |

| FuncR_S110 | Resources reallocation                                                                                                                                                                           | Mandatory |
|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | The system shall be able to reallocate resources (e.g. power, data, computational<br>power, etc.) and assign different path automatically in case of a defect (e.g.<br>interconnector of an APM) |           |
| COVERS     | Mission analysis RD2<br>Guidelines AD1-OG9-R07                                                                                                                                                   |           |
| COMMENT    |                                                                                                                                                                                                  |           |

{17}------------------------------------------------

![](_page_17_Picture_0.jpeg)

| FuncR_S111 | Failure handling                                                                                                                            | Mandatory |
|------------|---------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | The system shall be able to handle the tasks even during a connection failure or a<br>power interruption of defect modules/interconnectors. |           |
| COVERS     | Mission analysis RD2<br>Guidelines AD1-OG9-R08                                                                                              |           |
| COMMENT    |                                                                                                                                             |           |

| FuncR_S112 | Electrical power supply                                                                                                                                              | Mandatory |
|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | One or several modules options shall be available to implement for electrical power<br>supply enabling operation of the functional modules and the robot manipulator |           |
| COVERS     | Mission analysis RD2                                                                                                                                                 |           |
| COMMENT    | The power system could be integrated by one or more functional modules                                                                                               |           |

| FuncR_S113 | Electrical power supply, power management                                                                                                                                                                                                | Mandatory |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | The modular spacecraft shall be able to shut down or command a stand-by mode of any<br>non-critical module to reduce power consumption if needed.<br>Critical functions should not be affected by shutting down of non-critical modules. |           |
| COVERS     | Mission analysis RD2                                                                                                                                                                                                                     |           |
| COMMENT    |                                                                                                                                                                                                                                          |           |

| FuncR_S114 | Data handling system                                                                                                                                                                                           | Mandatory |
|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | One or several modules options shall be available to implement a data handling system<br>(that can be composed of one or more modules) that enables operation of the different<br>modules and the manipulator. |           |
| COVERS     | Mission analysis RD2                                                                                                                                                                                           |           |
| COMMENT    | The data handling system could be integrated by one or more functional modules                                                                                                                                 |           |

{18}------------------------------------------------

![](_page_18_Picture_0.jpeg)

| FuncR_S115 | Heat management and thermal considerations                                                                                                                                                                                                                               | Mandatory |
|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | One or several modules options shall be available to implement heat management<br>functions that allow thermal regulation of the different modules within its specific range<br>of temperatures. The heat management system could be composed of one or more<br>modules. |           |
| COVERS     | Mission analysis RD2                                                                                                                                                                                                                                                     |           |
| COMMENT    |                                                                                                                                                                                                                                                                          |           |

| FuncR_S116 | Propulsion subsystem                                                                                                                                                                                           | Mandatory |
|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | One or several modules options shall be available to implement a propulsion subsystem<br>with capacity to perform at least:<br><br>Station keeping manoeuvers.<br><br>Orbit relocation.<br><br>De-orbiting. |           |
| COVERS     | Mission analysis RD2                                                                                                                                                                                           |           |
| COMMENT    | The propulsion subsystem could be integrated by one or more functional modules.                                                                                                                                |           |

| FuncR_S117 | Attitude control subsystem                                                                                                                                                                                                                                                            | Mandatory |
|------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | One or several modules options shall be available to implement an attitude control<br>subsystem, with capacity to perform at least:<br><br>Spacecraft reorientation.<br><br>Attitude control compatible with mission objectives.<br><br>Autonomous search of the Sun and the Earth |           |
| COVERS     | Mission analysis RD2                                                                                                                                                                                                                                                                  |           |
| COMMENT    | The attitude control subsystem is essential to ensure correct functioning of other<br>subsystems.                                                                                                                                                                                     |           |

| FuncR_S118 | Module mechanical connections                                                                                                                                                      | Mandatory |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | Modules shall be able to connect mechanically to other modules or to the spacecraft<br>through interconnectors.                                                                    |           |
| COVERS     | Mission analysis RD2                                                                                                                                                               |           |
| COMMENT    | Not every module is directly linked to the OBC of the modular platform. Data relay<br>function is needed to dispatch telecommands and telemetries through a network of<br>modules. |           |

{19}------------------------------------------------

![](_page_19_Picture_0.jpeg)

| FuncR_S119 | Module data relay                                                                                                                                                                                                                               | Mandatory |
|------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | Any module should be able to act as a data relay for other modules or the robotic<br>manipulator through their interconnector, also if the module is in safe mode                                                                               |           |
| COVERS     | Mission analysis RD2                                                                                                                                                                                                                            |           |
| COMMENT    | Not every module is directly linked to the OBC of the modular platform. Data relay<br>function is needed to dispatch telecommands and telemetries through a network of<br>modules.<br>FM1 is in safe mode but still acts as data relay for FM2. |           |

| FuncR_S120 | Data routing                                                                                                                                                                                                                                                                                                                  | Mandatory |
|------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | The OBC shall be able to redirect telecommands to specific modules, for the spacecraft<br>configuration or for instance upon detection of failure on any point of the network.<br>If an alternative path is not available, the OBC shall be able to isolate the faulty node<br>and all the others nodes connected downstream. |           |
| COVERS     | Mission analysis RD2                                                                                                                                                                                                                                                                                                          |           |
| COMMENT    | FM5 has a nominal link to the OBC through FM3 and FM4. In case of failure of any of<br>these components, the OBC should redirect telecommands to FM5 through the alternative<br>path using FM1 and FM2.                                                                                                                       |           |

{20}------------------------------------------------

![](_page_20_Picture_0.jpeg)

![](_page_20_Figure_4.jpeg)

| FuncR_S121 | Module power relay                                                                                                                                              | Mandatory |
|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | Module should be able to act as a power relay for other modules or the robotic<br>manipulator through their interconnectors, also if the module is in safe mode |           |
| COVERS     | Mission analysis RD2<br>FuncR_S112                                                                                                                              |           |
| COMMENT    | To allow power distribution between the power supply (spacecraft or functional module)<br>and the other active modules                                          |           |

| FuncR_S122 | Power routing                                                                                                                                                                                                                                                                                                                | Mandatory |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | The OBC shall be able to redirect power to specific modules, for the spacecraft<br>configuration or for instance upon detection of power failure on any point of the network.<br>If an alternative path is not available, the OBC shall be able to isolate the faulty node<br>and all the others nodes connected downstream. |           |
| COVERS     | Mission analysis RD2                                                                                                                                                                                                                                                                                                         |           |
| COMMENT    | To allow power distribution between the power supply (spacecraft or functional module)<br>and the other active modules                                                                                                                                                                                                       |           |

{21}------------------------------------------------

![](_page_21_Picture_0.jpeg)

| FuncR_S123 | Module thermal relay                                                                               | Mandatory |
|------------|----------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | Module should be able to act as a thermal relay for other modules through their<br>interconnectors |           |
| COVERS     | Mission analysis RD2<br>FuncR_S115                                                                 |           |
| COMMENT    | To allow thermal distribution and management between the modules                                   |           |

# <span id="page-21-0"></span>**2.2.3 S200: Performance requirements [PerfR]**

Performance requirements are specific to each application. Detailed mission analysis is needed to adapt the generic requirements presented hereafter to the specific need of the mission.

| PerfR_S201 | Mechanical interfaces                                                                                                                                                                                       | Mandatory |
|------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | The modular spacecraft shall be able to withstand the loads expected on orbit with<br>significant (TBD) safety margins.<br>In any case, the mechanical integrity of the ensemble should not be compromised. |           |
| COVERS     | Mission analysis RD2                                                                                                                                                                                        |           |
| COMMENT    |                                                                                                                                                                                                             |           |

| PerfR_S202 | Manipulator mechanical loads                                                                                                                                                                                                                                                                                                            | Mandatory |
|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | The robot manipulator and its connections to the modules or spacecraft shall be able to<br>withstand the loads expected during modules operations with significant (TBC) safety<br>margins.<br>In any case, the mechanical integrity of the robotic arm and its connection with the<br>spacecraft or modules should not be compromised. |           |
| COVERS     | Mission analysis RD2                                                                                                                                                                                                                                                                                                                    |           |
| COMMENT    |                                                                                                                                                                                                                                                                                                                                         |           |

| PerfR_S203 | Mechanical interfaces (alignment and stiffness)                                                                                                                                                                                                                                                                              | Mandatory |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | The mechanical interfaces of the modular spacecraft shall provide the required<br>alignment accuracy and stiffness required by the different modules to meet their<br>respective performance requirements and to not constitute a harm to the rest of the<br>spacecraft.                                                     |           |
| COVERS     | Mission analysis RD2                                                                                                                                                                                                                                                                                                         |           |
| COMMENT    | The performance requirements of the different modules could be treated at system<br>level, showing adequacy to the mission objectives.<br>The minimum need in terms of alignment and stiffness of the mechanical interface<br>should at least guarantee that every module is safely integrated into the modular<br>platform. |           |

{22}------------------------------------------------

![](_page_22_Picture_0.jpeg)

#### <span id="page-22-0"></span>**2.2.4 S300: Interface requirements [IntRD]**

| IntR_S301 | Ground segment communication                                                                                                | Mandatory |
|-----------|-----------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | The modular spacecraft shall have a redundant communication link with the ground<br>segment for telemetry and telecommands. |           |
| COVERS    | Mission analysis RD2                                                                                                        |           |
| COMMENT   |                                                                                                                             |           |

| IntR_S302 | Telemetry of different modules                                                                                                                                                                                                                                                               | Mandatory |
|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | Every module shall have a communication link enabling to send telemetry to the<br>spacecraft monitoring unit (OBC) and ultimately to the ground station. The link with the<br>ground station could be done through a specific communication module implemented on<br>the modular spacecraft. |           |
| COVERS    | Mission analysis RD2                                                                                                                                                                                                                                                                         |           |
| COMMENT   |                                                                                                                                                                                                                                                                                              |           |

| IntR_S303 | Ground segment surveillance                                                                                                                                                                                                                                                                                                                         | Mandatory |
|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | The ground segment shall know at any moment the status of the different modules of<br>the modular spacecraft. This information is passed through two types of telemetries:<br><br>Periodic telemetry with standardized packets.<br><br>Asynchronous telemetry with error message.                                                                 |           |
| COVERS    | Mission analysis RD2                                                                                                                                                                                                                                                                                                                                |           |
| COMMENT   | The ground segment is able to detect problems in case an anomaly message is<br>received (asynchronous telemetry). Even if the error message is never received (for<br>instance, sudden power loss), the ground segment is able to detect a problem if the<br>periodic telemetry is not received and investigate the problem by analyzing this data. |           |

| IntR_S304 | Grounding (electrical power)                                                                                            | Mandatory |
|-----------|-------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | Any module of the modular spacecraft provided with an electrical power interface should<br>have a connection to ground. |           |
| COVERS    | Mission analysis RD2                                                                                                    |           |
| COMMENT   | Reduces the risk of introducing stray currents or ground loop currents.                                                 |           |

{23}------------------------------------------------

![](_page_23_Picture_0.jpeg)

#### <span id="page-23-0"></span>**2.2.5 S400: Design requirements [DesR]**

| DesR_S401 | Modular satellite reliability                                                                                                                                                                                                 | Desirable |
|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | The modular spacecraft shall be quantifiably more reliable by design than a monolithic<br>system over the mission lifetime of the satellite, including (and as a specific advantage)<br>under extensions of mission lifetime. |           |
| COVERS    | Mission analysis RD2                                                                                                                                                                                                          |           |
| COMMENT   |                                                                                                                                                                                                                               |           |

| DesR_S402 | Modular satellite flexibility                                                                                                                                     | Desirable |
|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | The modular spacecraft shall be quantifiably more flexible in operation and responsive<br>to mission changes than a traditional satellite with a similar mission. |           |
| COVERS    | Mission analysis RD2                                                                                                                                              |           |
| COMMENT   |                                                                                                                                                                   |           |

| DesR_S403 | Modular satellite economy                                                                                                                                                                                                                                                                                                    | Desirable |
|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | The modular spacecraft shall have quantifiable advantages in cost-effectiveness and<br>economy of operation from a mission perspective over the projected lifetime of the<br>satellite.<br>Otherwise, it should be demonstrated that the benefits (in terms of enhanced<br>functionalities) compensate the additional costs. |           |
| COVERS    | Mission analysis RD2                                                                                                                                                                                                                                                                                                         |           |
| COMMENT   |                                                                                                                                                                                                                                                                                                                              |           |

| DesR_S404 | Available connection interfaces                                                                                                                                                                                                   | Mandatory |
|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | The modular spacecraft and modules assembly shall implement a minimum number of<br>connection interfaces such as at least two of these interfaces are available at any<br>moment and within the reach of the robotic manipulator. |           |
| COVERS    | Mission analysis RD2                                                                                                                                                                                                              |           |
| COMMENT   | one spot for anchorage on the client spacecraft and a second one for placing a new<br>module.                                                                                                                                     |           |

{24}------------------------------------------------

![](_page_24_Picture_0.jpeg)

| DesR_S405 | Compatibility between modules                                                                                                     | Mandatory |
|-----------|-----------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | The assembly of modules on a modular spacecraft respond to a planning and design<br>that has previously being verified on ground. |           |
| COVERS    | Mission analysis RD2                                                                                                              |           |
| COMMENT   |                                                                                                                                   |           |

## <span id="page-24-0"></span>**2.2.6 S500: Physical and resource requirements [PhyR]**

| PhyR_S501 | Components weight                                                                                                                                                        | Mandatory |
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | The weight of all components associated with the concept of modular spacecraft shall<br>be minimized (interconnectors, functional module structure, robotic manipulator) |           |
| COVERS    | Mission analysis RD2                                                                                                                                                     |           |
| COMMENT   | The concept of modular spacecraft brings additional components that creates a penalty<br>on the system weight.                                                           |           |

| PhyR_S502 | Interconnectors size and volume                                                                                    | Mandatory |
|-----------|--------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | The size and volume of the interconnectors shall be minimized to offer more place<br>inside the functional modules |           |
| COVERS    | Mission analysis RD2                                                                                               |           |
| COMMENT   |                                                                                                                    |           |

#### <span id="page-24-1"></span>**2.2.7 S600: Environmental and Operational requirements [OpR]**

| OpR_S601  | Servicer satellite                                                                                                                 | Mandatory |
|-----------|------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | The functional modules shall be delivered to the modular spacecraft by a servicer<br>satellite equipped with a robotic manipulator |           |
| COVERS    | Mission analysis RD2<br>Operational Concept RD3                                                                                    |           |
| COMMENT   |                                                                                                                                    |           |

{25}------------------------------------------------

![](_page_25_Picture_0.jpeg)

| OpR_S602  | On-Orbit Rendez-vous, interfaces                                                                                    | Mandatory |
|-----------|---------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | The modular spacecraft shall implement a physical interface for docking and/or berthing<br>of a servicer satellite. |           |
| COVERS    | Mission analysis RD2                                                                                                |           |
| COMMENT   |                                                                                                                     |           |

| OpR_S603  | On-Orbit Rendez-vous, coupled spacecraft                                                                                  | Mandatory |
|-----------|---------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | The modular spacecraft shall be able to remain coupled to the servicer spacecraft<br>without time limitation.             |           |
| COVERS    | Mission analysis RD2                                                                                                      |           |
| COMMENT   | There should be no limitation coming from any of the subsystems of the modular<br>spacecraft (ADCS, power, thermal etc.). |           |

| OpR_S604  | On-Orbit Rendez-vous, communication to servicer                                                                                            | Mandatory |
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | The modular spacecraft should be able to communicate with the servicer and exchange<br>data during and after rendez-vous operation.        |           |
| COVERS    | Mission analysis RD2                                                                                                                       |           |
| COMMENT   | Not essential during rendez-vous but highly desirable for enhanced autonomy during<br>operations without (or with minimum) ground support. |           |

| OpR_S605  | On-Orbit Rendez-vous, ground communications                                                                                                                                                                                                                                                                                                    | Mandatory |
|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | The modular spacecraft shall be able to monitor operations during and after rendez<br>vous and send reports to the ground segment.                                                                                                                                                                                                             |           |
| COVERS    | Mission analysis RD2                                                                                                                                                                                                                                                                                                                           |           |
| COMMENT   | Continuous link to ground stations is not essential for rendez-vous, however, different<br>phases are usually defined with specific milestones that are controlled by ground<br>operators.<br>After rendez-vous, the communication supports transfer of the execution plan and the<br>monitoring and feedback of the operations to the ground. |           |

{26}------------------------------------------------

![](_page_26_Picture_0.jpeg)

| OpR_S606  | Space environment                                                                                                                                                          | Mandatory |
|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | The components of the modular spacecraft: subsystems, interfaces and structures shall<br>be able to withstand the space environment for the whole duration of the mission. |           |
| COVERS    | Mission analysis RD2                                                                                                                                                       |           |
| COMMENT   | Generic requirement to be verified depending on the specific application.                                                                                                  |           |

| OpR_S607  | Launch loads                                                                                                                                                                                                             | Desirable |
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | The interconnectors design shall optimize launch load capabilities, to offer the wider<br>range of possibilities regarding pre-assembled functional modules (on the initial<br>spacecraft or the servicer) before launch |           |
| COVERS    | Mission analysis RD2                                                                                                                                                                                                     |           |
| COMMENT   | Conditions are function of the launch conditions, configuration of the modules (inertia,<br>COG,…) and type of connection with the launcher                                                                              |           |

#### <span id="page-26-0"></span>**2.2.8 S700: Safety requirements [SafR]**

| SafR_S701 | Critical functionalities                                                            | Mandatory |
|-----------|-------------------------------------------------------------------------------------|-----------|
| STATEMENT | The failure of any functional module shall not yield to the loss of the spacecraft. |           |
| COVERS    | Mission analysis RD2                                                                |           |
| COMMENT   |                                                                                     |           |

| SafR_S702 | Redundancy of critical functionalities                                                                                                            | Mandatory |
|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | Any functional module providing a critical functionality (one that is needed for the safe<br>mode of the functional platform) shall be redundant. |           |
| COVERS    | Mission analysis RD2                                                                                                                              |           |
| COMMENT   |                                                                                                                                                   |           |

{27}------------------------------------------------

![](_page_27_Picture_0.jpeg)

| SafR_S703 | Propagation of failures                                                                                                                                                                                                                                | Mandatory |
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | Any module of the modular spacecraft shall be designed as to avoid failure propagation.<br>In particular, the module shall prevent itself or any of its components from degrading<br>performances of other modules or damaging the modular spacecraft. |           |
| COVERS    | Mission analysis RD2                                                                                                                                                                                                                                   |           |
| COMMENT   |                                                                                                                                                                                                                                                        |           |

| SafR_S704 | Substitution of critical modules                                                                                                                                                                                                                                                                                                                                                                                                             | Mandatory |
|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | Any module that is considered critical (without this module the spacecraft loss one of its<br>basic functionalities) can only be exchanged if:<br>1. Another module covering its functionality has already been added to the client<br>spacecraft.<br>2. This second module is already operational.<br>3. The module to be substituted has already been isolated and switched off.<br>4. No anomaly has been detected between steps 2 and 3. |           |
| COVERS    | Mission analysis RD2                                                                                                                                                                                                                                                                                                                                                                                                                         |           |
| COMMENT   | The design principle of "do not harm" should be applied for the modules of a modular<br>spacecraft.                                                                                                                                                                                                                                                                                                                                          |           |

| SafR_S705 | Robustness to power loss                                                                                                                                                                                        | Mandatory |  |
|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|--|
| STATEMENT | Any module shall be able to withstand a sudden power loss without any damage to itself<br>or to other modules. The module shall autonomously shut down or enter a standby<br>mode of minimum power consumption. |           |  |
| COVERS    | Mission analysis RD2                                                                                                                                                                                            |           |  |
| COMMENT   | The design principle of "do not harm" should be applied for the modules of a modular<br>spacecraft.<br>In case of major anomaly of FM1, FM2 may suddenly lose its power supply.                                 |           |  |

{28}------------------------------------------------

![](_page_28_Picture_0.jpeg)

| SafR_S706 | Restart after power loss                                                                                                                                                                                               | Mandatory |  |
|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|--|
| STATEMENT | After a sudden power loss, any module of the modular spacecraft shall be able to restart<br>and resume normal operation when power supply is restored.                                                                 |           |  |
| COVERS    | Mission analysis RD2                                                                                                                                                                                                   |           |  |
| COMMENT   | The design principle of "do not harm" should be applied for the modules of a modular<br>spacecraft.<br>When functionality of FM1 is restored, the modules downstream (FM2) can restart and<br>resume normal operation. |           |  |

| SafR_S707 | Data handling system (redundancy)                                                                                                                                                                                                                                                                                                                          | Mandatory |
|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | The modular spacecraft shall implement a redundant on-board computer. The two (or<br>more) OBCs could be integrated in different modules or in the same module. If the<br>OBCs are integrated in the same module, two different interfaces should be provided,<br>ensuring that in any case a single failure does not yield to the loss of the spacecraft. |           |
| COVERS    | Mission analysis RD2                                                                                                                                                                                                                                                                                                                                       |           |
| COMMENT   |                                                                                                                                                                                                                                                                                                                                                            |           |

| SafR_S708 | Modular Satellite Failure Detection, Isolation and Recovery                                                                                         | Mandatory |
|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | The modular satellite shall be able to detect failure of any module, isolate the faulty<br>equipment and perform recovery operations when possible. |           |
| COVERS    | Mission analysis RD2                                                                                                                                |           |
| COMMENT   |                                                                                                                                                     |           |

| SafR_S709 | Safe mode                                                                                                                                                                                                      | Mandatory |
|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | The modular spacecraft shall implement a safe mode that guarantees a stable condition<br>of the spacecraft without time limitation. This mode should be fully autonomous (without<br>any ground intervention). |           |
| COVERS    | Mission analysis RD2                                                                                                                                                                                           |           |
| COMMENT   |                                                                                                                                                                                                                |           |

{29}------------------------------------------------

![](_page_29_Picture_0.jpeg)

| SafR_S710 | Safe mode (modules)                                                                                                                                                                             | Mandatory |
|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | Any module of the modular spacecraft shall implement a safe mode. This mode<br>minimizes hardware and software functions as to make minimal use of the modular<br>spacecraft resources (power). |           |
| COVERS    | Mission analysis RD2                                                                                                                                                                            |           |
| COMMENT   |                                                                                                                                                                                                 |           |

| SafR_S711 | Safe mode (command)                                                                                                                            | Mandatory |
|-----------|------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | The modular spacecraft should enter safe mode either by autonomous transition<br>triggered by the on-board computer or through ground command. |           |
| COVERS    | Mission analysis RD2                                                                                                                           |           |
| COMMENT   |                                                                                                                                                |           |

| SafR_S712 | Safe mode (modules, command)                                                                                                                                                                                | Mandatory |
|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | Any module of the modular spacecraft should enter in safe mode when commanded by<br>the on-board computer of the modular spacecraft, by ground command or by<br>autonomous triggering of the module itself. |           |
| COVERS    | Mission analysis RD2                                                                                                                                                                                        |           |
| COMMENT   |                                                                                                                                                                                                             |           |

| SafR_S713 | Data relay for critical modules                                                                                                                                                                                                                                  | Mandatory |
|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | Any module considered as critical (needed for the safe mode of the modular platform,<br>ensuring no loss of the spacecraft) shall have either:<br>a) A direct connection to the OBC.<br>b) Two independent paths to reach the OBC through other modules.         |           |
| COVERS    | Mission analysis RD2<br>Guidelines AD1-OG9-R07                                                                                                                                                                                                                   |           |
| COMMENT   | FM1 and FM5 are critical modules. FM1 is directly connected to the OBC. FM5 is not<br>directly connected to the OBC, but has two alternative ways of communicating with the<br>OBC. The design is robust to a single failure of any of the non-critical modules. |           |

{30}------------------------------------------------

![](_page_30_Picture_0.jpeg)

![](_page_30_Figure_4.jpeg)

| SafR_S714 | Power relay for critical modules                                                                                                                                                                                                                                           | Mandatory |
|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | Any module considered as critical (needed for the safe mode of the modular platform,<br>ensuring no loss of the spacecraft) shall have either:<br>a) A direct connection to the power supply.<br>b) Two independent paths to reach the power supply through other modules. |           |
| COVERS    | Mission analysis RD2                                                                                                                                                                                                                                                       |           |
| COMMENT   |                                                                                                                                                                                                                                                                            |           |

| SafR_S715 | Single points of failure                                                                                                                                                                                                                                                                                               | Mandatory |
|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT | The design of the modular spacecraft shall minimize the number of single point of<br>failures (failure that yields to loss of the spacecraft or its mission). Every single point of<br>failure should be fully described, analyzed, and justified why any other implementation is<br>not better than the selected one. |           |
| COVERS    | Mission analysis RD2                                                                                                                                                                                                                                                                                                   |           |
| COMMENT   |                                                                                                                                                                                                                                                                                                                        |           |

# <span id="page-30-0"></span>**2.2.9 S800: Configuration and implementation requirements [ConfR]**

| ConfR_S801 | Configuration of the modular spacecraft                                                                                                                                                                          | Mandatory |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT  | A modular spacecraft implements identical modules in terms of structure shape and<br>materials. Singularly, different shapes could be accepted provided that compatibility with<br>the basic modules is ensured. |           |
| COVERS     | Mission analysis RD2                                                                                                                                                                                             |           |
| COMMENT    | The basic module is the rectangle. Singularly, other modules that are compatible could                                                                                                                           |           |

{31}------------------------------------------------

![](_page_31_Picture_0.jpeg)

| be added to the modular spacecraft. |
|-------------------------------------|
|                                     |
|                                     |

| ConfR_S802 | Functional module orientation                                                                                               | Mandatory |  |
|------------|-----------------------------------------------------------------------------------------------------------------------------|-----------|--|
| STATEMENT  | The functional module orientation shall be adjustable as function of its function and<br>position on the modular spacecraft |           |  |
| COVERS     | Mission analysis RD2                                                                                                        |           |  |
| COMMENT    | The function of the module could require a specific orientation (e.g. camera orientation,<br>radiator)                      |           |  |

{32}------------------------------------------------

![](_page_32_Picture_0.jpeg)

# <span id="page-32-0"></span>**3 MOSAR Demonstrator Requirements**

# <span id="page-32-1"></span>**3.1 Demonstrator Overview**

The purpose of the MOSAR demonstrator is to illustrate scenarios of modular spacecraft assembly and re-configuration operations. The baseline scenario is the one of a Servicer Spacecraft (SVC) transporting a cargo of Spacecraft Modules (SM) and a dedicated Walking Manipulator (WM), performing a number of operations with the transfer of SM from and to the Client Spacecraft (CLT) by the manipulator.

![](_page_32_Figure_7.jpeg)

**Figure 3-1: MOSAR Demonstrator Concept**

<span id="page-32-2"></span>Spacecraft Modules are individual structures associated with a specific function of the spacecraft, that once assembled, will ensure the spacecraft operations. They can cover system (ASM, Active System Modules) or payload (APM, Active Payload Modules) functions. The SM are equipped with Standard Interfaces (SI) enabling Modules to Modules and Modules to spacecraft connections. Each SI provides mechanical, data, power and thermal transfer capabilities, allowing a full configuration of the CLT functions. That includes mechanical structural integrity, data transmission, power routing and thermal management along the elements.

The main purpose of the manipulator is to transfer the SM between the servicer and the client satellite. In order to answer the problem of reachability, the MOSAR concept is based on the implementation of a walking manipulator that ensures a high mobility along the structure. Equipped with Standard Interfaces at its both end-effectors, it can attach and manipulate the SM, but also move along the structure by connection to either the SM or the spacecraft SI. The connection is also used to power the arm and transfer the control commands coming from the spacecraft computer.

The autonomous transfer and configuration of the SM follow an execution plan prepared and validated off-line, in the Monitoring and Control Centre (MCC), on the ground segment. The MCC includes a satellite design, modelling and validation tool, specifically targeting modular satellites applications. It also allows the automatic planning of the assembly or reconfiguration sequence that can be verified with a multi-physics simulator. All these elements are working iteratively together to prepare a valid execution plan that is finally uploaded to the spacecraft for execution. Based on the monitoring and feedback information received from the spacecraft during the operations (e.g. detected failed module), the MCC

{33}------------------------------------------------

![](_page_33_Picture_0.jpeg)

can update the execution plan. The MCC finally includes visualisation front-end to support the design, verification and monitoring activities during sequence execution.

# <span id="page-33-0"></span>**3.2 Formalism**

The following section details the system requirements following the structure exemplified in this table:

<span id="page-33-1"></span>

| YY_uniqueID  | Title                                                                    |        |                | LEVEL |
|--------------|--------------------------------------------------------------------------|--------|----------------|-------|
| STATEMENT    | Requirement Statement                                                    |        |                |       |
| VERIFICATION | Review of Design (ROD) /<br>Analysis / Inspection / Testing              | COVERS | PSA_FuncR_A000 |       |
| RESPONSIBLE  | SPACEAPPS, DLR, GMV, TAS-F, TAS-UK, SITAEL, MAGSOAR, USTRAT,<br>ELLIDISS |        |                |       |
| COMMENT      | Additional comment and explanations                                      |        |                |       |

# **Table 2: Example of requirement**

The top row of the table includes:

- Unique ID: identificator with the structure YY\_uniqueID
  - YY: type of the requirement Functional requirements (FuncR), Performance requirements (PerfR), Interface requirements (IntR), …
  - uniqueID: unique reference with 4 characters:
    - The first character is a letter identifying the subsystem the requirement belongs to
    - The next number identifies the type of requirement inside the subsystem
    - The next two numbers identify a number assigned to each requirement in that category
- Title: highlighting the topic of the requirement
- LEVEL: indicates the level of importance of the requirement (mandatory / desirable / optional)

The rest of the table includes the following fields:

- STATEMENT: clear and concise description of the requirement
- VERIFICATION METHOD: indicates how the requirement is going to be verified (simulation, internal testing, lunar analog testing) with a short description of the validation process (1 to 3 lines)
- COVERS: gives indication about the origin/scope of the requirements (specific user requirement or user case, partner expertise, project constraint, etc.)
- RESPONSIBLE: indicates which partner is responsible for the verification and follow up of the requirement
- COMMENT: provides rationale or additional comments about the requirement

{34}------------------------------------------------

![](_page_34_Picture_0.jpeg)

# <span id="page-34-0"></span>**3.3 System Requirements [Axxx]**

This section and following ones list the requirements for the physical demonstrator system and subsystems developed in MOSAR.

# <span id="page-34-1"></span>**3.3.1 A100: Functional requirements [FuncR]**

| FuncR_A101   | Demonstrator purpose                                                                                                                        |        |                        | Mandatory |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------|--------|------------------------|-----------|
| STATEMENT    | The MOSAR demonstrator shall illustrate the repair and update of modular spacecraft<br>by manipulation and repositioning of SM with the WM. |        |                        |           |
| VERIFICATION | Testing                                                                                                                                     | COVERS | FuncR_S101, FuncR_S102 |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                                   |        |                        |           |
| COMMENT      |                                                                                                                                             |        |                        |           |

| FuncR_A102   | Demonstrator components                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |        |                                           | Mandatory |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-------------------------------------------|-----------|
| STATEMENT    | The MOSAR demonstrator shall include:<br><br>A set of spacecraft modules (ASM/APM) to illustrate the scenarios and<br>functionalities of modular spacecraft<br><br>A robotic walking manipulator for the manipulation of the SM<br><br>A servicer satellite and client modular spacecraft mockup to support the<br>demonstration scenarios<br><br>A monitoring and control center that includes a design and simulation tool to<br>create and simulate the execution plan and a monitoring interface |        |                                           |           |
| VERIFICATION | Review of Design                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | COVERS | Guidelines AD1<br>Operational Concept RD3 |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |        |                                           |           |
| COMMENT      |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |        |                                           |           |

| FuncR_A103   | Plan execution                                                                                                          |        |                                         | Mandatory |
|--------------|-------------------------------------------------------------------------------------------------------------------------|--------|-----------------------------------------|-----------|
| STATEMENT    | The SVC OBC shall execute autonomously the assembly/ reconfiguration plan prepared<br>by the design and simulation tool |        |                                         |           |
| VERIFICATION | Testing                                                                                                                 | COVERS | FuncR_S107<br>MOSAR Operational Concept |           |
| RESPONSIBLE  | GMV                                                                                                                     |        |                                         |           |
| COMMENT      | None                                                                                                                    |        |                                         |           |

{35}------------------------------------------------

![](_page_35_Picture_0.jpeg)

| FuncR_A104   | SVC high level control                                                                                                           |        |                                         | Mandatory |
|--------------|----------------------------------------------------------------------------------------------------------------------------------|--------|-----------------------------------------|-----------|
| STATEMENT    | The SVC OBC shall perform the high-level control of the WM, SM and SI for the<br>execution of the assembly/ reconfiguration plan |        |                                         |           |
| VERIFICATION | Review of Design / Testing                                                                                                       | COVERS | FuncR_S107<br>MOSAR Operational Concept |           |
| RESPONSIBLE  | GMV / DLR                                                                                                                        |        |                                         |           |
| COMMENT      | None                                                                                                                             |        |                                         |           |

| FuncR_A105   | Components low level control                                                                                                                                            |        |                                         | Mandatory |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-----------------------------------------|-----------|
| STATEMENT    | Low level control of the WM, SM and SI shall be performed locally by each component                                                                                     |        |                                         |           |
| VERIFICATION | Review of Design / Testing                                                                                                                                              | COVERS | FuncR_S108<br>MOSAR Operational Concept |           |
| RESPONSIBLE  | SPACEAPSS, DLR, SITAEL, TAS-UK                                                                                                                                          |        |                                         |           |
| COMMENT      | This allow to relax constraints on the data bus requirements (e.g. high rate robotic<br>control), the SVC OBC having to send only high level commands to the components |        |                                         |           |

| FuncR_A106   | WM modules operations                                             |        |                                       | Mandatory |
|--------------|-------------------------------------------------------------------|--------|---------------------------------------|-----------|
| STATEMENT    | The WM shall be able to add and replace SM (ASM/APM) by using SI. |        |                                       |           |
| VERIFICATION | Testing                                                           | COVERS | FuncR_S103<br>Operational Concept RD3 |           |
| RESPONSIBLE  | SPACEAPPS / DLR                                                   |        |                                       |           |
| COMMENT      | None                                                              |        |                                       |           |

| FuncR_A107   | WM relocation                                                                                          |        |                                       | Mandatory |
|--------------|--------------------------------------------------------------------------------------------------------|--------|---------------------------------------|-----------|
| STATEMENT    | The WM shall be able to reposition itself by using the SI of the functional modules or the<br>platform |        |                                       |           |
| VERIFICATION | Testing                                                                                                | COVERS | FuncR_S104<br>Operational Concept RD3 |           |
| RESPONSIBLE  | SPACEAPPS / DLR                                                                                        |        |                                       |           |
| COMMENT      | None                                                                                                   |        |                                       |           |

{36}------------------------------------------------

![](_page_36_Picture_0.jpeg)

| FuncR_A108   | Monitoring                                                               |        |            | Mandatory |
|--------------|--------------------------------------------------------------------------|--------|------------|-----------|
| STATEMENT    | The SVC OBC shall be able to monitor the parameters of the SM, WM and SI |        |            |           |
| VERIFICATION | Testing                                                                  | COVERS | FuncR_S109 |           |
| RESPONSIBLE  | GMV, SITAEL                                                              |        |            |           |
| COMMENT      | None                                                                     |        |            |           |

| FuncR_A109   | Spacecraft reconfiguration                                                                                            |        |            | Mandatory |
|--------------|-----------------------------------------------------------------------------------------------------------------------|--------|------------|-----------|
| STATEMENT    | The system shall be able to re-configure the CLT (e.g. SM exchange) in case of a defect<br>(e.g. malfunction of a SM) |        |            |           |
| VERIFICATION | Testing                                                                                                               | COVERS | FuncR_S101 |           |
| RESPONSIBLE  | GMV, DLR, SPACEAPPS                                                                                                   |        |            |           |
| COMMENT      |                                                                                                                       |        |            |           |

| FuncR_A110   | System redundancy                                                                                                                                                  |        |                                                                | Mandatory |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|----------------------------------------------------------------|-----------|
| STATEMENT    | The system shall be able to re-route and reallocate resources (e.g. power, data,<br>computational power, etc.) in case of a defect (e.g. interconnector of an APM) |        |                                                                |           |
| VERIFICATION | Testing                                                                                                                                                            | COVERS | FuncR_S110, FuncR_S120,<br>FuncR_S122, SafR_S813,<br>SafR_S814 |           |
| RESPONSIBLE  | GMV, DLR, SPACEAPPS                                                                                                                                                |        |                                                                |           |
| COMMENT      | This should support connection failure or a power interruption of defect modules /<br>interconnectors. Computational power can only be done in the simulator.      |        |                                                                |           |

| FuncR_A111   | Modules Plug & Play detection                                                                        |        |            | Mandatory |
|--------------|------------------------------------------------------------------------------------------------------|--------|------------|-----------|
| STATEMENT    | The SVC OBC shall be able to detect and use additional functional modules (plug &<br>play principle) |        |            |           |
| VERIFICATION | Testing                                                                                              | COVERS | FuncR_S102 |           |
| RESPONSIBLE  | GMV, ELLI, UBREST, TAS-UK                                                                            |        |            |           |
| COMMENT      |                                                                                                      |        |            |           |

{37}------------------------------------------------

![](_page_37_Picture_0.jpeg)

| FuncR_A112   | Fault detection                                                                                             |        |           | Mandatory |
|--------------|-------------------------------------------------------------------------------------------------------------|--------|-----------|-----------|
| STATEMENT    | The SVC OBC shall be able to react to a faulty behavior detected by the SM, WM or SI                        |        |           |           |
| VERIFICATION | Testing                                                                                                     | COVERS | SafR_S808 |           |
| RESPONSIBLE  | GMV                                                                                                         |        |           |           |
| COMMENT      | The reaction could include local management on the spacecraft (e.g. SM isolation) or<br>feedback to the MCC |        |           |           |

| FuncR_A113   | 3D reconstruction through WM                                                                                                                                                                                                                                            |        |               | Optional |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|---------------|----------|
| STATEMENT    | A 3D reconstruction of the satellite could be produced from the observation by a camera<br>mounted on the WM, with a maximum surface average error of 1cm                                                                                                               |        |               |          |
| VERIFICATION | Testing                                                                                                                                                                                                                                                                 | COVERS | Re-use of OG3 |          |
| RESPONSIBLE  | USTRATH                                                                                                                                                                                                                                                                 |        |               |          |
| COMMENT      | Supported after re-configuration process. The WM is used to obtain different view points<br>The 3D reconstruction should allow a human operator to assess the correctness of the<br>re-configuration, and 1cm maximum surface error should be enough to meet the target |        |               |          |

| FuncR_A114   | 3D reconstruction through SM                                                                                                                                                                                                                            |        |               | Optional |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|---------------|----------|
| STATEMENT    | A 3D reconstruction of the satellite could be produced from the observation by a camera<br>mounted in a SM, with a maximum surface average error of 1cm                                                                                                 |        |               |          |
| VERIFICATION | Testing                                                                                                                                                                                                                                                 | COVERS | Re-use of OG3 |          |
| RESPONSIBLE  | USTRATH                                                                                                                                                                                                                                                 |        |               |          |
| COMMENT      | Supported during re-configuration process, in real time (30 frames/sec)<br>The 3D reconstruction should allow a human operator to assess the correctness of the<br>re-configuration, and 1cm maximum surface error should be enough to meet the target. |        |               |          |

| FuncR_A115   | Camera Localization                                                                                                                                                                                          |        |               | Optional |  |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|---------------|----------|--|
| STATEMENT    | The 3D pose estimation of the camera mounted on the WM could be computed based<br>on the image stream, with a mean error not larger than 1 cm translation and 5° rotation,<br>with a minimum of 30 frame/sec |        |               |          |  |
| VERIFICATION | Testing                                                                                                                                                                                                      | COVERS | Re-use of OG3 |          |  |
| RESPONSIBLE  | USTRATH                                                                                                                                                                                                      |        |               |          |  |
| COMMENT      | The accuracy of the estimated pose should allow correct positioning and connection of<br>the hardware interfaces. It should also allow 3D reconstruction with errors defined in                              |        |               |          |  |

{38}------------------------------------------------

![](_page_38_Picture_0.jpeg)

FuncR\_A113 and FuncR\_A114. 1cm translation and 5° rotation errors is a reasonable previously achieved target that are compatible with the initiation of the connection process of the interconnectors through the use of the form-fit guidance. Furthermore, localization has to happen in real time, and 30 milliseconds / frame is an acceptable value achieved by recent 3d localization and mapping algorithms as described in RD2.

| FuncR_A116   | SM Localization                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |        |               | Optional |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|---------------|----------|
| STATEMENT    | The 3D pose estimation of the SM could be computed based on the image stream<br>obtained by the camera mounted on the WM, with a mean error not larger than 1 cm<br>translation and 5° rotation, with a minimum of 30 frame/sec (first estimation of a new<br>module 10 sec after appearance)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |        |               |          |
| VERIFICATION | Testing                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | COVERS | Re-use of OG3 |          |
| RESPONSIBLE  | USTRATH                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |        |               |          |
| COMMENT      | The accuracy of the estimated pose should allow correct positioning and connection of<br>the hardware interfaces. It should also allow 3D reconstruction with errors defined in<br>FuncR_A113 and FuncR_A114. 1cm translation and 5° rotation errors is a reasonable<br>previously achieved target that are compatible with the initiation of the connection<br>process of the interconnectors through the use of the form-fit guidance. Furthermore,<br>localization has to happen in real time, and 30 milliseconds / frame is an acceptable<br>value achieved by recent 3d localization and mapping algorithms as described in RD2.<br>Initial detection of a module does not require real-time capabilities, but needs to be<br>achieved in useful operating time, 10 seconds is an acceptable operation delay. |        |               |          |

#### <span id="page-38-0"></span>**3.3.2 A200: Performance requirements [PerfR]**

| PerfR_A201   | Sub-systems TM/TC data rate                                                                                                              |        |                     | Mandatory |
|--------------|------------------------------------------------------------------------------------------------------------------------------------------|--------|---------------------|-----------|
| STATEMENT    | TM/TC control of the WM and SM, including their SI, by the SVC OBC shall require a<br>network supporting a data rate of 1Mbps or greater |        |                     |           |
| VERIFICATION | Review of Design                                                                                                                         | COVERS | Operational Concept |           |
| RESPONSIBLE  | TAS-UK, SPACEAPPS, DLR                                                                                                                   |        |                     |           |
| COMMENT      | The TM/TC control of the platform should not rely on high data rate links with low<br>latency.                                           |        |                     |           |

| PerfR_A202   | Sub-systems services data rate                                                                      |        |                     | Mandatory |
|--------------|-----------------------------------------------------------------------------------------------------|--------|---------------------|-----------|
| STATEMENT    | SVC OBC shall require a network supporting a data rate of 50Mbps or greater for SM<br>service data. |        |                     |           |
| VERIFICATION | Review of Design                                                                                    | COVERS | Operational Concept |           |
| RESPONSIBLE  | TAS-UK, SPACEAPPS, SITAEL                                                                           |        |                     |           |

{39}------------------------------------------------

![](_page_39_Picture_0.jpeg)

**COMMENT** For a camera APM, at 50 Mbps, a 4Mpixel image will take several seconds to transfer across the data network.

{40}------------------------------------------------

![](_page_40_Picture_0.jpeg)

#### <span id="page-40-0"></span>**3.3.3 A300: Interface requirements [IntR]**

| IntR_A301    | SVC to CLT mechanical interface                                                                                                                                                    |        |                                 | Mandatory |
|--------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|---------------------------------|-----------|
| STATEMENT    | The SVC shall provide a mechanical docking connection to the CLT                                                                                                                   |        |                                 |           |
| VERIFICATION | Review of Design                                                                                                                                                                   | COVERS | OpR_S603<br>Operational Concept |           |
| RESPONSIBLE  | SITAEL, TAS-UK                                                                                                                                                                     |        |                                 |           |
| COMMENT      | The docking procedure is not part of the In MOSAR demonstration scenarios. Both<br>spacecraft will be rigidly connected all along the demonstrations with a representative<br>gap. |        |                                 |           |

| IntR_A302    | SVC to CLT data interface                                                                                                     |        |                                 | Mandatory |
|--------------|-------------------------------------------------------------------------------------------------------------------------------|--------|---------------------------------|-----------|
| STATEMENT    | The SVC shall provide a data interface to the CLT to connect both internal networks                                           |        |                                 |           |
| VERIFICATION | Review of Design                                                                                                              | COVERS | OpR_S604<br>Operational Concept |           |
| RESPONSIBLE  | SITAEL, TAS-UK                                                                                                                |        |                                 |           |
| COMMENT      | The data interface allows the SVC to take the control of all the components for the<br>execution of the re-configuration plan |        |                                 |           |

| IntR_A303    | SVC to CLT power interface                                                               |        |                     | Optional |  |
|--------------|------------------------------------------------------------------------------------------|--------|---------------------|----------|--|
| STATEMENT    | The SVC shall provide a power interface to the CLT to be able to power CLT<br>components |        |                     |          |  |
| VERIFICATION | Review of Design                                                                         | COVERS | Operational Concept |          |  |
| RESPONSIBLE  | SITAEL, TAS-UK                                                                           |        |                     |          |  |
| COMMENT      | Not required as, in the demonstration, the CLT could have his own power sub-system       |        |                     |          |  |

| IntR_A304    | MCC to SVC data link                                                                                  |        |                                 | Mandatory |
|--------------|-------------------------------------------------------------------------------------------------------|--------|---------------------------------|-----------|
| STATEMENT    | The MCC shall provide a data link for upload of the execution plan and TM/TC services<br>with the SVC |        |                                 |           |
| VERIFICATION | Review of Design                                                                                      | COVERS | OpR_S605<br>Operational Concept |           |
| RESPONSIBLE  | GMV, DLR                                                                                              |        |                                 |           |
| COMMENT      | Represent the satellite link communication, could implement space standard                            |        |                                 |           |

{41}------------------------------------------------

![](_page_41_Picture_0.jpeg)

communication protocols, e.g. the packet utilization standard (PUS) to give some level of representativeness to the demonstrator.

| IntR_A305    | MCC to SVC debugging link                                                                                                        |        |                   | Mandatory |
|--------------|----------------------------------------------------------------------------------------------------------------------------------|--------|-------------------|-----------|
| STATEMENT    | The MCC shall provide a data link for monitoring and debugging purpose during the<br>integration and testing of the demonstrator |        |                   |           |
| VERIFICATION | Review of Design                                                                                                                 | COVERS | Partner expertise |           |
| RESPONSIBLE  | GMV                                                                                                                              |        |                   |           |
| COMMENT      |                                                                                                                                  |        |                   |           |

| IntR_A306    | SVC and CTL SI                                                               |        |                        | Mandatory |
|--------------|------------------------------------------------------------------------------|--------|------------------------|-----------|
| STATEMENT    | The SVC and CTL shall provide SI to enable connection with the SM and the WM |        |                        |           |
| VERIFICATION | Review of Design                                                             | COVERS | FuncR_S110, FuncR_S118 |           |
| RESPONSIBLE  | SITAEL, SPACEAPPS                                                            |        |                        |           |
| COMMENT      |                                                                              |        |                        |           |

# <span id="page-41-0"></span>**3.3.4 A400: Design requirements [DesR]**

| DesR_A401    | OG1 Reuse                                                                   |        |                        | Mandatory |
|--------------|-----------------------------------------------------------------------------|--------|------------------------|-----------|
| STATEMENT    | The platform shall implement ESROCOS from OG1 for the control of the system |        |                        |           |
| VERIFICATION | Review of Design                                                            | COVERS | Guidelines AD1 OG9-R10 |           |
| RESPONSIBLE  | GMV                                                                         |        |                        |           |
| COMMENT      | A number of adaptations and extensions are anticipate (see RD1)             |        |                        |           |

| DesR_A402    | OG2 Reuse                                                        |        |                        | Mandatory |
|--------------|------------------------------------------------------------------|--------|------------------------|-----------|
| STATEMENT    | The platform shall implement autonomy functions using OG2 (ERGO) |        |                        |           |
| VERIFICATION | Review of Design                                                 | COVERS | Guidelines AD1 OG9-R10 |           |
| RESPONSIBLE  | GMV                                                              |        |                        |           |
| COMMENT      | A number of adaptations and extensions are anticipate (see RD1)  |        |                        |           |

{42}------------------------------------------------

![](_page_42_Picture_0.jpeg)

| DesR_A403    | OG3 Reuse                                                                                                                                                                                                                                    |                                  |  | Optional |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------|--|----------|
| STATEMENT    | The platform shall implement sensor data fusion techniques from OG3 (Infuse)                                                                                                                                                                 |                                  |  |          |
| VERIFICATION | Review of Design                                                                                                                                                                                                                             | COVERS<br>Guidelines AD1 OG9-R10 |  |          |
| RESPONSIBLE  | USTRATH                                                                                                                                                                                                                                      |                                  |  |          |
| COMMENT      | The WM operations would rely only on known geometry information, without the need of<br>data fusion techniques. To be discussed and decided at SRR if data fusion techniques<br>are illustrated in the scenario (e.g. SVC visual validation) |                                  |  |          |

| DesR_A404    | OG4 Reuse                                                                                                                                                                                                 |        |                        | Mandatory |
|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------------------|-----------|
| STATEMENT    | The satellite shall be equipped with its own integrated R-ICU derived from the OG4<br>I3DS architecture and illustrate operations of functional modules equipped with selected<br>sensors suite from I3DS |        |                        |           |
| VERIFICATION | Review of Design                                                                                                                                                                                          | COVERS | Guidelines AD1 OG9-R10 |           |
| RESPONSIBLE  | TAS-UK, TAS-F                                                                                                                                                                                             |        |                        |           |
| COMMENT      | A number of adaptations and extensions are anticipate (see RD1)                                                                                                                                           |        |                        |           |

| DesR_A405    | OG5 Reuse                                                                                                          |        |                        | Mandatory |  |
|--------------|--------------------------------------------------------------------------------------------------------------------|--------|------------------------|-----------|--|
| STATEMENT    | The required H/W units in OG9 (platform, ASMs/APMs, robot) shall be equipped with<br>standard interfaces from OG5. |        |                        |           |  |
| VERIFICATION | Review of Design                                                                                                   | COVERS | Guidelines AD1 OG9-R10 |           |  |
| RESPONSIBLE  | SPACEAPPS                                                                                                          |        |                        |           |  |
| COMMENT      | A number of adaptations and extensions are anticipate (see RD1)                                                    |        |                        |           |  |

| DesR_A406    | SVC and CLT OBC                                                                                                                                      |        |            | Mandatory |
|--------------|------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------|-----------|
| STATEMENT    | The SVC and CLT spacecraft shall have on OBC for the management of the different<br>components associated with the spacecraft and the communications |        |            |           |
| VERIFICATION | Review of Design                                                                                                                                     | COVERS | FuncR_S114 |           |
| RESPONSIBLE  | SITAEL                                                                                                                                               |        |            |           |
| COMMENT      | In the MOSAR demonstration, the SVC OBC should take the lead on all the<br>components of the system.                                                 |        |            |           |

{43}------------------------------------------------

![](_page_43_Picture_0.jpeg)

| DesR_A407    | Data Network                                                                                                                                                                                         |        |                        | Mandatory |
|--------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------------------|-----------|
| STATEMENT    | The system shall implement a data technology network that supports data bus re<br>configuration and routing                                                                                          |        |                        |           |
| VERIFICATION | Review of Design / Testing                                                                                                                                                                           | COVERS | FuncR_S110, FuncR_S119 |           |
| RESPONSIBLE  | TAS-UK                                                                                                                                                                                               |        |                        |           |
| COMMENT      | In the MOSAR demonstration, the SVC OBC should take the lead on all the<br>components of the system.<br>The current selected technology is SpaceWire based on the developments and outputs<br>of OG4 |        |                        |           |

| DesR_A408    | Relevance to flight hardware                                                                                                                                                                                                                                                                                                                          |        |                            | Desirable |  |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|----------------------------|-----------|--|
| STATEMENT    | The demonstrator design should not be de-rated for demonstration use and be<br>representative of an actual space system in terms of capabilities (e.g. mass movement<br>capacity, speed of reconfiguration, processing capacity of on-board computing), while<br>still retaining feasibility of operation in Earth's gravity (so as to be functional) |        |                            |           |  |
| VERIFICATION | Review of Design                                                                                                                                                                                                                                                                                                                                      | COVERS | PERASPERA final objectives |           |  |
| RESPONSIBLE  | ALL                                                                                                                                                                                                                                                                                                                                                   |        |                            |           |  |
| COMMENT      |                                                                                                                                                                                                                                                                                                                                                       |        |                            |           |  |

# <span id="page-43-0"></span>**3.3.5 A500: Physical and resource requirements [PhyR]**

N./A.

# <span id="page-43-1"></span>**3.3.6 A600: Environmental and Operational requirements [OpR]**

| OpR_A601     | Laboratory Environment                                                                                             |        |                          | Mandatory |
|--------------|--------------------------------------------------------------------------------------------------------------------|--------|--------------------------|-----------|
| STATEMENT    | The demonstrator shall be able to work under laboratory conditions in a temperature<br>range between 10 and 30 deg |        |                          |           |
| VERIFICATION | Review of Design                                                                                                   | COVERS | Demonstration Constraint |           |
| RESPONSIBLE  | ALL                                                                                                                |        |                          |           |
| COMMENT      |                                                                                                                    |        |                          |           |

{44}------------------------------------------------

![](_page_44_Picture_0.jpeg)

| OpR_A602     | Gravity conditions                              |        |                          | Mandatory |
|--------------|-------------------------------------------------|--------|--------------------------|-----------|
| STATEMENT    | The demonstrator shall be able to work under 1g |        |                          |           |
| VERIFICATION | Review of Design                                | COVERS | Demonstration Constraint |           |
| RESPONSIBLE  | ALL                                             |        |                          |           |
| COMMENT      |                                                 |        |                          |           |

| OpR_A603     | Demonstrator Power supply                                              |        |                          | Mandatory |
|--------------|------------------------------------------------------------------------|--------|--------------------------|-----------|
| STATEMENT    | The demonstrator shall be able to be powered from standard power plugs |        |                          |           |
| VERIFICATION | Review of Design                                                       | COVERS | Demonstration Constraint |           |
| RESPONSIBLE  | ALL                                                                    |        |                          |           |
| COMMENT      |                                                                        |        |                          |           |

# <span id="page-44-0"></span>**3.3.7 A700: Safety requirements [SafR]**

| SafR_A701    | Demonstrator Safety                                                                                                                                                                                                                              |        |              | Mandatory |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|--------------|-----------|
| STATEMENT    | Demonstrator shall be inherently safe during operation, considering the implementation<br>in a laboratory environment with trained operators                                                                                                     |        |              |           |
| VERIFICATION | Review of Design                                                                                                                                                                                                                                 | COVERS | Safety rules |           |
| RESPONSIBLE  | ALL                                                                                                                                                                                                                                              |        |              |           |
| COMMENT      | Safety should consider mechanical and electrical potential issue. Safety can be<br>addressed by system design (limited speeds, compliance) and/or through<br>implementation of safety features (Emergency stops, interlocks or sensors barriers) |        |              |           |

## <span id="page-44-1"></span>**3.3.8 A800: Configuration and implementation requirements [ConfR]**

| ConfR_A801   | SVC and TGT test bench                                                                                                                                                                    |        |                                     | Mandatory |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-------------------------------------|-----------|
| STATEMENT    | A test bench shall be designed and integrated to represent the SVC satellite to the CLT<br>spacecraft, considering the gap existing between both the platform during docking<br>condition |        |                                     |           |
| VERIFICATION | Review of Design, Inspection                                                                                                                                                              | COVERS | OpR_S603<br>Operational Concept RD3 |           |
| RESPONSIBLE  | SITAEL                                                                                                                                                                                    |        |                                     |           |
| COMMENT      |                                                                                                                                                                                           |        |                                     |           |

{45}------------------------------------------------

![](_page_45_Picture_0.jpeg)

| ConfR_A801   | Test bench mechanical structure                                                                                              |        |                                | Mandatory |
|--------------|------------------------------------------------------------------------------------------------------------------------------|--------|--------------------------------|-----------|
| STATEMENT    | The structure of the test bench shall be stable and able to carry the own mass and the<br>loads introduced by the SMs and WM |        |                                |           |
| VERIFICATION | Review of Design, Analysis                                                                                                   | COVERS | Preliminary MOSAR demonstrator |           |
| RESPONSIBLE  | SITAEL                                                                                                                       |        |                                |           |
| COMMENT      |                                                                                                                              |        |                                |           |

| ConfR_A802   | Test bench SI interfaces                                                                                                |        |                                                           | Mandatory |
|--------------|-------------------------------------------------------------------------------------------------------------------------|--------|-----------------------------------------------------------|-----------|
| STATEMENT    | The SVC and CTL test benches shall provide the required number of SI to cover the<br>MOSAR scenario demonstrations      |        |                                                           |           |
| VERIFICATION | Review of Design                                                                                                        | COVERS | IntR_A306                                                 |           |
| RESPONSIBLE  | SITAEL, SPACEAPPS                                                                                                       |        |                                                           |           |
| COMMENT      |                                                                                                                         |        |                                                           |           |
| ConfR_A803   | Test bench harnessing                                                                                                   |        |                                                           | Mandatory |
| STATEMENT    | The test bench shall include the internal and external harnessing of the SVC and CTL<br>spacecraft and the connected SI |        |                                                           |           |
| VERIFICATION | Review of Design, Inspection                                                                                            | COVERS | Operational Concept RD3<br>Preliminary MOSAR demonstrator |           |
| RESPONSIBLE  | SITAEL, SPACEAPPS, TAS-UK                                                                                               |        |                                                           |           |
| COMMENT      |                                                                                                                         |        |                                                           |           |

{46}------------------------------------------------

![](_page_46_Picture_0.jpeg)

# <span id="page-46-0"></span>**3.4 Walking Manipulator Requirements [Bxxx]**

# <span id="page-46-1"></span>**3.4.1 B100: Functional requirements [FuncR]**

| FuncR_B101   | SM connection                                                                                                            |        |                        | Mandatory |
|--------------|--------------------------------------------------------------------------------------------------------------------------|--------|------------------------|-----------|
| STATEMENT    | The WM shall be able to connect to the SI of the SM or the spacecraft mockup,<br>independently through one of its own SI |        |                        |           |
| VERIFICATION | Testing                                                                                                                  | COVERS | FuncR_A106, FuncR_A107 |           |
| RESPONSIBLE  | SPACEAPPS, DLR                                                                                                           |        |                        |           |
| COMMENT      |                                                                                                                          |        |                        |           |

| FuncR_B102   | SM manipulation                                                                            |        |            | Mandatory |
|--------------|--------------------------------------------------------------------------------------------|--------|------------|-----------|
| STATEMENT    | The WM shall be able to move and assemble the functional modules in a 3-dimensional<br>way |        |            |           |
| VERIFICATION | Testing                                                                                    | COVERS | FuncR_A106 |           |
| RESPONSIBLE  | SPACEAPPS, DLR                                                                             |        |            |           |
| COMMENT      |                                                                                            |        |            |           |

| FuncR_B103   | Joint position control                                              |        |                                                | Mandatory |
|--------------|---------------------------------------------------------------------|--------|------------------------------------------------|-----------|
| STATEMENT    | The WM shall provide local joint position control at minimum 500 Hz |        |                                                |           |
| VERIFICATION | Testing                                                             | COVERS | MOSAR Operational Concept<br>Partner Expertise |           |
| RESPONSIBLE  | DLR, SPACEAPPS                                                      |        |                                                |           |
| COMMENT      |                                                                     |        |                                                |           |

| FuncR_B104   | Cartesian position control                                                                          |        |                                                | Mandatory |
|--------------|-----------------------------------------------------------------------------------------------------|--------|------------------------------------------------|-----------|
| STATEMENT    | The WM shall provide local Cartesian position control of the free end-effector at<br>minimum 500 Hz |        |                                                |           |
| VERIFICATION | Testing                                                                                             | COVERS | MOSAR Operational Concept<br>Partner Expertise |           |
| RESPONSIBLE  | DLR, SPACEAPPS                                                                                      |        |                                                |           |
| COMMENT      | To support manipulation of the SM along pre-defined trajectories and initial SI alignment           |        |                                                |           |

{47}------------------------------------------------

![](_page_47_Picture_0.jpeg)

| FuncR_B104   | Impedance control                                        |        |                                                | Mandatory |
|--------------|----------------------------------------------------------|--------|------------------------------------------------|-----------|
| STATEMENT    | The WM shall provide impedance control at minimum 500 Hz |        |                                                |           |
| VERIFICATION | Testing                                                  | COVERS | MOSAR Operational Concept<br>Partner Expertise |           |
| RESPONSIBLE  | DLR, SPACEAPPS                                           |        |                                                |           |
| COMMENT      | To support SI alignment or connection process            |        |                                                |           |

| FuncR_B105   | Fault detection                                              |        |            | Mandatory |
|--------------|--------------------------------------------------------------|--------|------------|-----------|
| STATEMENT    | The WM shall be able to detect malfunction of its operations |        |            |           |
| VERIFICATION | Testing                                                      | COVERS | FuncR_A112 |           |
| RESPONSIBLE  | SPACEAPPS                                                    |        |            |           |
| COMMENT      |                                                              |        |            |           |

| FuncR_B106   | Power-on/off                                                                                          |        |                           | Desirable |
|--------------|-------------------------------------------------------------------------------------------------------|--------|---------------------------|-----------|
| STATEMENT    | The WM shall be able to be powered on/off, keeping its current position                               |        |                           |           |
| VERIFICATION | Testing                                                                                               | COVERS | MOSAR Operational Concept |           |
| RESPONSIBLE  | SPACEAPPS                                                                                             |        |                           |           |
| COMMENT      | To reduce consumption when the WM is not in use. The power switch could be<br>managed at the SI level |        |                           |           |

| FuncR_B107   | WM start and initialization                                                                                                           |        |                           | Mandatory |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------|--------|---------------------------|-----------|
| STATEMENT    | The WM shall be able to start and initialize automatically after power-on, reaching a<br>state ready for communication and operations |        |                           |           |
| VERIFICATION | Testing                                                                                                                               | COVERS | MOSAR Operational Concept |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                             |        |                           |           |
| COMMENT      |                                                                                                                                       |        |                           |           |

{48}------------------------------------------------

![](_page_48_Picture_0.jpeg)

| FuncR_B106   | WM perception                                                                                                                                                |        |                     | Optional |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|---------------------|----------|
| STATEMENT    | The WM could have the ability to perceive the location of SMs in three dimensions to an<br>error of 1cm using attached stereo vision sensors.                |        |                     |          |
| VERIFICATION | Testing                                                                                                                                                      | COVERS | Operational Concept |          |
| RESPONSIBLE  | DLR, USTRATH                                                                                                                                                 |        |                     |          |
| COMMENT      | Not required with the current approach of WM SM approach and manipulation (based<br>on known geometry and SM localization). Would require additional sensors |        |                     |          |

# <span id="page-48-0"></span>**3.4.2 B200: Performance requirements [PerfR]**

| PerfR_B201   | WM payload capability                                                                                                                 |        |                                    | Mandatory |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------|--------|------------------------------------|-----------|
| STATEMENT    | The WM shall be able to manipulate a payload of 7kg all around his workspace                                                          |        |                                    |           |
| VERIFICATION | Testing                                                                                                                               | COVERS | Demonstration Scenario<br>OpR_A602 |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                             |        |                                    |           |
| COMMENT      | The target is to not implement external gravity compensation on the SM, TBC<br>depending on the updated weight estimations during PDR |        |                                    |           |

| PerfR_B202   | WM reachability                                                                                                                 |        |                                     | Mandatory |
|--------------|---------------------------------------------------------------------------------------------------------------------------------|--------|-------------------------------------|-----------|
| STATEMENT    | The WM kinematic structure shall be compatible in size and joint configuration to<br>support all MOSAR scenarios demonstrations |        |                                     |           |
| VERIFICATION | Testing                                                                                                                         | COVERS | Demonstration Scenario<br>DesR_S404 |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                       |        |                                     |           |
| COMMENT      | Kinematic configuration and reachability analyzed during PDR phase                                                              |        |                                     |           |

| PerfR_B203   | WM data interface rate for TM/TC                                                                 |        |                                         | Mandatory |
|--------------|--------------------------------------------------------------------------------------------------|--------|-----------------------------------------|-----------|
| STATEMENT    | The data interface of the WM shall support a data rate of 1Mbps or greater for TM/TC<br>control. |        |                                         |           |
| VERIFICATION | Testing                                                                                          | COVERS | MOSAR Operational Concept<br>PerfR_A201 |           |
| RESPONSIBLE  | SPACEAPPS, DLR, TAS-UK                                                                           |        |                                         |           |
| COMMENT      | The TM/TC control of the platform should not rely on high data rate links with low<br>latency.   |        |                                         |           |

{49}------------------------------------------------

![](_page_49_Picture_0.jpeg)

| PerfR_B204   | WM data interface rate for service data                                                                                                                                                                                                                                                   |        |                                         | Mandatory |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-----------------------------------------|-----------|
| STATEMENT    | The data interface of the WM shall support a data rate of 50 Mbps or greater for service<br>data.                                                                                                                                                                                         |        |                                         |           |
| VERIFICATION | Testing                                                                                                                                                                                                                                                                                   | COVERS | MOSAR Operational Concept<br>PerfR_A202 |           |
| RESPONSIBLE  | SPACEAPPS, DLR, TAS-UK                                                                                                                                                                                                                                                                    |        |                                         |           |
| COMMENT      | E.g. to support data transfer from a connected SM<br>The services provided by the Spacecraft Module share the same data interface as<br>TM/TC and will have a higher bandwidth requirement. At 50 Mbps, a 4Mpixel image will<br>take several seconds to transfer across the data network. |        |                                         |           |

| PerfR_B205   | WM power interface rate                                                   |  |  | Mandatory |
|--------------|---------------------------------------------------------------------------|--|--|-----------|
| STATEMENT    | The power interface of the WM shall support 0.5kW [TBC] of power transfer |  |  |           |
| VERIFICATION | Testing<br>COVERS<br>MOSAR Operational Concept<br>PerfR_A202              |  |  |           |
| RESPONSIBLE  | SPACEAPPS                                                                 |  |  |           |
| COMMENT      | For the operation of the WM and one connected SM (APM). Value TBC for PDR |  |  |           |

# <span id="page-49-0"></span>**3.4.3 B300: Interface requirements [IntR]**

| IntR_B301    | WM TM/TC                                                                                                                                                     |        |                     | Mandatory |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|---------------------|-----------|
| STATEMENT    | The WM shall transmit telemetry and receive high-level tele-command with the SVC<br>OBC, independently through the data interface of one of the connected SI |        |                     |           |
| VERIFICATION | Testing                                                                                                                                                      | COVERS | Operational Concept |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                                                    |        |                     |           |
| COMMENT      |                                                                                                                                                              |        |                     |           |

{50}------------------------------------------------

![](_page_50_Picture_0.jpeg)

| IntR_B302    | WM data transfer                                                                                    |        |                                       | Mandatory |
|--------------|-----------------------------------------------------------------------------------------------------|--------|---------------------------------------|-----------|
| STATEMENT    | The WM shall be able to transmit TM/TC and data from the SVC OBC with the SM<br>connected at its SI |        |                                       |           |
| VERIFICATION | Testing                                                                                             | COVERS | Operational Concept<br>Guidelines AD1 |           |
| RESPONSIBLE  | SPACEAPPS                                                                                           |        |                                       |           |
| COMMENT      |                                                                                                     |        |                                       |           |

| IntR_B303    | WM power                                                                                              |        |                     | Mandatory |
|--------------|-------------------------------------------------------------------------------------------------------|--------|---------------------|-----------|
| STATEMENT    | The WM shall get power from the spacecraft/modules through the power interface of the<br>connected SI |        |                     |           |
| VERIFICATION | Testing                                                                                               | COVERS | Operational Concept |           |
| RESPONSIBLE  | SPACEAPPS                                                                                             |        |                     |           |
| COMMENT      |                                                                                                       |        |                     |           |

| IntR_B304    | WM power transfer                                                    |        |                     | Mandatory |
|--------------|----------------------------------------------------------------------|--------|---------------------|-----------|
| STATEMENT    | The WM shall be able to transmit power to the SM connected at its SI |        |                     |           |
| VERIFICATION | Testing                                                              | COVERS | Operational Concept |           |
| RESPONSIBLE  | SPACEAPPS                                                            |        |                     |           |
| COMMENT      |                                                                      |        |                     |           |

| IntR_B304    | WM interface switch                                                                    |        |                     | Mandatory |
|--------------|----------------------------------------------------------------------------------------|--------|---------------------|-----------|
| STATEMENT    | The WM shall be able to switch power and data interface between the two SI extremities |        |                     |           |
| VERIFICATION | Testing                                                                                | COVERS | Operational Concept |           |
| RESPONSIBLE  | SPACEAPPS                                                                              |        |                     |           |
| COMMENT      |                                                                                        |        |                     |           |

{51}------------------------------------------------

![](_page_51_Picture_0.jpeg)

| IntR_B305    | WM local CAN network                                                                   |        |                     | Mandatory |
|--------------|----------------------------------------------------------------------------------------|--------|---------------------|-----------|
| STATEMENT    | The WM shall provide a local CAN network to interface and control the end-effectors SI |        |                     |           |
| VERIFICATION | Testing                                                                                | COVERS | Operational Concept |           |
| RESPONSIBLE  | SPACEAPPS                                                                              |        |                     |           |
| COMMENT      | CAN network technology is currently selected based on OG5 outputs                      |        |                     |           |

| IntR_B306    | WM local control network                                                                                                                                                                         |        |                     | Mandatory |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|---------------------|-----------|
| STATEMENT    | The WM shall be able to parse information from/to its data interface through the two SI<br>extremities and translate it in its own local bus for Real-Timer monitor and control of its<br>joins. |        |                     |           |
| VERIFICATION | Testing                                                                                                                                                                                          | COVERS | Operational Concept |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                                                                                        |        |                     |           |
| COMMENT      |                                                                                                                                                                                                  |        |                     |           |

| IntR_B307    | WM mechanical interface to SI                                                              |        |                     | Mandatory |
|--------------|--------------------------------------------------------------------------------------------|--------|---------------------|-----------|
| STATEMENT    | The WM shall provide a mechanical interface connection at each extremity to attach a<br>SI |        |                     |           |
| VERIFICATION | Testing                                                                                    | COVERS | Operational Concept |           |
| RESPONSIBLE  | SPACEAPPS                                                                                  |        |                     |           |
| COMMENT      |                                                                                            |        |                     |           |

#### <span id="page-51-0"></span>**3.4.4 B400: Design requirements [DesR]**

| DesR_B401    | SI as WM end-effectors                                        |        |                         | Mandatory |
|--------------|---------------------------------------------------------------|--------|-------------------------|-----------|
| STATEMENT    | The WM shall be equipped with a SI at each of its extremities |        |                         |           |
| VERIFICATION | Review of Design                                              | COVERS | Operational Concept RD3 |           |
| RESPONSIBLE  | SPACEAPPS                                                     |        |                         |           |
| COMMENT      |                                                               |        |                         |           |

{52}------------------------------------------------

![](_page_52_Picture_0.jpeg)

| DesR_B402    | Embedded controller                                                                                                                          |        |                                         | Mandatory |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------|--------|-----------------------------------------|-----------|
| STATEMENT    | The WM shall have an embedded local controller to convert high-level control<br>commands from the SVC OBC to low-level control of the joints |        |                                         |           |
| VERIFICATION | Review of Design                                                                                                                             | COVERS | FuncR_S108<br>MOSAR Operational Concept |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                                    |        |                                         |           |
| COMMENT      |                                                                                                                                              |        |                                         |           |

| DesR_B403    | Torque/force sensors                                                                                         |        |                         | Mandatory |
|--------------|--------------------------------------------------------------------------------------------------------------|--------|-------------------------|-----------|
| STATEMENT    | The WM shall be equipped with Force/Torque sensors to support the implementation of<br>the impedance control |        |                         |           |
| VERIFICATION | Review of Design                                                                                             | COVERS | Operational Concept RD3 |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                    |        |                         |           |
| COMMENT      | End-tip of joint torque TBC                                                                                  |        |                         |           |

| DesR_B404    | Compatibility to environmental tests conditions                                                      |        |                           | Mandatory |
|--------------|------------------------------------------------------------------------------------------------------|--------|---------------------------|-----------|
| STATEMENT    | The design of the WM shall be such that it is able to withstand the test environmental<br>conditions |        |                           |           |
| VERIFICATION | Review of Design                                                                                     | COVERS | Demonstration constraints |           |
| RESPONSIBLE  | SPACEAPPS                                                                                            |        |                           |           |
| COMMENT      |                                                                                                      |        |                           |           |

| DesR_B405    | Compatibility to space design                                                                                   |        |                                    | Mandatory |
|--------------|-----------------------------------------------------------------------------------------------------------------|--------|------------------------------------|-----------|
| STATEMENT    | The design of the WM shall be such that the later product is able to withstand the harsh<br>conditions in space |        |                                    |           |
| VERIFICATION | Review of Design                                                                                                | COVERS | Guidelines RD3 OG9-R09<br>OpR_S606 |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                       |        |                                    |           |
| COMMENT      |                                                                                                                 |        |                                    |           |

{53}------------------------------------------------

![](_page_53_Picture_0.jpeg)

## <span id="page-53-0"></span>**3.4.5 B500: Physical and resource requirements [PhyR]**

| PhyR_B501    | WM weight                                                                                       |        |           | Mandatory |  |
|--------------|-------------------------------------------------------------------------------------------------|--------|-----------|-----------|--|
| STATEMENT    | The weight of the WM shall minimized with a targeted weight of 14kg [TBC], including<br>the SI. |        |           |           |  |
| VERIFICATION | Testing                                                                                         | COVERS | PhyR_S501 |           |  |
| RESPONSIBLE  | SPACEAPPS                                                                                       |        |           |           |  |
| COMMENT      | Based on the assumption of a 1 to half payload capability of 7kg                                |        |           |           |  |

# <span id="page-53-1"></span>**3.4.6 B600: Environmental and Operational requirements [OpR]**

N./A.

# <span id="page-53-2"></span>**3.4.7 B700: Safety requirements [SafR]**

N./A.

# <span id="page-53-3"></span>**3.4.8 B800: Configuration and implementation requirements [ConfR]**

N./A.

{54}------------------------------------------------

![](_page_54_Picture_0.jpeg)

# <span id="page-54-0"></span>**3.5 Spacecraft Modules Requirements [Cxxx]**

## <span id="page-54-1"></span>**3.5.1 C100: Functional requirements [FuncR]**

| FuncR_C101   | SM functions                                                                                                                                  |        |                         | Mandatory |
|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------|--------|-------------------------|-----------|
| STATEMENT    | The SMs shall provide all required support functions to any embarked unit and<br>guarantee the required operative profile during the lifetime |        |                         |           |
| VERIFICATION | Review of Design, Testing                                                                                                                     | COVERS | Operational Concept RD3 |           |
| RESPONSIBLE  | SITAEL                                                                                                                                        |        |                         |           |
| COMMENT      |                                                                                                                                               |        |                         |           |

| FuncR_C102   | SM components                                                                    |        |                        | Mandatory |
|--------------|----------------------------------------------------------------------------------|--------|------------------------|-----------|
| STATEMENT    | Each SM shall be able to host all the components needed to fulfill its functions |        |                        |           |
| VERIFICATION | Review of Design                                                                 | COVERS | Guidelines AD1 OG9-R11 |           |
| RESPONSIBLE  | SITAEL                                                                           |        |                        |           |
| COMMENT      |                                                                                  |        |                        |           |

| FuncR_C103   | SM data routing configuration                                                                                                                                                                        |        |                                         | Mandatory |
|--------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-----------------------------------------|-----------|
| STATEMENT    | The baseline functionality of a Spacecraft Module shall include the ability to externally<br>configure the SM's data routing function between the Standard Interfaces and services<br>provided by SM |        |                                         |           |
| VERIFICATION | Review of Design / Testing                                                                                                                                                                           | COVERS | FuncR_S120<br>MOSAR Operational Concept |           |
| RESPONSIBLE  | TAS-UK                                                                                                                                                                                               |        |                                         |           |
| COMMENT      |                                                                                                                                                                                                      |        |                                         |           |

{55}------------------------------------------------

![](_page_55_Picture_0.jpeg)

| FuncR_C104   | SM data transmission                                                                                                                                                                                                                  |        |                                                     | Mandatory |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-----------------------------------------------------|-----------|
| STATEMENT    | The baseline functionality of a Spacecraft Module shall include the ability to provide<br>external TM/TC control and service data of the Spacecraft Module via the SM data<br>interface once the routing function has been configured |        |                                                     |           |
| VERIFICATION | Review of Design / Testing                                                                                                                                                                                                            | COVERS | FuncR_S119, FuncR_A108<br>MOSAR Operational Concept |           |
| RESPONSIBLE  | TAS-UK                                                                                                                                                                                                                                |        |                                                     |           |
| COMMENT      |                                                                                                                                                                                                                                       |        |                                                     |           |

| FuncR_C103   | SM rower routing configuration                                                                                                                                         |                                     |  | Mandatory |
|--------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------|--|-----------|
| STATEMENT    | The baseline functionality of a Spacecraft Module shall include the ability to externally<br>configure the SM's power routing function between the Standard Interfaces |                                     |  |           |
| VERIFICATION | Review of Design / Testing                                                                                                                                             | COVERS<br>MOSAR Operational Concept |  |           |
| RESPONSIBLE  | TAS-UK                                                                                                                                                                 |                                     |  |           |
| COMMENT      | This can be envisaged by an internal power distribution unit in the SM or at the SI level                                                                              |                                     |  |           |

| FuncR_C105   | SM redundancy                                                                   |        |            | Mandatory |
|--------------|---------------------------------------------------------------------------------|--------|------------|-----------|
| STATEMENT    | The assembled modules shall be able to switch to redundant data and power paths |        |            |           |
| VERIFICATION | Testing                                                                         | COVERS | FuncR_A110 |           |
| RESPONSIBLE  | TAS-UK, SPACEAPPS                                                               |        |            |           |
| COMMENT      |                                                                                 |        |            |           |

| FuncR_C106   | SM power-on/off                                                                                                                     |  |  | Desirable |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------|--|--|-----------|
| STATEMENT    | The SM shall be able to be powered on/off or put in stand-by mode, keeping its<br>capability to transmit data and power to other SM |  |  |           |
| VERIFICATION | Testing<br>COVERS<br>MOSAR Operational Concept                                                                                      |  |  |           |
| RESPONSIBLE  | SITAEL                                                                                                                              |  |  |           |
| COMMENT      | To reduce consumption when the SM is not in use.                                                                                    |  |  |           |

{56}------------------------------------------------

![](_page_56_Picture_0.jpeg)

| FuncR_C107   | SM start and initialization                                                                                                           |        |                           | Mandatory |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------|--------|---------------------------|-----------|
| STATEMENT    | The SM shall be able to start and initialize automatically after power-on, reaching a state<br>ready for communication and operations |        |                           |           |
| VERIFICATION | Testing                                                                                                                               | COVERS | MOSAR Operational Concept |           |
| RESPONSIBLE  | SITAEL, TAS-UK                                                                                                                        |        |                           |           |
| COMMENT      |                                                                                                                                       |        |                           |           |

| FuncR_C108   | Identification information                                                                                                |        |            | Mandatory |
|--------------|---------------------------------------------------------------------------------------------------------------------------|--------|------------|-----------|
| STATEMENT    | The SM shall be able to provide identification information including unique identifier<br>number and list of capabilities |        |            |           |
| VERIFICATION | Testing                                                                                                                   | COVERS | FuncR_A111 |           |
| RESPONSIBLE  | SITAEL, TAS-UK                                                                                                            |        |            |           |
| COMMENT      | To support automatic detection and plug and play operations                                                               |        |            |           |

| FuncR_C109   | Fault detection                                              |        |            | Mandatory |
|--------------|--------------------------------------------------------------|--------|------------|-----------|
| STATEMENT    | The SM shall be able to detect malfunction of its operations |        |            |           |
| VERIFICATION | Testing                                                      | COVERS | FuncR_A112 |           |
| RESPONSIBLE  | SITAEL                                                       |        |            |           |
| COMMENT      |                                                              |        |            |           |

#### <span id="page-56-0"></span>**3.5.2 C200: Performance requirements [PerfR]**

| PerfR_C201   | SM data interface rate for TM/TC                                                                                |        |                                         | Mandatory |
|--------------|-----------------------------------------------------------------------------------------------------------------|--------|-----------------------------------------|-----------|
| STATEMENT    | The data interface of the Spacecraft Module shall support a data rate of 1Mbps or<br>greater for TM/TC control. |        |                                         |           |
| VERIFICATION | Testing                                                                                                         | COVERS | MOSAR Operational Concept<br>PerfA_A202 |           |
| RESPONSIBLE  | SPACEAPPS, DLR, TAS-UK                                                                                          |        |                                         |           |
| COMMENT      | The TM/TC control of the platform should not rely on high data rate links with low<br>latency.                  |        |                                         |           |

{57}------------------------------------------------

![](_page_57_Picture_0.jpeg)

| PerfR_C202   | SM data interface rate for service data                                                                                                                                                                                              |        |                                         | Mandatory |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-----------------------------------------|-----------|
| STATEMENT    | The data interface of the Spacecraft Module shall support a data rate of 50 Mbps or<br>greater for service data.                                                                                                                     |        |                                         |           |
| VERIFICATION | Testing                                                                                                                                                                                                                              | COVERS | MOSAR Operational Concept<br>PerfA_A203 |           |
| RESPONSIBLE  | SPACEAPPS, DLR, TAS-UK                                                                                                                                                                                                               |        |                                         |           |
| COMMENT      | The services provided by the Spacecraft Module share the same data interface as<br>TM/TC and will have a higher bandwidth requirement. At 50 Mbps, a 4Mpixel image will<br>take several seconds to transfer across the data network. |        |                                         |           |

| PerfR_C203   | SM power interface rate                                                                                                        |        |                                      | Mandatory |
|--------------|--------------------------------------------------------------------------------------------------------------------------------|--------|--------------------------------------|-----------|
| STATEMENT    | The power interface of the SM shall support [1-2kW] [TBC] of power transfer                                                    |        |                                      |           |
| VERIFICATION | Testing                                                                                                                        | COVERS | Operational Concept<br>RD3PerfR_A202 |           |
| RESPONSIBLE  | SITAEL, SPACEAPPS                                                                                                              |        |                                      |           |
| COMMENT      | The power APM should be able to deliver the required power for the operations of the<br>other SM, WM and SI. Value TBC for PDR |        |                                      |           |

#### <span id="page-57-0"></span>**3.5.3 C300: Interface requirements [IntR]**

| IntR_C301    | SM power                                                                   |        |                     | Mandatory |
|--------------|----------------------------------------------------------------------------|--------|---------------------|-----------|
| STATEMENT    | The SM shall get power from the power interface of one of the connected SI |        |                     |           |
| VERIFICATION | Testing                                                                    | COVERS | Operational Concept |           |
| RESPONSIBLE  | SPACEAPPS                                                                  |        |                     |           |
| COMMENT      |                                                                            |        |                     |           |

| IntR_C302    | SM R-ICU power Up                                                                                                           |        |                         | Mandatory |
|--------------|-----------------------------------------------------------------------------------------------------------------------------|--------|-------------------------|-----------|
| STATEMENT    | The Spacecraft Module's R-ICU shall be powered up whenever external power is<br>supplied to any of its Standard Interfaces. |        |                         |           |
| VERIFICATION | Testing                                                                                                                     | COVERS | Operational Concept RD3 |           |
| RESPONSIBLE  | SITAEL, SPACEAPPS                                                                                                           |        |                         |           |
| COMMENT      | Enables plug and play of Spacecraft Modules.                                                                                |        |                         |           |

{58}------------------------------------------------

![](_page_58_Picture_0.jpeg)

| IntR_C303    | SM R-ICU to SI TM/TC                                                                                                                                          |        |                           | Mandatory |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|---------------------------|-----------|
| STATEMENT    | The R-ICU shall provide TM/TC control of the Standard Interfaces using CANbus                                                                                 |        |                           |           |
| VERIFICATION | Testing                                                                                                                                                       | COVERS | MOSAR Operational Concept |           |
| RESPONSIBLE  | SPACEAPPS, TAS-UK                                                                                                                                             |        |                           |           |
| COMMENT      | The R-ICU is the CAN bus master and the Standard Interfaces are all slaves to the R<br>ICU. CAN network technology is currently selected based on OG5 outputs |        |                           |           |

| IntR_C304    | SM mechanical interface to SI                                         |        |                     | Mandatory |
|--------------|-----------------------------------------------------------------------|--------|---------------------|-----------|
| STATEMENT    | The SM shall provide a mechanical interface connection to attach a SI |        |                     |           |
| VERIFICATION | Testing                                                               | COVERS | Operational Concept |           |
| RESPONSIBLE  | SITAEL                                                                |        |                     |           |
| COMMENT      |                                                                       |        |                     |           |

# <span id="page-58-0"></span>**3.5.4 C400: Design requirements [DesR]**

| DesR_C401    | SM structure                                                                                                                                                                                                                  |        |                   | Mandatory |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-------------------|-----------|
| STATEMENT    | The SM structure shall be composed by the following units:<br><br>6 lateral panels<br><br>12 beams<br><br>4 corners<br><br>Connection items (to connect all the units of the SMs with the structural<br>units of the SMs) |        |                   |           |
| VERIFICATION | Review of Design                                                                                                                                                                                                              | COVERS | Partner expertise |           |
| RESPONSIBLE  | SITAEL                                                                                                                                                                                                                        |        |                   |           |
| COMMENT      | For improved cross-compatibility of launchers and internal systems, SMs should target<br>to the form factor for a cubic 27U CubeSat (RD1).                                                                                    |        |                   |           |

{59}------------------------------------------------

![](_page_59_Picture_0.jpeg)

| DesR_C402    | Number of SI                                                                                                                                         |        |                                           | Mandatory |
|--------------|------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-------------------------------------------|-----------|
| STATEMENT    | All SM shall have a sufficient number of SI in order to manipulate them with the WM and<br>to couple them with each other and to the SVC or CLT      |        |                                           |           |
| VERIFICATION | Review of Design                                                                                                                                     | COVERS | Operational Concept RD3<br>Guidelines AD1 |           |
| RESPONSIBLE  | SITAEL, DLR                                                                                                                                          |        |                                           |           |
| COMMENT      | A maximum number of 3 SI are currently considered as optimization between<br>demonstration application and demonstration constraints (weight, costs) |        |                                           |           |

| DesR_C403    | SM mechanical loading                                                                                                                                                                     |        |                                           | Mandatory |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-------------------------------------------|-----------|
| STATEMENT    | The structure of the modules shall be able to carry its own mass under the gravity force<br>and the loads introduced by the "walking" robot-system during the manipulation of the<br>SMs. |        |                                           |           |
| VERIFICATION | Analysis, Testing                                                                                                                                                                         | COVERS | Operational Concept RD3<br>Guidelines AD1 |           |
| RESPONSIBLE  | SITAEL                                                                                                                                                                                    |        |                                           |           |
| COMMENT      |                                                                                                                                                                                           |        |                                           |           |

| DesR_C404    | SM mechanical loading data                                                                                             |        |                   | Mandatory |
|--------------|------------------------------------------------------------------------------------------------------------------------|--------|-------------------|-----------|
| STATEMENT    | The forces applied by the WM and the motion dynamics shall be provided for the design<br>of the SMs in the worst case. |        |                   |           |
| VERIFICATION | Analysis                                                                                                               | COVERS | Partner Expertise |           |
| RESPONSIBLE  | SITAEL                                                                                                                 |        |                   |           |
| COMMENT      |                                                                                                                        |        |                   |           |

| DesR_C405    | SM physical layout                                                                                                                                                                                                                                             |        |                   | Mandatory |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-------------------|-----------|
| STATEMENT    | The SMs physical layout shall allow the accommodation of all the equipment, by<br>guaranteeing the proper mechanically assembly, the thermo-mechanical behavior, the<br>SM mechanical/electrical integration and testing, as required by the test requirements |        |                   |           |
| VERIFICATION | Review of Design                                                                                                                                                                                                                                               | COVERS | Partner expertise |           |
| RESPONSIBLE  | SITAEL                                                                                                                                                                                                                                                         |        |                   |           |
| COMMENT      |                                                                                                                                                                                                                                                                |        |                   |           |

{60}------------------------------------------------

![](_page_60_Picture_0.jpeg)

| DesR_C406    | SM accommodation                                                                                                                                                                                                                                                                                                                                                                         |        |                   | Mandatory |
|--------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-------------------|-----------|
| STATEMENT    | The accommodation of the units shall take into account the following criteria:<br><br>Need of assembly and disassembly<br><br>Easy access to the electrical connectors, fixation points, grounding studs<br><br>Alignment requirements<br><br>Mass distribution<br><br>Envelope<br><br>Harness routing<br><br>FOV constraints (in the case of the integration of optical sensors) |        |                   |           |
| VERIFICATION | Review of Design, Inspection,<br>Testing                                                                                                                                                                                                                                                                                                                                                 | COVERS | Partner expertise |           |
| RESPONSIBLE  | SITAEL                                                                                                                                                                                                                                                                                                                                                                                   |        |                   |           |
| COMMENT      |                                                                                                                                                                                                                                                                                                                                                                                          |        |                   |           |

| DesR_C407    | SM accommodation flexibility                                                                                       |        |                                        | Mandatory |
|--------------|--------------------------------------------------------------------------------------------------------------------|--------|----------------------------------------|-----------|
| STATEMENT    | The SMs structure shall be flexible in order to allow the accommodation of different kind<br>of internal equipment |        |                                        |           |
| VERIFICATION | Inspection                                                                                                         | COVERS | Mission analysis RD2<br>Guidelines AD1 |           |
| RESPONSIBLE  | SITAEL                                                                                                             |        |                                        |           |
| COMMENT      |                                                                                                                    |        |                                        |           |

| DesR_C408    | SM face assignation                                                                                                                                                                        |        |                   | Mandatory |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-------------------|-----------|
| STATEMENT    | Only the assigned faces of the SM shall host the standard interfaces.<br>While, only one customized face for each SM shall host all the other units needed to<br>fulfill the SM functions. |        |                   |           |
| VERIFICATION | Review of Design                                                                                                                                                                           | COVERS | Partner Expertise |           |
| RESPONSIBLE  | SITAEL                                                                                                                                                                                     |        |                   |           |
| COMMENT      |                                                                                                                                                                                            |        |                   |           |

{61}------------------------------------------------

![](_page_61_Picture_0.jpeg)

| DesR_C409    | Thermal conditions                                                                                                       |        |                   | Mandatory |
|--------------|--------------------------------------------------------------------------------------------------------------------------|--------|-------------------|-----------|
| STATEMENT    | The SMs shall be design in order to guarantee the required thermal conditions to all the<br>units mounted inside the SMs |        |                   |           |
| VERIFICATION | Review of Design, Testing                                                                                                | COVERS | Partner Expertise |           |
| RESPONSIBLE  | SITAEL                                                                                                                   |        |                   |           |
| COMMENT      |                                                                                                                          |        |                   |           |

| DesR_C405    | Compatibility to environmental tests conditions                                                      |        |                           | Mandatory |
|--------------|------------------------------------------------------------------------------------------------------|--------|---------------------------|-----------|
| STATEMENT    | The design of the SM shall be such that it is able to withstand the test environmental<br>conditions |        |                           |           |
| VERIFICATION | Review of Design                                                                                     | COVERS | Demonstration constraints |           |
| RESPONSIBLE  | SITAEL                                                                                               |        |                           |           |
| COMMENT      |                                                                                                      |        |                           |           |

| DesR_C406    | Compatibility to space design                                                                                   |        |                                    | Mandatory |
|--------------|-----------------------------------------------------------------------------------------------------------------|--------|------------------------------------|-----------|
| STATEMENT    | The design of the SM shall be such that the later product is able to withstand the harsh<br>conditions in space |        |                                    |           |
| VERIFICATION | Review of Design                                                                                                | COVERS | Guidelines RD3 OG9-R09<br>OpR_S606 |           |
| RESPONSIBLE  | SITAEL                                                                                                          |        |                                    |           |
| COMMENT      |                                                                                                                 |        |                                    |           |

#### <span id="page-61-0"></span>**3.5.5 C500: Physical and resource requirements [PhyR]**

| PhyR_C501    | SM Weight                                                                                                                                  |        |           | Mandatory |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------|--------|-----------|-----------|
| STATEMENT    | The weight of the SM shall be minimized with a target mass of 7kg [TBC]                                                                    |        |           |           |
| VERIFICATION | Testing                                                                                                                                    | COVERS | PhyR_S501 |           |
| RESPONSIBLE  | SITAEL                                                                                                                                     |        |           |           |
| COMMENT      | For improved cross-compatibility of launchers and internal systems, SMs should target<br>to the form factor for a cubic 27U CubeSat (RD1). |        |           |           |

{62}------------------------------------------------

![](_page_62_Picture_0.jpeg)

| DesR_C502    | SM size                                                                                                                                    |  |  | Mandatory |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------|--|--|-----------|
| STATEMENT    | The SM shall be cubical in shape in size 300 to 400 mm (TBD) per side                                                                      |  |  |           |
| VERIFICATION | COVERS<br>Review of Design<br>Mission analysis RD2                                                                                         |  |  |           |
| RESPONSIBLE  | SITAEL                                                                                                                                     |  |  |           |
| COMMENT      | For improved cross-compatibility of launchers and internal systems, SMs should target<br>to the form factor for a cubic 27U CubeSat (RD1). |  |  |           |

# <span id="page-62-0"></span>**3.5.6 C600: Environmental and Operational requirements [OpR]**

# <span id="page-62-1"></span>**3.5.7 C700: Safety requirements [SafR]**

| SafR_C701    | SM hand manipulation                                  |  |  | Mandatory |
|--------------|-------------------------------------------------------|--|--|-----------|
| STATEMENT    | The SM shall be able to be safely manipulated by hand |  |  |           |
| VERIFICATION | COVERS<br>Inspection<br>Safety rules                  |  |  |           |
| RESPONSIBLE  | SITAEL                                                |  |  |           |
| COMMENT      |                                                       |  |  |           |

#### <span id="page-62-2"></span>**3.5.8 C800: Configuration and implementation requirements [ConfR]**

| ConfR_C801   | Demonstrator SM Configurations                                                                                                                                                                                                                                                              |        |                                                                                                                                                                                                                                                                                                                                                                             | Mandatory |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| STATEMENT    | A set of 7 SMs shall be developed, with the following functions:<br>●<br>4 ASMs:<br>○<br>○<br>TGT spacecraft.<br>○<br>○<br>management of the TGT SMs<br>●<br>2 APMs Optical Sensor Payload module (OSP): is an SM that exposes an<br>optical lens on one of its faces.<br>●<br>1 back-up SM |        | Data Management Subsystem module (DMS): this ASM hosts the<br>main Onboard Computer of the target spacecraft.<br>Power Subsystem (PWS): is managing the electrical power on the<br>Battery ORU module (BAT): is an SM that comprises a set of Lithium<br>ion batteries and the electronic to manage them.<br>Thermal Subsystem module (THS): is responsible for the thermal |           |
| VERIFICATION | Review of Design                                                                                                                                                                                                                                                                            | COVERS | FuncR_S112, FuncR_S114,<br>FuncR_S115<br>Scenarios Description                                                                                                                                                                                                                                                                                                              |           |
| RESPONSIBLE  | SITAEL                                                                                                                                                                                                                                                                                      |        |                                                                                                                                                                                                                                                                                                                                                                             |           |
| COMMENT      | Selection of ASM and APM are illustrative to the possible missions scenario, final<br>selection and specifications of each developed module at PDR                                                                                                                                          |        |                                                                                                                                                                                                                                                                                                                                                                             |           |

{63}------------------------------------------------

![](_page_63_Picture_0.jpeg)

# <span id="page-63-0"></span>**3.6 Standard Interfaces Requirements [Dxxx]**

# <span id="page-63-1"></span>**3.6.1 D100: Functional requirements [FuncR]**

| FuncR_D101   | Mechanical, Data and Electrical Interface                                                                                                                                                                                                                                                                |        |                  | Mandatory |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------------|-----------|
| STATEMENT    | The standard interface shall provide<br><br>a mechanical interface to mechanically couple two system components<br><br>an electrical interface to transfer electrical energy (power) between two system<br>components<br><br>a data interface to allow exchange of data between two system components |        |                  |           |
| VERIFICATION | Review of Design                                                                                                                                                                                                                                                                                         | COVERS | OG1-5 Review RD1 |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                                                                                                                                                                                                |        |                  |           |
| COMMENT      | MOSAR system components include Spacecraft Modules, Spacecraft Bus and Walking<br>Manipulator                                                                                                                                                                                                            |        |                  |           |

| FuncR_D102   | Thermal Interface                                                                                                                   |        |                  | Mandatory |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------|--------|------------------|-----------|
| STATEMENT    | The standard interface shall provide a thermal interface to allow active transfer of<br>thermal flow between two Spacecraft Modules |        |                  |           |
| VERIFICATION | Review of Design                                                                                                                    | COVERS | OG1-5 Review RD1 |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                           |        |                  |           |
| COMMENT      | In MOSAR, active thermal transfer is only considered between SM (not with the<br>Spacecraft Bus or Walking Manipulator)             |        |                  |           |

| FuncR_D103   | Passive Coupling                                                                                                                                       |        |                  | Mandatory |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------------|-----------|
| STATEMENT    | The standard interface shall allow the mechanical, power, data and thermal coupling<br>with another interface that cannot provide actuation            |        |                  |           |
| VERIFICATION | Review of Design                                                                                                                                       | COVERS | OG1-5 Review RD1 |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                                              |        |                  |           |
| COMMENT      | Passive configurations of the SI is currently envisaged in the scenarios for costs<br>reductions (could also have an interest for future exploitation) |        |                  |           |

{64}------------------------------------------------

![](_page_64_Picture_0.jpeg)

| FuncR_D104   | Passive Decoupling                                                                                                                             |        |                  | Mandatory |
|--------------|------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------------|-----------|
| STATEMENT    | The standard interface shall allow the mechanical, power, data and thermal de-coupling<br>with another interface that cannot provide actuation |        |                  |           |
| VERIFICATION | Review of Design                                                                                                                               | COVERS | OG1-5 Review RD1 |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                                      |        |                  |           |
| COMMENT      |                                                                                                                                                |        |                  |           |

| FuncR_D105   | Electrical Interface Protection                                               |        |                                       | Mandatory |
|--------------|-------------------------------------------------------------------------------|--------|---------------------------------------|-----------|
| STATEMENT    | The electrical interface shall have an overcurrent and overvoltage protection |        |                                       |           |
| VERIFICATION | Review of Design / Testing                                                    | COVERS | OG5 Requirement<br>Internal Expertise |           |
| RESPONSIBLE  | SPACEAPPS                                                                     |        |                                       |           |
| COMMENT      |                                                                               |        |                                       |           |

| FuncR_D106   | Electrical Interface Switch                                                                                                   |        |            | Mandatory |
|--------------|-------------------------------------------------------------------------------------------------------------------------------|--------|------------|-----------|
| STATEMENT    | The electrical interface shall incorporate a bidirectional power switch to control current<br>flow at the interface.          |        |            |           |
| VERIFICATION | Review of Design / Testing                                                                                                    | COVERS | FuncR_S122 |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                     |        |            |           |
| COMMENT      | Required to support (re)-routing of electrical power. Could also be managed by a central<br>power distribution unit in the SM |        |            |           |

| FuncR_D107   | Electrical Interface Telemetry                                                                                                          |        |            | Mandatory |  |
|--------------|-----------------------------------------------------------------------------------------------------------------------------------------|--------|------------|-----------|--|
| STATEMENT    | The electrical interface shall provide voltage and current telemetry at the power bus<br>system level, in both power transfer direction |        |            |           |  |
| VERIFICATION | Testing                                                                                                                                 | COVERS | FuncR_S122 |           |  |
| RESPONSIBLE  | SPACEAPPS                                                                                                                               |        |            |           |  |
| COMMENT      | Required to monitor (re)-routing of electrical power.                                                                                   |        |            |           |  |

{65}------------------------------------------------

![](_page_65_Picture_0.jpeg)

| FuncR_D108   | Data Interface Support                                                                                                         |  |  | Mandatory |
|--------------|--------------------------------------------------------------------------------------------------------------------------------|--|--|-----------|
| STATEMENT    | The data interface shall support at least one technology with capabilities of dynamic<br>data bus re-configuration and routing |  |  |           |
| VERIFICATION | COVERS<br>Review of Design<br>DesR_A407                                                                                        |  |  |           |
| RESPONSIBLE  | SPACEAPPS / TAS-UK                                                                                                             |  |  |           |
| COMMENT      | Current selected technology in MOSAR is SpaceWire, based on OG4 outputs                                                        |  |  |           |

| FuncR_D109   | SI Telemetry                                                                                                                                                                                                                                                                                                                                                                                                                                                      |        |                                             | Mandatory |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|---------------------------------------------|-----------|
| STATEMENT    | The SI shall measure and store the following local SI parameters:<br><br>Temperature (Power electronics if local, structure)<br><br>Alignment / proximity status<br><br>Locking status<br><br>SI orientation (in relation with design symmetry)<br><br>Data/Power interface status<br><br>Thermal interface status<br><br>Motor position (incremental or absolute) / Mechanism position (absolute)<br><br>Motor current<br><br>Controller supply voltage |        |                                             |           |
| VERIFICATION | Review of Design / Testing                                                                                                                                                                                                                                                                                                                                                                                                                                        | COVERS | OG1-5 Review RD1<br>Operational Concept RD3 |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                                                                                                                                                                                                                                                                                                                                                         |        |                                             |           |
| COMMENT      | Needed to monitor the function of the SI and support autonomous operation in MOSAR                                                                                                                                                                                                                                                                                                                                                                                |        |                                             |           |

#### <span id="page-65-0"></span>**3.6.2 D200: Performance requirements [PerfR]**

| PerfR_D201   | Mechanical Loads                                                                                                                                                                                                                                                                                                                                                                        |        |                              | Mandatory |
|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------------------------|-----------|
| STATEMENT    | The mechanical interface shall withstand, in connected mode, all mechanical loads<br>induced by the demonstration operations:<br><br>Axial Force: 250 / 160 N<br><br>Radial Force: 250 / 160 N<br><br>Bending Moment: 204 / 84 Nm<br><br>Torsion: TBD Nm<br>As function of the gravity compensation of the SM (TBC).                                                                |        |                              |           |
| VERIFICATION | Analysis / Testing                                                                                                                                                                                                                                                                                                                                                                      | COVERS | OG1-5 Review RD1<br>OpR_A602 |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                                                                                                                                                                                                                                                                               |        |                              |           |
| COMMENT      | Best current estimations<br>Required load transfer will depend on the configuration of the demonstrator setup and<br>the possible application of gravity mitigation technics. Due to the complexity of the<br>operations and motions, we currently target to not implement gravity compensation (left<br>number). We could however still envisage compensation of the SM (right number) |        |                              |           |

{66}------------------------------------------------

![](_page_66_Picture_0.jpeg)

| PerfR_D202   | Positioning Tolerance                                                                 |  |  | Mandatory |
|--------------|---------------------------------------------------------------------------------------|--|--|-----------|
| STATEMENT    | The mechanical interface shall maximize positioning tolerance for guidance and mating |  |  |           |
| VERIFICATION | Analysis / Testing<br>COVERS<br>OG1-5 Review RD1                                      |  |  |           |
| RESPONSIBLE  | SPACEAPPS                                                                             |  |  |           |
| COMMENT      |                                                                                       |  |  |           |

| PerfR_D203   | Power Transfer Rating                                                                                                                                                                                             |        |            | Mandatory |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------|-----------|
| STATEMENT    | The electrical interface shall be capable of supporting [1-2kW] (TBC) of power transfer,<br>as required by the MOSAR demonstration<br>The power interface of the SM shall support [1-2kW] [TBC] of power transfer |        |            |           |
| VERIFICATION | Analysis / Testing                                                                                                                                                                                                | COVERS | PerfR_C203 |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                                                                                                         |        |            |           |
| COMMENT      | Value TBC for PDR                                                                                                                                                                                                 |        |            |           |

| PerfR_D204   | Data Interface Rating                                                                                                                   |  |  | Mandatory |
|--------------|-----------------------------------------------------------------------------------------------------------------------------------------|--|--|-----------|
| STATEMENT    | The data interface shall allow a data rate of minimum 50Mbit/s                                                                          |  |  |           |
| VERIFICATION | Analysis / Testing<br>COVERS<br>PerfR_A202                                                                                              |  |  |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                               |  |  |           |
| COMMENT      | To support the recording and processing of large amounts of data between modules<br>and with the spacecraft, value TBC during PDR phase |  |  |           |

| PerfR_D205   | Thermal Interface Rating                                          |        |                  | Mandatory |
|--------------|-------------------------------------------------------------------|--------|------------------|-----------|
| STATEMENT    | The thermal interface shall allow a thermal flow rating of: TBD W |        |                  |           |
| VERIFICATION | Analysis / Testing                                                | COVERS | OG1-5 Review RD1 |           |
| RESPONSIBLE  | MAGSOAR / SPACEAPPS                                               |        |                  |           |
| COMMENT      |                                                                   |        |                  |           |

{67}------------------------------------------------

![](_page_67_Picture_0.jpeg)

## <span id="page-67-0"></span>**3.6.3 D300: Interface requirements [IntR]**

| IntR_D301    | Mechanical Interface to Components                                                                                                                                                                                  |        |                                          | Mandatory |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------------------------------------|-----------|
| STATEMENT    | The standard interface shall provide a mechanical connection to the modules,<br>spacecraft bus or robotic base/end-effector manipulator, compatible with the mechanical<br>loads transferred through the interface. |        |                                          |           |
| VERIFICATION | Review of Design / Analysis                                                                                                                                                                                         | COVERS | OG1-5 Review RD1<br>IntR_B307, IntR_C304 |           |
| RESPONSIBLE  | SPACEAPPS, SITAEL                                                                                                                                                                                                   |        |                                          |           |
| COMMENT      |                                                                                                                                                                                                                     |        |                                          |           |

| IntR_D302    | Harnessing to Components                                                                                                                                                  |        |                  | Mandatory |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------------|-----------|
| STATEMENT    | The standard interface shall provide internal harnessing to connect power, data and<br>control buses from the module, spacecraft or robotic base/end-effector manipulator |        |                  |           |
| VERIFICATION | Review of Design                                                                                                                                                          | COVERS | OG1-5 Review RD1 |           |
| RESPONSIBLE  | SPACEAPPS, SITAEL                                                                                                                                                         |        |                  |           |
| COMMENT      |                                                                                                                                                                           |        |                  |           |

| IntR_D303    | Interface to Module Thermal System                                                        |        |                  | Mandatory |  |
|--------------|-------------------------------------------------------------------------------------------|--------|------------------|-----------|--|
| STATEMENT    | The thermal interface shall enable thermal connection to the thermal module sub<br>system |        |                  |           |  |
| VERIFICATION | Review of Design                                                                          | COVERS | OG1-5 Review RD1 |           |  |
| RESPONSIBLE  | SPACEAPPS, SITAEL, MAGSOAR                                                                |        |                  |           |  |
| COMMENT      |                                                                                           |        |                  |           |  |

| IntR_D304    | Power Distribution Unit                                                                                                                                                                           |        |                   | Mandatory |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-------------------|-----------|
| STATEMENT    | The SI shall be interfaced with a Power Distribution Unit (PDU) to provide low-level<br>voltage power rails to supply the internal components of the SI (controller, sensors and<br>motor drives) |        |                   |           |
| VERIFICATION | Review of Design                                                                                                                                                                                  | COVERS | Partner Expertise |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                                                                                         |        |                   |           |
| COMMENT      | The PDU could be local to the SI or shared at module level                                                                                                                                        |        |                   |           |

{68}------------------------------------------------

![](_page_68_Picture_0.jpeg)

| IntR_D305    | Standard Interface TM/TC                                                                                                                                                                                                                                      |        |            | Mandatory |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------|-----------|
| STATEMENT    | The SI shall be able to send/receive local TM/TC to/from the module or spacecraft OBC<br>TM: See FuncR_D109 list<br>TC:<br><br>Coupling / de-coupling (TBC for intermediate states)<br><br>Electrical power transfer on/off<br><br>Low-level control (TBC) |        |            |           |
| VERIFICATION | Testing                                                                                                                                                                                                                                                       | COVERS | FuncR_A104 |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                                                                                                                                                     |        |            |           |
| COMMENT      | Based on OG5 developments, CAN is the current selected technology for SI TM/TC                                                                                                                                                                                |        |            |           |

| IntR_D306    | Redundant Data/Power/Control Interface                                |                     |  | Mandatory |
|--------------|-----------------------------------------------------------------------|---------------------|--|-----------|
| STATEMENT    | The SI shall feature redundant data, power and control interface      |                     |  |           |
| VERIFICATION | Review of Design                                                      | COVERS<br>SafR_S702 |  |           |
| RESPONSIBLE  | SPACEAPPS                                                             |                     |  |           |
| COMMENT      | In case of failure, the SI shall be able to switch to a redundant bus |                     |  |           |

#### <span id="page-68-0"></span>**3.6.4 D400: Design requirements [DesR]**

| DesR_D401    | Androgynous Design                                                                                                  |        |                  | Mandatory |
|--------------|---------------------------------------------------------------------------------------------------------------------|--------|------------------|-----------|
| STATEMENT    | The standard interface shall have an androgynous design, including mechanical, data,<br>power and thermal interface |        |                  |           |
| VERIFICATION | Review of Design                                                                                                    | COVERS | OG1-5 Review RD1 |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                           |        |                  |           |
| COMMENT      |                                                                                                                     |        |                  |           |

| DesR_D402    | Design Symmetry                                                                                                               |        |                                | Mandatory |
|--------------|-------------------------------------------------------------------------------------------------------------------------------|--------|--------------------------------|-----------|
| STATEMENT    | The standard interface shall present a 90deg. rotational symmetry, including<br>mechanical, data, power and thermal interface |        |                                |           |
| VERIFICATION | Review of Design                                                                                                              | COVERS | OG1-5 Review RD1<br>ConfR_S902 |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                     |        |                                |           |
| COMMENT      | The standard interface shall allow module connections without restriction on relative<br>module orientation                   |        |                                |           |

{69}------------------------------------------------

![](_page_69_Picture_0.jpeg)

| DesR_D403    | Diagonal Engagement                                                           |        |                                             | Mandatory |
|--------------|-------------------------------------------------------------------------------|--------|---------------------------------------------|-----------|
| STATEMENT    | The standard interface shall allow diagonal engagement up to 55 deg           |        |                                             |           |
| VERIFICATION | Review of Design / Testing                                                    | COVERS | OG1-5 Review RD1<br>Operational Concept RD3 |           |
| RESPONSIBLE  | SPACEAPPS                                                                     |        |                                             |           |
| COMMENT      | To enable multiple simultaneous approach and connection (e.g. corner example) |        |                                             |           |

| DesR_D404    | Form-Fit Guidance                                                                                                                                             |        |                                             | Mandatory |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|---------------------------------------------|-----------|
| STATEMENT    | The standard interface shall provide guidance form-fit features                                                                                               |        |                                             |           |
| VERIFICATION | Review of Design / Testing                                                                                                                                    | COVERS | OG1-5 Review RD1<br>Operational Concept RD3 |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                                                     |        |                                             |           |
| COMMENT      | To support the alignment process between two interfaces, specifically when multiple<br>connections are considered, without requiring external guidance system |        |                                             |           |

| DesR_D405    | SI Costs                                                                                                            |        |           | Mandatory |
|--------------|---------------------------------------------------------------------------------------------------------------------|--------|-----------|-----------|
| STATEMENT    | The design of the SI shall take into account optimization of the manufacturing and<br>integration costs             |        |           |           |
| VERIFICATION | Analysis                                                                                                            | COVERS | DesR_S403 |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                           |        |           |           |
| COMMENT      | Cost should be a design driver considering the large quantity of interfaces in the<br>proposed operational concept. |        |           |           |

# <span id="page-69-0"></span>**3.6.5 D500: Physical requirements [PhyR]**

| PhyR_D501    | Standard Interface Mass                                      |        |                                    | Mandatory |
|--------------|--------------------------------------------------------------|--------|------------------------------------|-----------|
| STATEMENT    | The standard interface shall be optimized regarding the mass |        |                                    |           |
| VERIFICATION | Testing                                                      | COVERS | PhyR_S501, PhyR_B501,<br>PhyR_C501 |           |
| RESPONSIBLE  | SPACEAPPS                                                    |        |                                    |           |
| COMMENT      |                                                              |        |                                    |           |

{70}------------------------------------------------

![](_page_70_Picture_0.jpeg)

| PhyR_D502    | Standard Interface Volume                                           |        |           | Mandatory |
|--------------|---------------------------------------------------------------------|--------|-----------|-----------|
| STATEMENT    | The standard interface shall be optimized regarding size and volume |        |           |           |
| VERIFICATION | Testing                                                             | COVERS | PhyR_S502 |           |
| RESPONSIBLE  | SPACEAPPS                                                           |        |           |           |
| COMMENT      | To reduce constraints on the module design and integration          |        |           |           |

## <span id="page-70-0"></span>**3.6.6 D600: Environmental and Operational requirements [OpR]**

| PhyR_D601    | Standard Interface ShutDown                                                                                                                                                                                                       |        |                           | Desirable |
|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|---------------------------|-----------|
| STATEMENT    | The standard interface (or a part of it) shall be able to be switched off/on (behave as a<br>passive plug), while ensuring data and power transfer.                                                                               |        |                           |           |
| VERIFICATION | Testing                                                                                                                                                                                                                           | COVERS | MOSAR Operational Concept |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                                                                                                                         |        |                           |           |
| COMMENT      | In regards to the total mission time, the operation time of the standard interface is very<br>small. For energy optimization, it could be interesting to be able to switch off the<br>component (and be able to revive it later). |        |                           |           |

| PhyR_D602    | Standard Interface Power Consumption                               |        |                                            | Mandatory |
|--------------|--------------------------------------------------------------------|--------|--------------------------------------------|-----------|
| STATEMENT    | The power consumption of the standard interface shall be minimized |        |                                            |           |
| VERIFICATION | Testing                                                            | COVERS | MOSAR Operational Concept<br>OG5 Expertise |           |
| RESPONSIBLE  | SPACEAPPS                                                          |        |                                            |           |
| COMMENT      | Values TBC during PDR phase                                        |        |                                            |           |

| PhyR_D603    | Coupling Time                                                                   |        |                           | Mandatory |
|--------------|---------------------------------------------------------------------------------|--------|---------------------------|-----------|
| STATEMENT    | The coupling time between two standard interfaces shall be minimized            |        |                           |           |
| VERIFICATION | Testing                                                                         | COVERS | MOSAR Operational Concept |           |
| RESPONSIBLE  | SPACEAPPS                                                                       |        |                           |           |
| COMMENT      | MOSAR demonstration will require a lot of successive mating/demating operations |        |                           |           |

{71}------------------------------------------------

![](_page_71_Picture_0.jpeg)

## <span id="page-71-0"></span>**3.6.7 D700: Safety requirements [SafR]**

| SafR_D801    | SI Safe Manipulation                                                                                                                                          |        |              | Mandatory |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|--------------|-----------|
| STATEMENT    | The SI shall be safe to be manipulated during integration within SM, WM or Spacecraft<br>Buses. If there exist potential risks, they shall be well documented |        |              |           |
| VERIFICATION | Inspection                                                                                                                                                    | COVERS | Safety Rules |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                                                     |        |              |           |
| COMMENT      |                                                                                                                                                               |        |              |           |

## <span id="page-71-1"></span>**3.6.8 D800: Configuration and implementation requirements [ConfR]**

| PhyR_D901    | SI Design Configurations                                                                                                                                                                                                                                                                                                     |        |                                                       | Mandatory |
|--------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-------------------------------------------------------|-----------|
| STATEMENT    | The standard interface shall be declined in different configurations that are:<br><br>Active<br><br>Passive (not active behavior but can be couple and transmit data and power)<br><br>Mechanical (not active and can only be coupled)<br><br>Thermal (including thermal interface connectors, either active or passive) |        |                                                       |           |
| VERIFICATION | Review of Design / Testing                                                                                                                                                                                                                                                                                                   | COVERS | OGs costs and physical<br>characteristics constraints |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                                                                                                                                                                                                                    |        |                                                       |           |
| COMMENT      | This is mainly to support costs and volume/weight reduction in the ground<br>demonstrators. This could also be applicable in future mission depending on specific<br>mission characteristics.                                                                                                                                |        |                                                       |           |

{72}------------------------------------------------

![](_page_72_Picture_0.jpeg)

# <span id="page-72-0"></span>**3.7 Planner and Simulator Requirements [Exxx]**

# <span id="page-72-1"></span>**3.7.1 E100: Functional requirements [FuncR]**

| FuncR_E101   | Design and Simulation Tool Purpose                                                                                                                                                                                                |        |                        | Mandatory |
|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------------------|-----------|
| STATEMENT    | The design and simulation software shall be able to simulate the system with all related<br>robotic elements and tasks (e.g. reconfiguration) as well as create a robotic compatible<br>servicing plan for the satellite platform |        |                        |           |
| VERIFICATION | Testing                                                                                                                                                                                                                           | COVERS | FuncR_S105, FuncR_S106 |           |
| RESPONSIBLE  | DLR/GMV                                                                                                                                                                                                                           |        |                        |           |
| COMMENT      |                                                                                                                                                                                                                                   |        |                        |           |

| FuncR_E102   | Design Software                                                                                                                                                                                                                            |        |            | Mandatory |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------|-----------|
| STATEMENT    | The software shall support engineers developing new components and satellites and<br>shall give system integrators the chance to test the entire satellite including all relevant<br>aspects of on-orbit assembly and servicing operation. |        |            |           |
| VERIFICATION | Review of Design                                                                                                                                                                                                                           | COVERS | FuncR_S105 |           |
| RESPONSIBLE  | DLR                                                                                                                                                                                                                                        |        |            |           |
| COMMENT      |                                                                                                                                                                                                                                            |        |            |           |

| FuncR_E103   | System Simulation                                                                                                                                                                                               |        |            | Mandatory |
|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------|-----------|
| STATEMENT    | The software shall allow users to simulation and test high-modular building<br>block space system architectures with regard to the requirements and<br>constraints of robotics, structure and the entire system |        |            |           |
| VERIFICATION | Review of Design                                                                                                                                                                                                | COVERS | FuncR_S106 |           |
| RESPONSIBLE  | DLR                                                                                                                                                                                                             |        |            |           |
| COMMENT      |                                                                                                                                                                                                                 |        |            |           |

{73}------------------------------------------------

![](_page_73_Picture_0.jpeg)

| FuncR_E104   | Task Planning and Simulation                                                             |        |                | Mandatory |
|--------------|------------------------------------------------------------------------------------------|--------|----------------|-----------|
| STATEMENT    | The software shall be used to plan and to test the servicing task of the robot<br>system |        |                |           |
| VERIFICATION | Testing                                                                                  | COVERS | Guidelines AD1 |           |
| RESPONSIBLE  | GMV (Planner) and DLR (Test)                                                             |        |                |           |
| COMMENT      |                                                                                          |        |                |           |

| FuncR_E105   | Simulation Topics                                                                                                                                        |        |                | Mandatory |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|--------|----------------|-----------|
| STATEMENT    | The software shall allow to test and simulate the demonstration scenario regarding<br>mechanical and thermal loads as well as distribution of resources. |        |                |           |
| VERIFICATION | Review of Design                                                                                                                                         | COVERS | Guidelines AD1 |           |
| RESPONSIBLE  | DLR                                                                                                                                                      |        |                |           |
| COMMENT      |                                                                                                                                                          |        |                |           |

| FuncR_E106   | Simulation of Reconfiguration                                                                                                                                                                       |        |                | Mandatory |
|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|----------------|-----------|
| STATEMENT    | The software shall allow the addition of functional modules to the spacecraft, perform<br>reconfiguration process, and simulate the servicing task considering dedicated robotic<br>specifications. |        |                |           |
| VERIFICATION | Review of Design                                                                                                                                                                                    | COVERS | Guidelines AD1 |           |
| RESPONSIBLE  | DLR                                                                                                                                                                                                 |        |                |           |
| COMMENT      |                                                                                                                                                                                                     |        |                |           |

| FuncR_E108   | Environmental Conditions Simulation                                                                                                   |        |                      | Optional |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------|--------|----------------------|----------|
| STATEMENT    | The simulation software shall be able to simulate the environmental conditions in LEO                                                 |        |                      |          |
| VERIFICATION | Inspection                                                                                                                            | COVERS | Mission Analysis RD2 |          |
| RESPONSIBLE  | DLR                                                                                                                                   |        |                      |          |
| COMMENT      | The effects of orbital disturbances and their respective relevance shall be verified based<br>on dedicated simulation output signals. |        |                      |          |

{74}------------------------------------------------

![](_page_74_Picture_0.jpeg)

| FuncR_E109   | Manipulator Dynamics Simulation                                                                                                                                   |        |                         | Mandatory |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-------------------------|-----------|
| STATEMENT    | The simulation software shall be able to represent manipulator dynamics like motor<br>dynamics and joint flexibilities, if relevant in the demonstrator scenario. |        |                         |           |
| VERIFICATION | Inspection                                                                                                                                                        | COVERS | Operational Concept RD3 |           |
| RESPONSIBLE  | DLR                                                                                                                                                               |        |                         |           |
| COMMENT      |                                                                                                                                                                   |        |                         |           |

# <span id="page-74-0"></span>**3.7.2 D200: Performance requirements [PerfR]**

| PerfR_E201   | Simulation Real-Time Performance                                                                                   |        |                         | Desirable |
|--------------|--------------------------------------------------------------------------------------------------------------------|--------|-------------------------|-----------|
| STATEMENT    | The simulation software shall be able to compute the reconfiguration scenarios in real<br>time as far as possible. |        |                         |           |
| VERIFICATION | Testing                                                                                                            | COVERS | Operational Concept RD3 |           |
| RESPONSIBLE  | DLR                                                                                                                |        |                         |           |
| COMMENT      | The real-time performance is verified during reference simulation runs (TBD).                                      |        |                         |           |

| PerfR_E202   | Number of SM in Simulation                                                                                                                   |        |                         | Mandatory |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------|--------|-------------------------|-----------|
| STATEMENT    | The simulation software shall be able to process as many replaceable modules models<br>as required according to the demonstration scenarios. |        |                         |           |
| VERIFICATION | Testing                                                                                                                                      | COVERS | Operational Concept RD3 |           |
| RESPONSIBLE  | DLR                                                                                                                                          |        |                         |           |
| COMMENT      | The ability to handle a sufficient number of modules is verified during reference<br>simulation runs (TBD).                                  |        |                         |           |

#### <span id="page-74-1"></span>**3.7.3 D300: Interface requirements [IntR]**

| IntR_E301    | Simulator Input Interfaces                                                                                                       |        |                         | Mandatory |
|--------------|----------------------------------------------------------------------------------------------------------------------------------|--------|-------------------------|-----------|
| STATEMENT    | The simulation software of the FES shall be able to receive joint control inputs from<br>external joint controllers and planners |        |                         |           |
| VERIFICATION | Testing                                                                                                                          | COVERS | Operational Concept RD3 |           |
| RESPONSIBLE  | DLR                                                                                                                              |        |                         |           |
| COMMENT      |                                                                                                                                  |        |                         |           |

{75}------------------------------------------------

![](_page_75_Picture_0.jpeg)

| IntR_E302    | Simulator Output Interfaces                                                                                                                                               |        |                         | Mandatory |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-------------------------|-----------|
| STATEMENT    | The simulation software of the FES shall be able to feed back sensor information from<br>sensor models and simulation states to external controllers or a control console |        |                         |           |
| VERIFICATION | Testing                                                                                                                                                                   | COVERS | Operational Concept RD3 |           |
| RESPONSIBLE  | DLR                                                                                                                                                                       |        |                         |           |
| COMMENT      |                                                                                                                                                                           |        |                         |           |

| IntR_E303    | Simulator Communication Interface                                                                |  |  | Optional |
|--------------|--------------------------------------------------------------------------------------------------|--|--|----------|
| STATEMENT    | The simulation software shall be able to communicate with external entities via TCP/IP<br>or UDP |  |  |          |
| VERIFICATION | COVERS<br>Testing<br>Operational Concept RD3                                                     |  |  |          |
| RESPONSIBLE  | DLR                                                                                              |  |  |          |
| COMMENT      |                                                                                                  |  |  |          |

| IntR_E304    | Generation of plan for onboard execution                                                                                                                                                           |        |                         | Mandatory |  |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-------------------------|-----------|--|
| STATEMENT    | The ground instance of the ERGO Agent used to generate and validate the<br>reconfiguration plan shall generate a static plan that can be transferred to and executed<br>by the onboard ERGO Agent. |        |                         |           |  |
| VERIFICATION | Testing                                                                                                                                                                                            | COVERS | Operational Concept RD3 |           |  |
| RESPONSIBLE  | GMV                                                                                                                                                                                                |        |                         |           |  |
| COMMENT      |                                                                                                                                                                                                    |        |                         |           |  |

<span id="page-75-0"></span>**3.7.4 D400: Design requirements [DesR]**

N./A.

{76}------------------------------------------------

![](_page_76_Picture_0.jpeg)

#### <span id="page-76-0"></span>**3.7.5 D500: Physical and resource requirements [PhyR]**

| PhyR_E501    | Simulator Computing Platform                         |        |  | Mandatory |
|--------------|------------------------------------------------------|--------|--|-----------|
| STATEMENT    | The FES shall run on an individual single-purpose PC |        |  |           |
| VERIFICATION | Inspection / Testing                                 | COVERS |  |           |
| RESPONSIBLE  | DLR                                                  |        |  |           |
| COMMENT      |                                                      |        |  |           |

# <span id="page-76-1"></span>**3.7.6 D600: Environmental and Operational requirements [OpR]**

N./A.

# <span id="page-76-2"></span>**3.7.7 D700: Safety requirements [SafR]**

N./A.

## <span id="page-76-3"></span>**3.7.8 D800: Configuration and implementation requirements [ConfR]**

| ConfR_E901   | Scenario Simulation Models                                                             |        |                   | Desirable |
|--------------|----------------------------------------------------------------------------------------|--------|-------------------|-----------|
| STATEMENT    | For each scenario to be demonstrated, an individual simulation model shall be provided |        |                   |           |
| VERIFICATION | Inspection                                                                             | COVERS | Partner Expertise |           |
| RESPONSIBLE  | DLR                                                                                    |        |                   |           |
| COMMENT      | In order to minimize re-configuration activities                                       |        |                   |           |

{77}------------------------------------------------

![](_page_77_Picture_0.jpeg)

# <span id="page-77-0"></span>**3.8 Software Requirements [Fxxx]**

This section lists the requirements for on-board software that is run on the MOSAR demonstrator SVC platform, SMs and WM for control and management of the system.

# <span id="page-77-1"></span>**3.8.1 F100: Functional requirements [FuncR]**

| FuncR_F101   | Extension of TASTE for reconfigurable systems                                                                                                                                 |        |                  | Mandatory |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------------|-----------|
| STATEMENT    | The TASTE framework shall be extended to support modelling and code generation for<br>software systems that can switch between different configurations known at design time. |        |                  |           |
| VERIFICATION | Testing                                                                                                                                                                       | COVERS | OG1-5 Review RD1 |           |
| RESPONSIBLE  | ELLI, UBREST, GMV                                                                                                                                                             |        |                  |           |
| COMMENT      |                                                                                                                                                                               |        |                  |           |

| FuncR_F102   | TASTE-DDS bridge                                                                                                                                                                                                                                                                                                  |  |  | Desirable |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|--|-----------|
| STATEMENT    | A middleware bridge generator that enables the communication between TASTE and<br>DDS in runtime should be developed in order to assess the capabilities of the software<br>and modelling environment needed to support the reconfiguration of an onboard system<br>with configurations not known at design time. |  |  |           |
| VERIFICATION | COVERS<br>Testing<br>OG1-5 Review RD1                                                                                                                                                                                                                                                                             |  |  |           |
| RESPONSIBLE  | ELLI, UBREST, GMV                                                                                                                                                                                                                                                                                                 |  |  |           |
| COMMENT      |                                                                                                                                                                                                                                                                                                                   |  |  |           |

| FuncR_F103   | DDS over SpaceWire                                                                                                                         |        |                  | Desirable |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------|--------|------------------|-----------|
| STATEMENT    | An existing open DDS implementation should be adapted to run over SpaceWire links<br>so that it can be deployed in the MOSAR demonstrator. |        |                  |           |
| VERIFICATION | Testing                                                                                                                                    | COVERS | OG1-5 Review RD1 |           |
| RESPONSIBLE  | GMV                                                                                                                                        |        |                  |           |
| COMMENT      | Feasibility needs to be assessed                                                                                                           |        |                  |           |

{78}------------------------------------------------

![](_page_78_Picture_0.jpeg)

| FuncR_F104   | Large data transfer over SpaceWire                                                                                                                                                                             |        |                  | Optional |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------------|----------|
| STATEMENT    | The software should provide a common mechanism to transfer large data messages<br>(1KiB to 1MiB) over SpaceWire links, in order to transfer images from the camera<br>sensor to the OBC and the ground system. |        |                  |          |
| VERIFICATION | Testing                                                                                                                                                                                                        | COVERS | OG1-5 Review RD1 |          |
| RESPONSIBLE  | GMV, TAS-F, USTRAT, SPACEAPPS                                                                                                                                                                                  |        |                  |          |
| COMMENT      | Feasibility needs to be assessed                                                                                                                                                                               |        |                  |          |

| FuncR_F105   | ERGO robotic arm driver for WM                                                                                                                                                           |        |                  | Mandatory |
|--------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------------|-----------|
| STATEMENT    | A robotic arm driver component shall be developed to execute the robot plan actions on<br>the WM and return the observations needed by the Agent to manage the execution of<br>the plan. |        |                  |           |
| VERIFICATION | Testing                                                                                                                                                                                  | COVERS | OG1-5 Review RD1 |           |
| RESPONSIBLE  | GMV, DLR                                                                                                                                                                                 |        |                  |           |
| COMMENT      |                                                                                                                                                                                          |        |                  |           |

| FuncR_F106   | ERGO Agent for plan execution                                                                                                                               |        |                  | Mandatory |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------------|-----------|
| STATEMENT    | An instance of the ERGO Agent shall be deployed on the OBC to command and monitor<br>the execution of the robotic reconfiguration plan generated on ground. |        |                  |           |
| VERIFICATION | Testing                                                                                                                                                     | COVERS | OG1-5 Review RD1 |           |
| RESPONSIBLE  | GMV                                                                                                                                                         |        |                  |           |
| COMMENT      |                                                                                                                                                             |        |                  |           |

# <span id="page-78-0"></span>**3.8.2 F200: Performance requirements [PerfR]**

N./A.

{79}------------------------------------------------

![](_page_79_Picture_0.jpeg)

## <span id="page-79-0"></span>**3.8.3 F300: Interface requirements [IntR]**

| IntR_F301    | PUS services                                                                                                                                                                                                                              |        |                  | Mandatory |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------------|-----------|
| STATEMENT    | The monitoring and control from the ground system of the onboard system status and<br>the execution of the robotic reconfiguration plan shall be done using the ESROCOS<br>PUS services library, extended with mission-specific services. |        |                  |           |
| VERIFICATION | Testing                                                                                                                                                                                                                                   | COVERS | OG1-5 Review RD1 |           |
| RESPONSIBLE  | GMV                                                                                                                                                                                                                                       |        |                  |           |
| COMMENT      |                                                                                                                                                                                                                                           |        |                  |           |

## <span id="page-79-1"></span>**3.8.4 F400: Design requirements [DesR]**

| DesR_F401    | Robotics data types                                                                                                                                                                                                                  |        |                  | Mandatory |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------------|-----------|
| STATEMENT    | The data types used for the interface between the ERGO Agent and the Functional<br>Layer shall be modelled in ASN.1. If a suitable data type is available from ESROCOS, it<br>should be reused rather than defining a new data type. |        |                  |           |
| VERIFICATION | Review of Design                                                                                                                                                                                                                     | COVERS | OG1-5 Review RD1 |           |
| RESPONSIBLE  | GMV                                                                                                                                                                                                                                  |        |                  |           |
| COMMENT      |                                                                                                                                                                                                                                      |        |                  |           |

# <span id="page-79-2"></span>**3.8.5 F500: Physical and resource requirements [PhyR]**

N./A.

# <span id="page-79-3"></span>**3.8.6 F600: Environmental and Operational requirements [OpR]**

| OpR_F601     | Plan execution monitoring                                                                                                                          |        |                                                             | Mandatory |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------|--------|-------------------------------------------------------------|-----------|
| STATEMENT    | A graphical tool shall allow the operator to command and monitor the execution of the<br>robotic reconfiguration plan, both simulated and onboard. |        |                                                             |           |
| VERIFICATION | Review of Design                                                                                                                                   | COVERS | Operational Concept RD3<br>Demonstrator preliminary Concept |           |
| RESPONSIBLE  | GMV                                                                                                                                                |        |                                                             |           |
| COMMENT      |                                                                                                                                                    |        |                                                             |           |

# <span id="page-79-4"></span>**3.8.7 F700: Safety requirements [SafR]**

N./A.

{80}------------------------------------------------

![](_page_80_Picture_0.jpeg)

## <span id="page-80-0"></span>**3.8.8 F800: Configuration and implementation requirements [ConfR]**

| ConfR_F801   | TASTE modelling                                                                                                                                                                                                                                                                                             |        |                  | Mandatory |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------------|-----------|
| STATEMENT    | The TASTE framework shall be used to model the software components running on the<br>OBC. These components include:<br>-<br>Functions related to robot autonomy (ERGO Agent and functional layer)<br>-<br>Sample OBSW for the management of the reconfigurable system (monitoring<br>and control of the SM) |        |                  |           |
| VERIFICATION | Review of Design                                                                                                                                                                                                                                                                                            | COVERS | OG1-5 Review RD1 |           |
| RESPONSIBLE  | GMV                                                                                                                                                                                                                                                                                                         |        |                  |           |
| COMMENT      |                                                                                                                                                                                                                                                                                                             |        |                  |           |

| ConfR_F802   | Development platform                                                                                                                                                                   | Mandatory |  |  |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|--|--|
| STATEMENT    | The development platform for the OBSW shall be Ubuntu Linux 18.04 LTS (64 bit) on x86.<br>The ESROCOS framework, and in particular TASTE, shall be adapted to run on this<br>platform. |           |  |  |
| VERIFICATION | Review of Design                                                                                                                                                                       | COVERS    |  |  |
| RESPONSIBLE  | GMV                                                                                                                                                                                    |           |  |  |
| COMMENT      |                                                                                                                                                                                        |           |  |  |

{81}------------------------------------------------

![](_page_81_Picture_0.jpeg)

# <span id="page-81-0"></span>**3.9 Validation Requirements [Gxxx]**

| VerR_G101    | Validation purpose                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |        |                      | Mandatory |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|----------------------|-----------|
| STATEMENT    | The MOSAR demonstrator shall allow to verify and validate the following functionalities<br>relevant for future modular spacecraft missions:<br><br>Creation of a re-configuration execution plan (FuncR_S105)<br><br>Simulation of the execution plan (FuncR_S106)<br><br>Manipulation and repositioning of SM (FuncR_S101)<br><br>Control and re-location of the WM (FuncR_S104, FuncR_S107)<br><br>Update/upgrade of satellite functionalities (FuncR_S102)<br><br>Data and power transfer between SM<br><br>Heat management between SM (FuncR_S115)<br><br>Failure detection and handling (FuncR_S111)<br><br>Resources re-allocation, data and power routing (FuncR_S110) |        |                      |           |
| VERIFICATION | Testing                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | COVERS | Mission Analysis RD2 |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |        |                      |           |
| COMMENT      |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |        |                      |           |

| VerR_G102    | Validation sequence                                                                                                                                                                                                                            |        |                        | Mandatory |
|--------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------------------|-----------|
| STATEMENT    | The validation shall include the following sequence:<br>1.<br>Calibrate/verify the simulation tool<br>2.<br>Simulate the reconfiguration process and generate a valid robot execution plan<br>3.<br>Execute the plan on the demonstrator setup |        |                        |           |
| VERIFICATION | Review of Design                                                                                                                                                                                                                               | COVERS | Guidelines AD1 OG9-R14 |           |
| RESPONSIBLE  | SPACEAPPS, DLR                                                                                                                                                                                                                                 |        |                        |           |
| COMMENT      |                                                                                                                                                                                                                                                |        |                        |           |

| VerR_G103    | SM modules selection                                                                                                                 |  |  | Mandatory |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------|--|--|-----------|
| STATEMENT    | The SM implemented in the MOSAR demonstrator should be representative of relevant<br>modules for future modular spacecraft missions. |  |  |           |
| VERIFICATION | Review of Design<br>COVERS<br>Mission Analysis RD2                                                                                   |  |  |           |
| RESPONSIBLE  | SITAEL, TAS-Fs                                                                                                                       |  |  |           |
| COMMENT      |                                                                                                                                      |  |  |           |

{82}------------------------------------------------

![](_page_82_Picture_0.jpeg)

| VerR_G104    | Orbital Test Facility                                                                                                                                                                                                                              |        |                                                  | Mandatory |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|--------------------------------------------------|-----------|
| STATEMENT    | The demonstrator shall be integrated in an orbital simulation facility to validate the<br>MOSAR scenarios                                                                                                                                          |        |                                                  |           |
| VERIFICATION | Inspection                                                                                                                                                                                                                                         | COVERS | Guidelines AD1 OG9-R13<br>Guidelines AD1 OG9-R14 |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                                                                                                                                          |        |                                                  |           |
| COMMENT      | The orbital dynamics is not relevant in OG9 – e.g. docking is not part of the scenarios.<br>The provided facility (in SPACEAPPS' lab) could however produce illumination<br>conditions that are relevant w.r.t. orbital applications (if relevant) |        |                                                  |           |

| VerR_G105    | Test facility dimensions                                                                                                                                                                                      |        |                    | Mandatory |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|--------------------|-----------|
| STATEMENT    | The test facility shall ensure a volume of 5 m (L)x 3.5 m (W)x 3 m (H) in order<br>to allow the integration of the test bench and all required components for the<br>regular performance of the demonstration |        |                    |           |
| VERIFICATION | Inspection                                                                                                                                                                                                    | COVERS | MOSAR Demonstrator |           |
| RESPONSIBLE  | SPACEAPPS                                                                                                                                                                                                     |        |                    |           |
| COMMENT      | Values TBC by PDR                                                                                                                                                                                             |        |                    |           |

| VerR_G106    | Test facility displays                                                                                 |        |                    | Mandatory |
|--------------|--------------------------------------------------------------------------------------------------------|--------|--------------------|-----------|
| STATEMENT    | The test facility shall provide displays to support the design and monitoring of<br>the execution plan |        |                    |           |
| VERIFICATION | Inspection                                                                                             | COVERS | MOSAR Demonstrator |           |
| RESPONSIBLE  | SPACEAPPS                                                                                              |        |                    |           |
| COMMENT      |                                                                                                        |        |                    |           |

| VerR_G107    | Test facility power                                                                            |  |  | Mandatory |
|--------------|------------------------------------------------------------------------------------------------|--|--|-----------|
| STATEMENT    | The test facility shall provide the required power for the performance of the<br>demonstration |  |  |           |
| VERIFICATION | COVERS<br>Inspection<br>MOSAR Demonstrator                                                     |  |  |           |
| RESPONSIBLE  | SPACEAPPS                                                                                      |  |  |           |
| COMMENT      | It can include barrier protections, flashing light during operations,                          |  |  |           |

{83}------------------------------------------------

![](_page_83_Picture_0.jpeg)

| VerR_G108    | Test facility safety features                                                                          |  |  | Mandatory |
|--------------|--------------------------------------------------------------------------------------------------------|--|--|-----------|
| STATEMENT    | The test facility shall provide safety features to guarantee the safe operation of<br>the demonstrator |  |  |           |
| VERIFICATION | Inspection<br>COVERS<br>MOSAR Demonstrator                                                             |  |  |           |
| RESPONSIBLE  | SPACEAPPS                                                                                              |  |  |           |
| COMMENT      | It can include barrier protections, flashing light during operations,                                  |  |  |           |

{84}------------------------------------------------

![](_page_84_Picture_0.jpeg)

# <span id="page-84-0"></span>**4 Conclusions**

The overall system requirements and associated verification methods are described in this document, detailing the specific requirements for each of the high level subsystems. They reflect the consortium analysis and vision of MOSAR system requirements to develop the demonstrator reflecting the proposed concept of space modular spacecraft and operations. This document will serve as a baseline for the preliminary design analysis, including the detailed system architecture, interfaces definitions between subsystems, the detailed technical requirements of the equipment and their respective preliminary design that shall be consolidated by the end of M9 (PDR milestone).

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* End of Document \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*