# Tutorial 4 ─ Relaxed Planning Graph Planning 

## Satellite domain

```pddl
(define (domain satellite)

(:requirements :strips :typing)

(:types
    satellite
    instrument
    mode
    direction
)

(:predicates 
    (supports ?i - instrument ?m - mode)
    (calibration_target ?i - instrument ?d - direction)
    (on_board ?i - instrument ?s - satellite)
    (power_avail ?s - satellite)
    (pointing ?s - satellite ?d - direction)
    (have_image ?d - direction ?m - mode)
    (power_on ?i - instrument)
    (calibrated ?i - instrument)
)
; actions 
(:action turn_to
    :parameters (?s - satellite ?d_new - direction ?d_prev - direction)
    :precondition (and 
        (pointing ?s ?d_prev) 
        (not (= ?d_new ?d_prev))
    )
    :effect (and 
        (pointing ?s ?d_new)
        (not (pointing ?s ?d_prev))
    )
)

(:action switch_on
    :parameters (?i - instrument ?s - satellite)
    :precondition (and 
        (on_board ?i ?s) 
        (power_avail ?s)
    )
    :effect (and 
        (power_on ?i)
        (not (calibrated ?i))
        (not (power_avail ?s))
    )
)

(:action switch_off
    :parameters (?i - instrument ?s - satellite)
    :precondition (and 
        (on_board ?i ?s) 
        (power_on ?i)
    )
    :effect (and 
        (not (power_on ?i))
        (power_avail ?s)
    )
)

(:action calibrate
    :parameters (?s - satellite ?i - instrument  ?d - direcion)
    :precondition (and 
        (on_board ?i ?s) 
        (calibration_target ?i ?d)
        (pointing ?s ?d)
        (power_on ?i)
    )
    :effect (and 
        (callibrated ?i)
    )
)

(:action take_image
    :parameters (?s - satellite ?d - direcion ?i - instrument ?m - mode)
    :precondition (and 
        (calibrated ?i)
        (on_board ?i ?s)
        (supports ?i ?m)
        (power_on ?i)
        (pointing ?s ?d)
        (power_on ?i)
    )
    :effect (and 
        (have_image ?d ?m)
    )
)

)
```

## Satellite problem 

```pddl 
(define (problem tutorial_problem) (:domain satellite)
(:objects 
    satellite1 - satellite
    instrument1 - instrument
    thermograph1 - mode 
    GroundStation1 Phenomenon1 Phenomenon2 - direction
)

(:init
    (supports instrument1 thermograph1)
    (calibration_target instrument1 GroundStation1)
    (on_board instrument1 satellite1)
    (power_avail satellite1)
    (pointing satellite1 Phenomenon1)
)

(:goal (and 
    (have_image Phenomenon2 thermograph1)
))

)
```

## How would FF find a solution?

- Build the RPG for the initial state ($S_{init}$).
- Extract a solution from the RPG. 
- Compute the $h$ value for the initial state. 

**Answer**:

The Relaxed Planning Graph starting from the initial state is shown below.
The solution for the relaxed problem is highlighted (the colored actions). This relaxed solution is obtained by working backwards:

![Figure 1](figure/tut4-ex1-sol.png)
[Link to image](figure/tut4-ex1-sol.png)

Working backwards to extract RPG relaxed solution:

| **i** | **f(i)** (Fact Layer) | **g(i)** (Goal Layer) | **$O_i$** (Actions of the relaxed plan) |
| --- | --- | --- | --- |
| 3 | (supports instrument1 thermograph1) (calibration_target instrument1 GroundStation1) (on_board instrument1 satellite1) (power_avail satellite) (pointing satellite1 Phenomenon1) (power_on instrument1) (pointing satellite1 Phenomenon2) (pointing satellite1 GroundState1) (callibrated instrument1) (have_image Phenomenon2 thermograph1) | **(have_image Phenomenon2 thermograph1)** | (take_image satellite1 Phenomenon2 instrument1 thermograph1) | 
| 2 | (supports instrument1 thermograph1) (calibration_target instrument1 GroundStation1) (on_board instrument1 satellite1) (power_avail satellite) (pointing satellite1 Phenomenon1) (power_on instrument1) (pointing satellite1 Phenomenon2) (pointing satellite1 GroundState1) (callibrated instrument1) | **(callibrated instrument1)** (supports instrument1 thermograph1) (on_board instrument1 satellite1) (power_on instrument1) (pointing satellite1 Phenomenon2) | (callibrate satellite1 instrument1 GroundStation1) |
| 1 | (supports instrument1 thermograph1) (calibration_target instrument1 GroundStation1) (on_board instrument1 satellite1) (power_avail satellite) (pointing satellite1 Phenomenon1) (power_on instrument1) (pointing satellite1 Phenomenon2) (pointing satellite1 GroundState1) | (supports instrument1 thermograph1) (on_board instrument1 satellite1) **(power_on instrument1)** **(pointing satellite1 Phenomenon2)** (calibration_target instrument1 GroundStation1) **(pointing satellite1 GroundStation1)** | (switch_on instrument1 satellite1) (turn_to satellite1 Phenomenon2 Phenomenon1) (turn_to satellite1 GroundState1 Phenomenon1) | 
| 0 | (supports instrument1 thermograph1) (calibration_target instrument1 GroundStation1) (on_board instrument1 satellite1) (power_avail satellite) (pointing satellite1 Phenomenon1) | (supports instrument1 thermograph1) (on_board instrument1 satellite1) (calibration_target instrument1 GroundStation1) (power_avail satellite1) (pointing satellite1 Phenomenon1) | | 

> Goals that are not available from the previous fact layer ($s_i$ in $g(i)$ but not in $f(i-1)$) are bolded. 

The $h$ of the initial state is $\Sigma_{i=1}^{m}|O_i| = 5$. 

## Rovers domain

```pddl
(define (domain rovers)

(:requirements :strips :typing)

(:types
    rover
    waypoint
    store
    camera
    objective
    lander
    mode
)

(:predicates 
    (communicated_soil_data ?w - waypoint)
    (communicated_image_data ?o - objective ?m - mode)
    (at ?r - rover ?w - waypoint)
    (can_traverse ?r - rover ?w1 - waypoint ?w2 - waypoint)
    (visible ?from - waypoint ?to - waypoint)
    (available ?r - rover)
    (at_soil_sample ?w - waypoint)
    (have_soil_analysis ?r - rover ?w - waypoint)
    (equipped_for_soil_analysis ?r - rover)
    (equipped_for_imaging ?r - rover)
    (calibration_target ?c - camera ?obj - objective)
    (visible_from ?obj - objective ?w - waypoint)
    (calibrated ?c - camera ?r - rover)
    (on_board ?c - camera ?r - rover)
    (supports ?c - camera ?m - mode)
    (at_lander ?l - lander ?w - waypoint)
    (have_image ?r - rover ?obj - objective ?m - mode)
    (channel_free ?l - lander)
)

(:action navigate
    :parameters (?r - rover ?curr - waypoint ?next - waypoint)
    :precondition (and
        (can_traverse ?r ?curr ?next)
        (available ?r)
        (at ?r ?curr)
        (visible ?curr ?next)
    )
    :effect (and
        (not (at ?r ?curr))
        (at ?r ?next)
    )
)

(:action sample_soil
    :parameters (?r - rover ?s - store ?w - waypoint)
    :precondition (and
        (at ?r ?w)
        (at_soil_sample ?w)
        (equipped_for_soil_analysis ?r)
    )
    :effect (and
        (have_soil_analysis ?r ?w)
        (not (at_soil_sample ?w))
    )
)

(:action calibrate
    :parameters (?r - rover ?c - camera ?obj - objective ?w - waypoint)
    :precondition (and
        (equipped_for_imaging ?r)
        (calibration_target ?c ?obj)
        (at ?r ?w)
        (visible_from ?obj ?w)
        (on_board ?c ?r)
    )
    :effect (calibrated ?c ?r)
)

(:action take_image
    :parameters (?r - rover ?w - waypoint ?obj - objective ?c - camera ?m - mode)
    :precondition (and 
        (calibrated ?c ?r)
        (on_board ?c ?r)
        (equipped_for_imaging ?r)
        (supports ?c ?m)
        (visible_from ?obj ?w)
        (at ?r ?w)
    )
    :effect (and
        (have_image ?r ?obj ?m)
        (not (calibrated ?c ?r))
    )
)

(:action communicate_image_data
    :parameters (?r - rover ?l - lander ?obj - objective ?m - mode ?from - waypoint ?to - waypoint)
    :precondition (and
        (at ?r ?from)
        (at_lander ?l ?to)
        (have_image ?r ?obj ?m)
        (visible ?from ?to)
        (available ?r)
        (channel_free ?l)
    )
    :effect (and
        (not (available ?r))
        (not (channel_free ?l))
        (channel_free ?l)
        (communicated_image_data ?obj ?m)
        (available ?r)
    )
)

(:action communicate_soil_data
    :parameters (?r - rover ?l - lander ?obj - waypoint ?from - waypoint ?to - waypoint)
    :precondition (and
        (at ?r ?from)
        (at_lander ?l ?to)
        (have_soil_analysis ?r ?obj)
        (visible ?from ?to)
        (available ?r)
        (channel_free ?l)
    )
    :effect (and
        (not (available ?r))
        (not (channel_free ?l))
        (channel_free ?l)
        (communicated_soil_data ?obj)
        (available ?r)
    )
)

)
```

## Rovers problem

```pddl 
(define (problem tutorial_problem) (:domain rovers)
(:objects 
    w0 w1 w2 - waypoint
    rover - rover
    obj1 - objective 
    general - lander
    camera - camera
    high_res - mode 
    store - store 
)

(:init
    (visible w2 w0)
    (visible w0 w2)
    (visible w2 w1)
    (visible w1 w2)
    (can_traverse rover w1 w2)
    (can_traverse rover w2 w1)
    (visible_from obj1 w1)

    (at_lander general w0)
    (channel_free general)
    (at rover w2)
    (available rover)
    (equipped_for_imaging rover)
    (on_board camera rover)
    (calibration_target camera obj1)
    (supports camera high_res)
)

(:goal (and
    (communicated_image_data obj1 high_res)
))

)
```

## How would FF find a solution?
Working backwards to extract RPG relaxed solution:

| **i** | **f(i)** (Fact Layer) | **g(i)** (Goal Layer) | **$O_i$** (Actions of the relaxed plan) |
| --- | --- | --- | --- |
| 4 | (visible w2 w0) (visible w0 w2) (visible w2 w1) (visible w1 w2) (can_traverse rover w1 w2) (can_traverse rover w2 w1) (visible_from obj1 w1) (at_lander general w0) (channel_free general) (at rover w2) (available rover) (equipped_for_imaging rover) (on_board camera rover) (calibration_target camera obj1) (supports camera high_res) (at rover w1) (calibrated camera rover) (have_image rover obj1 high_res) (communicated_image_data obj1 high_res) | **(communicated_image_data obj1 high_res)** | (communicate_image_data rover general obj1 high_res w2 w0) |
| 3 | (visible w2 w0) (visible w0 w2) (visible w2 w1) (visible w1 w2) (can_traverse rover w1 w2) (can_traverse rover w2 w1) (visible_from obj1 w1) (at_lander general w0) (channel_free general) (at rover w2) (available rover) (equipped_for_imaging rover) (on_board camera rover) (calibration_target camera obj1) (supports camera high_res) (at rover w1) (calibrated camera rover) (have_image rover obj1 high_res) | (at rover w2) (at_lander general w0) **(have_image rover obj1 high_res)** (visible w2 w0) (available rover) (channel_free general) | (take_image rover w1 obj1 camera high_res) |
| 2 | (visible w2 w0) (visible w0 w2) (visible w2 w1) (visible w1 w2) (can_traverse rover w1 w2) (can_traverse rover w2 w1) (visible_from obj1 w1) (at_lander general w0) (channel_free general) (at rover w2) (available rover) (equipped_for_imaging rover) (on_board camera rover) (calibration_target camera obj1) (supports camera high_res) (at rover w1) (calibrated camera rover) | (at rover w2) (at_lander general w0) (visible w2 w0) (available rover) (channel_free general) **(calibrated camera rover)** (on_board camera rover) (equipped_for_imaging rover) (supports camera high_res) (visible_from obj1 w1) (at rover w1) | (calibrate rover camera obj1 w1) |
| 1 | (visible w2 w0) (visible w0 w2) (visible w2 w1) (visible w1 w2) (can_traverse rover w1 w2) (can_traverse rover w2 w1) (visible_from obj1 w1) (at_lander general w0) (channel_free general) (at rover w2) (available rover) (equipped_for_imaging rover) (on_board camera rover) (calibration_target camera obj1) (supports camera high_res) (at rover w1) | (at rover w2) (at_lander general w0) (visible w2 w0) (available rover) (channel_free general) (on_board camera rover) (equipped_for_imaging rover) (supports camera high_res) (visible_from obj1 w1) **(at rover w1)** (calibration_target camera obj1) | (navigate w2 w1) | 
| 0 | (visible w2 w0) (visible w0 w2) (visible w2 w1) (visible w1 w2) (can_traverse rover w1 w2) (can_traverse rover w2 w1) (visible_from obj1 w1) (at_lander general w0) (channel_free general) (at rover w2) (available rover) (equipped_for_imaging rover) (on_board camera rover) (calibration_target camera obj1) (supports camera high_res) | (at rover w2) (at_lander general w0) (visible w2 w0) (available rover) (channel_free general) (on_board camera rover) (equipped_for_imaging rover) (supports camera high_res) (visible_from obj1 w1) (calibration_target camera obj1) (can_traverse rover w2 w1) (visible w2 w1) | | 

> Goals that are not available from the previous fact layer ($s_i$ in $g(i)$ but not in $f(i-1)$) are bolded. 

The $h$ of the initial state is $\Sigma_{i=1}^{m}|O_i| = 4$. 

