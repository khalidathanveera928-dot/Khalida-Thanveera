Gravitational Lensing Simulation
An interactive gravitational-lensing simulation that visualizes how light from a distant galaxy is deflected by a massive foreground lens.
What it does
This project uses the gravitational lens equation to perform inverse ray tracing. For each pixel in the observed image, the program traces the light ray backward through the lens and determines where that ray originated in the source galaxy.
The simulation produces a distorted view of a synthetic background galaxy around a massive foreground lens, while displaying the physical parameters used in the calculation.
Physics
The simulation uses the Einstein angular radius for a point-mass gravitational lens:
[
\theta_E =
\sqrt{
\frac{4GM}{c^2}
\frac{D_{DS}}{D_DD_S}
}
]
where:
(G) = gravitational constant
(M) = lens mass
(c) = speed of light
(D_D) = observer-to-lens distance
(D_S) = observer-to-source distance
(D_{DS}) = lens-to-source distance
For the current configuration:
Lens mass = (10^{12}) solar masses
Lens distance = 1000 Mpc
Source distance = 2000 Mpc
Calculated Einstein angle ≈ (9.783\times10^{-6}) radians
The point-mass lens equation is implemented in inverse form:
[
\beta =
\theta -
\frac{\theta_E^2}{|\theta|^2}\theta
]
This determines the corresponding source position for each observed image pixel.
Visualization
The background source is a procedurally generated spiral galaxy containing:
A central bulge
An exponential disk
Spiral-arm structure
An elliptical inclination
Radial brightness variation
The lensing transformation is then applied to this source image using inverse ray tracing.
Important visual approximation
The physical Einstein angle is calculated from the lensing equation, but the displayed Einstein radius is represented using a pixel-scale visualization radius.
This is intentional: the physical angular scale is far smaller than a useful 800 × 600 pixel visualization. The program therefore separates the physical calculation from the display scale.
The simulation should therefore be interpreted as a scientifically motivated visualization rather than a direct angular-scale rendering of an astronomical image.
Running the simulation
Requirements
Python 3
NumPy
Pygame
Install the required packages with:
pip install numpy pygame
Run
python3 lensing_simulation.py
A Pygame window will open displaying the gravitational-lensing simulation.
Controls
Arrow keys — move the background source position
R — reset the source position
ESC — exit the simulation
Changing the source position allows different lensing configurations to be explored interactively.
Project structure
Khalida-Thanveera/
├── lensing_simulation.py
├── .gitignore
└── README.md
Scientific scope
The current implementation focuses on a point-mass lens and inverse ray tracing. The source galaxy is synthetic rather than an observed galaxy catalogue.
Future extensions can incorporate real astronomical catalogue data, physically derived stellar systems, orbital self-tests, and additional measurable validation of the simulated physics.
Author
Khalida Thanveera
Gravitational lensing simulation developed for the Real Skies and Invented Worlds competition.
