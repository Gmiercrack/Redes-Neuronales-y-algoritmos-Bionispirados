"""Pipeline completo de la Parte 1 en un solo comando (auditoría 4/5).

Uso oficial (configuración del reporte):
    python run.py                  # dims 2 y 3, 30 corridas, todo el pipeline

Demo en vivo (NO pisa los resultados oficiales: usa resultados/demo/):
    python run.py --dims 2 --runs 3 --resto --eta 0.001 --pso-c1 1.5
    python run.py --out resultados/mi-prueba --dims 2 --runs 3

verificar.py siempre revisa la carpeta que realmente se usó.
"""
import argparse
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OFICIAL = os.path.join(BASE, "resultados")
DEMO = os.path.join(BASE, "resultados", "demo")


def sh(cmd):
    print("+", " ".join(cmd))
    r = subprocess.run(cmd, cwd=BASE)
    if r.returncode != 0:
        sys.exit(r.returncode)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dims", type=int, nargs="+", default=[2, 3])
    ap.add_argument("--runs", type=int, default=30)
    ap.add_argument("--out", type=str, default=None,
                    help="directorio base de salida (por defecto: resultados/; "
                         "una ruta relativa se interpreta respecto al "
                         "directorio actual, no respecto a parte1/)")
    ap.add_argument("--no-verificar", action="store_true")
    ap.add_argument("--resto", nargs=argparse.REMAINDER, default=[],
                    help="flags extra para experimentos.py (p. ej. --eta 0.001)")
    a = ap.parse_args()

    demo = bool(a.resto) or a.runs != 30 or a.dims != [2, 3]
    # Ruta absoluta una sola vez: así --out relativo funciona desde cualquier
    # directorio (el subproceso corre con cwd=BASE) y no falla en Windows
    # entre unidades distintas (relpath lanzaría ValueError).
    base = os.path.abspath(a.out) if a.out else (DEMO if demo else OFICIAL)
    if demo and not a.out:
        print(f"Modo demo: los resultados van a {base} "
              f"(no se pisan los oficiales).")

    for dim in a.dims:
        sh([sys.executable, "experimentos.py", "--dim", str(dim),
            "--runs", str(a.runs), "--out", os.path.join(base, f"dim{dim}")]
           + a.resto)
    sh([sys.executable, "graficas.py", f"--base={base}"]
       + [str(d) for d in a.dims])
    # verificar.py siempre revisa la carpeta que realmente se usó
    # (antes, con --out X y config oficial, miraba resultados/ por defecto)
    if not a.no_verificar:
        sh([sys.executable, "verificar.py", "--out", base,
            "--dims"] + [str(d) for d in a.dims] +
           ["--runs", str(a.runs)])
    print("Pipeline completo OK.")


if __name__ == "__main__":
    main()
