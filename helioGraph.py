import cv2
import numpy as np

def draw_heliographic_grid(image_path, step_deg=5):

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # wygładzenie
    blur = cv2.GaussianBlur(gray, (9,9), 0)

    # detekcja krawędzi
    edges = cv2.Canny(blur, 50, 150)

    # znajdź kontury
    contours,_ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # największy kontur = tarcza
    c = max(contours, key=cv2.contourArea)

    # dopasuj okrąg
    (cx,cy),R = cv2.minEnclosingCircle(c)
    cx,cy,R = int(cx), int(cy), int(R)

    overlay = img.copy()

    # narysuj limb
    cv2.circle(overlay,(cx,cy),R,(255,255,255),2)

    # szerokości heliograficzne
    for lat in range(-80,81,step_deg):

        phi = np.radians(lat)

        pts = []

        for lon in np.linspace(-90,90,400):

            lam = np.radians(lon)

            X = R*np.cos(phi)*np.sin(lam)
            Y = R*np.sin(phi)
            Z = R*np.cos(phi)*np.cos(lam)

            if Z > 0:

                px = int(cx + X)
                py = int(cy - Y)

                pts.append((px,py))

        for i in range(len(pts)-1):
            cv2.line(overlay, pts[i], pts[i+1], (255,255,255),1)

    # długości heliograficzne
    for lon in range(-80,81,step_deg):

        lam = np.radians(lon)

        pts = []

        for lat in np.linspace(-90,90,400):

            phi = np.radians(lat)

            X = R*np.cos(phi)*np.sin(lam)
            Y = R*np.sin(phi)
            Z = R*np.cos(phi)*np.cos(lam)

            if Z > 0:

                px = int(cx + X)
                py = int(cy - Y)

                pts.append((px,py))

        for i in range(len(pts)-1):
            cv2.line(overlay, pts[i], pts[i+1], (255,255,255),1)

    return overlay