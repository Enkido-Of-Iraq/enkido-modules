import Foundation
import AVFoundation
import CoreVideo
import CoreGraphics
import ImageIO

let root = "/Users/abbasmamoori/Documents/ChatGPT/New project/character-3d/enkidu-walk"
let out = URL(fileURLWithPath: root + "/Enkidu_slow_walk_preview_v14.mp4")
let fm = FileManager.default
let frames = (1...64).map { URL(fileURLWithPath: root + String(format: "/frames/walk_%04d.png", $0)) }
guard frames.allSatisfy({ fm.fileExists(atPath: $0.path) }) else { fatalError("Frame sequence is incomplete") }
if fm.fileExists(atPath: out.path) { try fm.removeItem(at: out) }
let writer = try AVAssetWriter(outputURL: out, fileType: .mp4)
let input = AVAssetWriterInput(mediaType: .video, outputSettings: [AVVideoCodecKey: AVVideoCodecType.h264, AVVideoWidthKey: 480, AVVideoHeightKey: 640, AVVideoCompressionPropertiesKey: [AVVideoAverageBitRateKey: 2200000, AVVideoMaxKeyFrameIntervalKey: 24]])
input.expectsMediaDataInRealTime = false
let adaptor = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: input, sourcePixelBufferAttributes: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32ARGB, kCVPixelBufferWidthKey as String: 480, kCVPixelBufferHeightKey as String: 640, kCVPixelBufferCGImageCompatibilityKey as String: true, kCVPixelBufferCGBitmapContextCompatibilityKey as String: true])
writer.add(input)
guard writer.startWriting() else { fatalError("Cannot start writer: \(String(describing: writer.error))") }
writer.startSession(atSourceTime: .zero)
for index in 0..<128 {
 while !input.isReadyForMoreMediaData {
  if writer.status == .failed { fatalError("Writer failed: \(String(describing: writer.error))") }
  Thread.sleep(forTimeInterval: 0.005)
 }
 try autoreleasepool {
  let url = frames[index % 64]
  guard let src = CGImageSourceCreateWithURL(url as CFURL, nil), let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { fatalError("Cannot read frame") }
  var buffer: CVPixelBuffer?
  let status = CVPixelBufferPoolCreatePixelBuffer(nil, adaptor.pixelBufferPool!, &buffer)
  guard status == kCVReturnSuccess, let pixel = buffer else { fatalError("Cannot allocate pixel buffer") }
  CVPixelBufferLockBaseAddress(pixel, [])
  guard let context = CGContext(data: CVPixelBufferGetBaseAddress(pixel), width: 480, height: 640, bitsPerComponent: 8, bytesPerRow: CVPixelBufferGetBytesPerRow(pixel), space: CGColorSpaceCreateDeviceRGB(), bitmapInfo: CGImageAlphaInfo.noneSkipFirst.rawValue | CGBitmapInfo.byteOrder32Big.rawValue) else { fatalError("Cannot create context") }
  context.draw(img, in: CGRect(x: 0, y: 0, width: 480, height: 640))
  CVPixelBufferUnlockBaseAddress(pixel, [])
  guard adaptor.append(pixel, withPresentationTime: CMTime(value: Int64(index), timescale: 24)) else { fatalError("Cannot append frame: \(String(describing: writer.error))") }
 }
}
input.markAsFinished()
let sem = DispatchSemaphore(value: 0)
writer.finishWriting { sem.signal() }
sem.wait()
guard writer.status == .completed else { fatalError("Encoding failed: \(String(describing: writer.error))") }
let asset = AVURLAsset(url: out)
let generator = AVAssetImageGenerator(asset: asset)
generator.appliesPreferredTrackTransform = true
let check = try generator.copyCGImage(at: CMTime(value: 16, timescale: 24), actualTime: nil)
let checkURL = URL(fileURLWithPath: root + "/video-verification-frame.png")
let dest = CGImageDestinationCreateWithURL(checkURL as CFURL, "public.png" as CFString, 1, nil)!
CGImageDestinationAddImage(dest, check, nil)
CGImageDestinationFinalize(dest)
print("Encoded 128 frames / two seamless cycles at 24 fps: " + out.path)
