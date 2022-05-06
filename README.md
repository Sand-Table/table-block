# The Sand Table
## Making Intelligent Things CS-358
This repository contains the 3D files and the code to create the sand table.

![](images/table.webp)
# Timeline / Notes / Explanations

## Week 1

- Design and discussion on the table
- Setting up the timeline 
 
---

## Week 2

### Hardware

- Going to the SKIL to discuss the design
    - We decide to use bouleau as a wood type

### Software

- Understanding the 17HS4401S and following some tutorials to manually control the motor such as

### Issues we ran into:
<details close>
<summary></summary>
We spent a lot of time trying to get consistent results in the rotation of the motor. Unfortuantely a <b>shortcirtuit</b> cost us a lot of time
</details>

---

## Week 3

### Hardware

- Construction of the radius axis as well as the platform on which it will be placed begins.
- Discussion around the design of the rotation axis and gearboxes to reduce the torque necessary take place. 
### Software

- A great [instructibles](https://www.instructables.com/DIY-3-Axis-Polar-CNC-Machine/) discussing the construction of a CNC tutorial exists that we followed.This allowed us to discover:
    - [grbl](https://github.com/grbl/grbl), software that allows to create an interface between the motors with the controllers and the computer.
    - [ugc](https://github.com/winder/Universal-G-Code-Sender/releases/tag/v2.0.11), an interface for grbl.

### Issues we ran into:
<details close>
<summary></summary>

</details>
