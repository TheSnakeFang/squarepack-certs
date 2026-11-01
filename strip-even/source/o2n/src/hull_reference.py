# Independent check of the m4 vertex reduction: M(H) = min over 64 floor/ceiling patterns and 6 tilts of
# h(th1)+h(th6)+sum kappa(th_i, th_{i+1}, dy_i), kappa = right boundary of S(th1)+S(th2) at height dy.
import math, sys, itertools

def verts(th):
    c, s = math.cos(th), math.sin(th)
    return [(c*x - s*y, s*x + c*y) for x, y in ((.5,.5),(-.5,.5),(-.5,-.5),(.5,-.5))]
def kappa(t1, t2, dy):
    pts = [(a[0]+b[0], a[1]+b[1]) for a in verts(t1) for b in verts(t2)]
    # max x on the segment {y = dy} inside the convex hull of pts: max over pairs of points straddling dy
    best = -1e9
    for (x1,y1),(x2,y2) in itertools.combinations(pts, 2):
        if (y1-dy)*(y2-dy) <= 0 and y1 != y2:
            x = x1 + (dy-y1)*(x2-x1)/(y2-y1); best = max(best, x)
        elif y1 == y2 == dy: best = max(best, x1, x2)
    return best
