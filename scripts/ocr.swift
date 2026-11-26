import Foundation
import Vision
import AppKit

// usage: swift ocr.swift <image_dir> <out_file>
let args = CommandLine.arguments
let dir = URL(fileURLWithPath: args[1])
let outPath = args[2]
let files = try FileManager.default.contentsOfDirectory(atPath: dir.path)
    .filter { $0.hasSuffix(".png") }
    .sorted { a, b in
        let na = Int(a.replacingOccurrences(of: ".png", with: "")) ?? 0
        let nb = Int(b.replacingOccurrences(of: ".png", with: "")) ?? 0
        return na < nb
    }
var output = ""
for f in files {
    let url = dir.appendingPathComponent(f)
    guard let img = NSImage(contentsOf: url),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { continue }
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.usesLanguageCorrection = true
    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    try handler.perform([req])
    let lines = (req.results ?? []).compactMap { $0.topCandidates(1).first?.string }
    output += "\n===== PAGE \(f.replacingOccurrences(of: ".png", with: "")) =====\n" + lines.joined(separator: "\n") + "\n"
}
try output.write(toFile: outPath, atomically: true, encoding: .utf8)
print("wrote \(outPath) pages=\(files.count)")
