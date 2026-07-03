#!/usr/bin/env python3
"""
render-pdf.py — render PDF pages to PNG images for Claude to read (E9).

Supports the /ingest job: decks and reports arrive as PDFs; Claude reads
images, not PDF binaries beyond its page limits. Tries renderers in order
of quality/availability, no Python dependencies:

  1. pdftoppm  (poppler — `brew install poppler`)
  2. mutool    (mupdf — `brew install mupdf-tools`)
  3. Swift + CoreGraphics (macOS with Xcode CLT — compiled once, cached)

Usage:
  render-pdf.py <file.pdf> <out_dir> [first_page] [last_page]

Writes out_dir/page-001.png … and prints the file list.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SWIFT_RENDERER = r'''
import CoreGraphics
import Foundation
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
guard args.count >= 5, let first = Int(args[3]), let last = Int(args[4]),
      let doc = CGPDFDocument(URL(fileURLWithPath: args[1]) as CFURL) else {
    FileHandle.standardError.write("usage: render <pdf> <outdir> <first> <last>\n".data(using: .utf8)!)
    exit(2)
}
let outDir = args[2]
for pageNum in first...min(last, doc.numberOfPages) {
    guard let page = doc.page(at: pageNum) else { continue }
    let box = page.getBoxRect(.mediaBox)
    let scale: CGFloat = 2.0
    let w = Int(box.width * scale), h = Int(box.height * scale)
    guard let ctx = CGContext(data: nil, width: w, height: h, bitsPerComponent: 8,
        bytesPerRow: 0, space: CGColorSpaceCreateDeviceRGB(),
        bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue) else { continue }
    ctx.setFillColor(CGColor(red: 1, green: 1, blue: 1, alpha: 1))
    ctx.fill(CGRect(x: 0, y: 0, width: CGFloat(w), height: CGFloat(h)))
    ctx.scaleBy(x: scale, y: scale)
    ctx.drawPDFPage(page)
    guard let img = ctx.makeImage() else { continue }
    let out = URL(fileURLWithPath: String(format: "%@/page-%03d.png", outDir, pageNum))
    guard let dest = CGImageDestinationCreateWithURL(out as CFURL, UTType.png.identifier as CFString, 1, nil) else { continue }
    CGImageDestinationAddImage(dest, img, nil)
    CGImageDestinationFinalize(dest)
}
'''


def page_count(pdf: Path) -> int:
    """Best-effort page count (mdls on macOS, else big default)."""
    try:
        out = subprocess.run(
            ["mdls", "-name", "kMDItemNumberOfPages", "-raw", str(pdf)],
            capture_output=True, text=True, timeout=10).stdout.strip()
        return int(out)
    except Exception:
        return 500


def try_pdftoppm(pdf, out_dir, first, last):
    if not shutil.which("pdftoppm"):
        return False
    subprocess.run(
        ["pdftoppm", "-png", "-r", "144", "-f", str(first), "-l", str(last),
         str(pdf), str(out_dir / "page")], check=True)
    return True


def try_mutool(pdf, out_dir, first, last):
    if not shutil.which("mutool"):
        return False
    subprocess.run(
        ["mutool", "draw", "-r", "144", "-o", str(out_dir / "page-%03d.png"),
         str(pdf), f"{first}-{last}"], check=True)
    return True


def try_swift(pdf, out_dir, first, last):
    if sys.platform != "darwin" or not shutil.which("swiftc"):
        return False
    cache = Path(tempfile.gettempdir()) / "pm-copilot-pdf-render"
    cache.mkdir(exist_ok=True)
    binary = cache / "render"
    if not binary.exists():
        src = cache / "render.swift"
        src.write_text(SWIFT_RENDERER, encoding="utf-8")
        subprocess.run(["swiftc", "-O", "-o", str(binary), str(src)], check=True)
    subprocess.run([str(binary), str(pdf), str(out_dir), str(first), str(last)],
                   check=True)
    return True


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    pdf = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    if not pdf.is_file():
        print(f"error: {pdf} not found")
        return 1
    first = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    last = int(sys.argv[4]) if len(sys.argv) > 4 else page_count(pdf)
    out_dir.mkdir(parents=True, exist_ok=True)

    for renderer in (try_pdftoppm, try_mutool, try_swift):
        try:
            if renderer(pdf, out_dir, first, last):
                break
        except subprocess.CalledProcessError:
            continue
    else:
        print("error: no PDF renderer available.\n"
              "Install one of: `brew install poppler` (pdftoppm), "
              "`brew install mupdf-tools` (mutool), or Xcode CLT (swiftc).")
        return 1

    pages = sorted(out_dir.glob("page*.png"))
    for p in pages:
        print(p)
    print(f"{len(pages)} page(s) rendered → {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
