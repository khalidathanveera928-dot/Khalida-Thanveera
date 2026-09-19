import math
import numpy as np
import pygame

WIDTH,HEIGHT=800,600
CX,CY=WIDTH//2,HEIGHT//2
G=6.67430e-11
C=299792458.0
PARSEC=3.085677581491367e16
MPC=1.0e6*PARSEC
SOLAR_MASS=1.98847e30
LENS_MASS=1.0e12*SOLAR_MASS
D_D=1000.0*MPC
D_S=2000.0*MPC
D_DS=D_S-D_D
THETA_E=math.sqrt((4*G*LENS_MASS/C**2)*(D_DS/(D_D*D_S)))
EINSTEIN_RADIUS=150.0

print(f"Physical Einstein angle: {THETA_E:.3e} rad")
print("Creating synthetic source galaxy...")

y=np.arange(HEIGHT,dtype=np.float32)
x=np.arange(WIDTH,dtype=np.float32)
X,Y=np.meshgrid(x,y)
dx=X-CX
dy=Y-CY
angle=np.deg2rad(18.0)
xr=dx*np.cos(angle)+dy*np.sin(angle)
yr=-dx*np.sin(angle)+dy*np.cos(angle)
q=0.58
r=np.sqrt(xr*xr+(yr/q)**2)
phi=np.arctan2(yr,xr)
safe_r=np.maximum(r,4.0)
bulge=np.exp(-(r/45.0)**2)
disk=np.exp(-r/95.0)
spiral=0.5+0.5*np.cos(2.7*phi+0.055*safe_r)
arms=spiral**8
galaxy_structure=disk*(0.30+1.10*arms)+1.7*bulge
galaxy_structure*=np.exp(-(r/430.0)**8)
red=1.10*galaxy_structure+0.55*bulge
green=0.72*galaxy_structure+0.65*bulge
blue=0.95*galaxy_structure+1.05*arms*disk
galaxy=np.stack([red,green,blue],axis=2)
galaxy/=np.max(galaxy)
galaxy*=255.0
galaxy=np.clip(galaxy,0,255).astype(np.uint8)

print("Source galaxy ready.")
print("Calculating inverse ray-traced image...")

DX=X-CX
DY=Y-CY
R2=DX*DX+DY*DY
safe=np.maximum(R2,1.0)
factor=1.0-(EINSTEIN_RADIUS**2/safe)
beta_x=CX+DX*factor
beta_y=CY+DY*factor

ix=np.rint(beta_x).astype(np.int32)
iy=np.rint(beta_y).astype(np.int32)
valid=(ix>=0)&(ix<WIDTH)&(iy>=0)&(iy<HEIGHT)
ix=np.clip(ix,0,WIDTH-1)
iy=np.clip(iy,0,HEIGHT-1)
image=galaxy[iy,ix].copy()
image[~valid]=0

lens_mask=R2<15**2
image[lens_mask]=(0,0,0)

pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Point-Mass Gravitational Lensing | Inverse Ray Tracing")
font=pygame.font.SysFont("Arial",20,bold=True)
small=pygame.font.SysFont("Arial",16)
surface=pygame.surfarray.make_surface(image.swapaxes(0,1))
clock=pygame.time.Clock()
source_x=0.0
source_y=0.0
running=True
source_x=0.0
source_y=0.0

def render_at_offset(sx,sy):
    bx=beta_x+sx
    by=beta_y+sy
    px=np.rint(bx).astype(np.int32)
    py=np.rint(by).astype(np.int32)
    ok=(px>=0)&(px<WIDTH)&(py>=0)&(py<HEIGHT)
    px=np.clip(px,0,WIDTH-1)
    py=np.clip(py,0,HEIGHT-1)
    out=galaxy[py,px].copy()
    out[~ok]=0
    out[lens_mask]=(0,0,0)
    return pygame.surfarray.make_surface(out.swapaxes(0,1))

while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                running=False
            elif event.key==pygame.K_LEFT:
                source_x-=5.0
                surface=render_at_offset(source_x,source_y)
            elif event.key==pygame.K_RIGHT:
                source_x+=5.0
                surface=render_at_offset(source_x,source_y)
            elif event.key==pygame.K_UP:
                source_y-=5.0
                surface=render_at_offset(source_x,source_y)
            elif event.key==pygame.K_DOWN:
                source_y+=5.0
                surface=render_at_offset(source_x,source_y)
            elif event.key==pygame.K_r:
                source_x=0.0
                source_y=0.0
                surface=render_at_offset(0.0,0.0)

    screen.blit(surface,(0,0))
    panel=pygame.Surface((500,185),pygame.SRCALPHA)
    panel.fill((3,6,18,190))
    screen.blit(panel,(15,15))
    screen.blit(font.render('POINT-MASS GRAVITATIONAL LENSING',True,(235,240,255)),(28,25))
    screen.blit(small.render(f'Einstein radius: {EINSTEIN_RADIUS:.1f} px',True,(190,205,230)),(28,55))
    screen.blit(small.render(f'Physical theta_E: {THETA_E:.3e} rad',True,(190,205,230)),(28,78))
    screen.blit(small.render('Lens mass: 1.0e12 solar masses',True,(190,205,230)),(28,101))
    screen.blit(small.render('Lens distance: 1000 Mpc | Source distance: 2000 Mpc',True,(190,205,230)),(28,124))
    screen.blit(small.render(f'Source offset: ({source_x:.1f}, {source_y:.1f}) px',True,(190,205,230)),(28,147))
    screen.blit(small.render('Arrow keys: move source | R: reset | ESC: quit',True,(255,220,110)),(28,170))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
