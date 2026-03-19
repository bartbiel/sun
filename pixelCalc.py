import numpy as np

def px_per_helio_degree(aperture_mm,
                        focal_length_mm,
                        pixel_size_um,
                        B_deg,
                        L_deg):
    """
    Zwraca:
    - piksele na 1° heliograficzny (centrum)
    - piksele na 1° heliograficzny (z poprawką projekcji)
    - skala arcsec/pixel
    """

    # =============================
    # STAŁE
    # =============================
    SUN_DIAMETER_ARCSEC = 1920
    SUN_DIAMETER_HELIO = 180

    # =============================
    # KROK 1 — skala obrazu
    # =============================
    arcsec_per_pixel = 206.265 * pixel_size_um / focal_length_mm

    # =============================
    # KROK 2 — px na 1° w centrum
    # =============================
    arcsec_per_helio_deg = SUN_DIAMETER_ARCSEC / SUN_DIAMETER_HELIO
    px_per_deg_center = arcsec_per_helio_deg / arcsec_per_pixel

    # =============================
    # KROK 3 — poprawka projekcji
    # =============================
    B = np.deg2rad(B_deg)
    L = np.deg2rad(L_deg)

    cos_theta = np.cos(B) * np.cos(L)

    if cos_theta <= 0:
        raise ValueError("Region za brzegiem tarczy lub bardzo blisko limb!")

    px_per_deg_corrected = px_per_deg_center * cos_theta

    # =============================
    # WYNIK
    # =============================
    return {
        "arcsec_per_pixel": arcsec_per_pixel,
        "px_per_deg_center": px_per_deg_center,
        "px_per_deg_corrected": px_per_deg_corrected, #rezulat z poprawką projekcji
        "cos_theta": cos_theta
    }

# S = south → ujemna
B = -5
# E = east (lewa strona tarczy) → ujemna
L = -21

result = px_per_helio_degree(90, 900, 2.9, B, L )
print(f"Piksele na 1° z poprawką: {result['px_per_deg_corrected']:.2f}")
