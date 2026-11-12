# Spec Delta

## Purpose

Defines the playable behavior and acceptance criteria for controlling Anzu while Enkidu is mounted, across desktop and mobile input, camera, animation, and performance.

## ADDED Requirements

### Requirement: Mounted test scene
The game SHALL provide a playable `AnzuDesert` test scene in which Enkidu begins mounted on Anzu and the mounted pair is the player-controlled character.

#### Scenario: Entering the test scene
- **WHEN** the player starts `AnzuDesert`
- **THEN** Enkidu is visibly seated on Anzu
- **AND** mounted movement input is active without a mounting interaction

### Requirement: Authoritative locomotion state
The mounted pair SHALL have one authoritative locomotion state representing Idle, Walking, Running, Stopping, or Reversing, and dependent presentation systems SHALL consume that state.

#### Scenario: Starting from rest
- **WHEN** forward input rises above the movement dead zone while the state is Idle
- **THEN** the state changes to Walking

#### Scenario: Releasing movement
- **WHEN** movement input is released while the mounted pair is moving
- **THEN** the state changes to Stopping
- **AND** the state changes to Idle only after speed reaches the configured stop threshold

#### Scenario: Running
- **WHEN** forward input is active and the run input is held
- **THEN** the state changes to Running

#### Scenario: Returning to a walk
- **WHEN** the run input is released while forward input remains active
- **THEN** the state changes from Running to Walking

### Requirement: Weighted speed response
Forward input SHALL set a target speed up to walk speed, run input SHALL select run speed, and actual speed SHALL approach the target using independently configurable acceleration and deceleration rates.

#### Scenario: Accelerating to a walk
- **WHEN** the player applies partial or full forward input without run input
- **THEN** speed increases smoothly toward the proportional walk target
- **AND** speed does not jump directly to the target

#### Scenario: Accelerating to a run
- **WHEN** the player holds run while applying forward input
- **THEN** speed increases smoothly toward run speed

#### Scenario: Coasting to a stop
- **WHEN** the player releases movement input
- **THEN** speed decreases using the configured deceleration rate
- **AND** reaches zero without reversing direction

#### Scenario: Reducing input magnitude
- **WHEN** the player reduces movement-stick magnitude while moving
- **THEN** speed decelerates smoothly toward the new proportional target

### Requirement: Braking and controlled reverse
Backward input SHALL brake forward motion before permitting a separately limited reverse speed, preventing an immediate forward-to-reverse direction change.

#### Scenario: Braking from forward motion
- **WHEN** backward input is applied while forward speed is above the stop threshold
- **THEN** forward speed decreases using the configured braking behavior
- **AND** the mounted pair does not reverse until it has nearly stopped

#### Scenario: Reversing from rest
- **WHEN** backward input remains active at or below the stop threshold
- **THEN** the state changes to Reversing
- **AND** Anzu moves backward no faster than the configured reverse speed

### Requirement: Creature steering
Left and right movement input SHALL rotate Anzu around the vertical axis using a configurable turn rate, with movement following Anzu's facing direction and without sideways strafing.

#### Scenario: Steering while moving
- **WHEN** the player applies forward and left or right input
- **THEN** Anzu turns smoothly in the requested direction
- **AND** the mounted pair continues moving along Anzu's changing forward direction

#### Scenario: Steering from rest
- **WHEN** the player applies left or right input at rest
- **THEN** Anzu turns at the configured low-speed turn rate without translating sideways

### Requirement: Shared desktop and mobile actions
Desktop and mobile controls SHALL drive the same logical Move, Look, and Run actions so locomotion behavior does not depend on the active control surface.

#### Scenario: Keyboard movement
- **WHEN** the player uses WASD or arrow keys and the desktop run control
- **THEN** the shared movement and run actions receive equivalent values

#### Scenario: Mobile movement
- **WHEN** the player uses the virtual movement stick and mobile run button
- **THEN** the same movement and run actions receive equivalent values

#### Scenario: Mobile hold-to-run
- **WHEN** the player presses and holds the mobile run button while moving forward
- **THEN** the Run action remains active only for the duration of the press
- **AND** releasing the button returns the target locomotion state to Walking

#### Scenario: Switching control surface
- **WHEN** input changes between desktop controls and mobile simulation in the test environment
- **THEN** locomotion continues without resetting the mounted pair or creating a second controller state

### Requirement: Orbiting third-person camera
The mounted camera SHALL follow the mounted pair with damping while allowing independent orbit input, bounded vertical rotation, and recentering toward Anzu's travel direction.

#### Scenario: Orbiting the camera
- **WHEN** the player supplies Look input
- **THEN** the camera orbits around the mounted pair without changing Anzu's steering direction

#### Scenario: Vertical limits
- **WHEN** Look input would rotate beyond the configured vertical limits
- **THEN** camera pitch remains within those limits

#### Scenario: Camera recentering
- **WHEN** the player stops supplying Look input while the mounted pair travels
- **THEN** the camera smoothly recenters toward Anzu's travel direction after the configured delay

#### Scenario: Following acceleration and stopping
- **WHEN** the mounted pair accelerates, turns, or stops
- **THEN** the camera follows with damping and keeps Enkidu and Anzu framed together

### Requirement: Rider and creature animation synchronization
Enkidu and Anzu SHALL remain spatially and temporally synchronized while mounted, and visible animation behavior SHALL follow the authoritative locomotion state and actual speed.

#### Scenario: Changing locomotion state
- **WHEN** the state changes among Idle, Walking, Running, Stopping, and Reversing
- **THEN** the visible mounted animation responds to the new state
- **AND** Enkidu remains aligned with the mount point throughout the transition

#### Scenario: Matching animation to speed
- **WHEN** actual movement speed changes during acceleration or deceleration
- **THEN** gait playback changes smoothly enough to avoid a sudden cadence jump
- **AND** does not visibly propel the animated root away from the gameplay controller

#### Scenario: Extended traversal
- **WHEN** the player traverses continuously for sixty seconds while walking, running, and turning
- **THEN** the rider does not accumulate visible positional drift relative to Anzu

### Requirement: Test-scene performance evidence
The change SHALL record repeatable performance measurements for the mounted test scene on the development desktop and one representative midrange mobile device.

#### Scenario: Desktop performance run
- **WHEN** the sixty-second traversal sequence is measured in a development desktop build
- **THEN** the recorded median frame rate is at least 60 frames per second
- **AND** the record includes frame time and the dominant CPU or GPU cost

#### Scenario: Mobile performance run
- **WHEN** the same traversal sequence is measured in a device build on the selected midrange mobile target
- **THEN** the recorded median frame rate is at least 30 frames per second
- **AND** the record includes frame time, memory use, and the dominant rendering cost

#### Scenario: Missing mobile target
- **WHEN** no representative mobile device has been selected or measured
- **THEN** the mounted traversal slice is not considered performance-accepted for mobile
