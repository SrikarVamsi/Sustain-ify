import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:flutter_svg/flutter_svg.dart'; // Import for SVG assets (if used)

class ScanningPage extends StatefulWidget {
  final CameraDescription camera;
  final Function(File) onVideoUpload; // Callback function for video upload

  const ScanningPage({Key? key, required this.camera, required this.onVideoUpload})
      : super(key: key);

  @override
  _ScanningPageState createState() => _ScanningPageState();
}

class _ScanningPageState extends State<ScanningPage>
    with SingleTickerProviderStateMixin {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;
  bool _isFlashOn = false;
  bool _isRecording = false;
  File? _videoFile;
  late AnimationController _animationController;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = CameraController(
      widget.camera,
      ResolutionPreset.high,
    );
    _initializeControllerFuture = _controller.initialize();

    _animationController = AnimationController(
      vsync: this,
      duration: Duration(seconds: 10),
    );

    _animation = Tween<double>(begin: 0, end: 1).animate(_animationController)
      ..addListener(() {
        setState(() {});
      });
  }

  @override
  void dispose() {
    _controller.dispose();
    _animationController.dispose();
    super.dispose();
  }

  Future<void> _startVideoRecording() async {
    if (!_controller.value.isInitialized) {
      return;
    }

    if (_controller.value.isRecordingVideo) {
      return;
    }

    try {
      await _controller.startVideoRecording();
      _animationController.forward();
      setState(() {
        _isRecording = true;
      });
    } on CameraException catch (e) {
      print('Error starting video recording: $e');
    }
  }

  Future<void> _stopVideoRecording() async {
    if (!_controller.value.isRecordingVideo) {
      return;
    }

    try {
      XFile? videoFile = await _controller.stopVideoRecording();
      if (videoFile != null) {
        _videoFile = File(videoFile.path);
      }
      _animationController.reset();
      setState(() {
        _isRecording = false;
        // Call the callback function to upload the video
        widget.onVideoUpload(_videoFile!); 
        Navigator.pop(context, _videoFile);
      });
    } on CameraException catch (e) {
      print('Error stopping video recording: $e');
    }
  }

  // Function to pick a video from the gallery
  Future<void> _pickVideoFromGallery() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.video,
    );

    if (result != null) {
      _videoFile = File(result.files.single.path!);
      // Call the callback function to upload the video
      widget.onVideoUpload(_videoFile!);
      Navigator.pop(context, _videoFile);
    } else {
      print('Video picking canceled.');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          FutureBuilder<void>(
            future: _initializeControllerFuture,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.done) {
                return CameraPreview(_controller);
              } else {
                return Center(child: CircularProgressIndicator());
              }
            },
          ),
          Positioned(
            top: 40.0,
            right: 16.0,
            child: Row(
              children: [
                IconButton(
                  icon: Icon(Icons.arrow_back, color: Colors.white),
                  onPressed: () => Navigator.pop(context),
                ),
                SizedBox(width: 8.0),
                IconButton(
                  icon: Icon(
                    _isFlashOn ? Icons.flash_on : Icons.flash_off,
                    color: Colors.white,
                  ),
                  onPressed: () async {
                    setState(() {
                      _isFlashOn = !_isFlashOn;
                    });
                    await _controller.setFlashMode(
                      _isFlashOn ? FlashMode.torch : FlashMode.off,
                    );
                  },
                ),
              ],
            ),
          ),
          Center(
            child: Container(
              height: 280.0,
              width: 320.0,
              decoration: BoxDecoration(
                border: Border.all(
                  color: Colors.white.withOpacity(0.6),
                  width: 3.0,
                ),
                borderRadius: BorderRadius.circular(8.0),
              ),
              // You can add your corner SVGs here if needed
              child: Stack(
                children: [
                  // ... (Your corner SVGs, if applicable)
                ],
              ),
            ),
          ),
          Align(
            alignment: Alignment.bottomCenter,
            child: Padding(
              padding: const EdgeInsets.only(bottom: 20.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  // Button to pick video from gallery
                  FloatingActionButton(
                    heroTag: 'galleryButton', // Unique hero tag
                    onPressed: _pickVideoFromGallery,
                    child: Icon(Icons.photo_library),
                  ),
                  // Button to record video
                  GestureDetector(
                    onLongPressStart: (details) => _startVideoRecording(),
                    onLongPressEnd: (details) => _stopVideoRecording(),
                    child: Stack(
                      alignment: Alignment.center,
                      children: [
                        AnimatedBuilder(
                          animation: _animation,
                          builder: (context, child) {
                            return CircularProgressIndicator(
                              value: _animation.value,
                              strokeWidth: 8.0,
                              color: Colors.greenAccent[700],
                              backgroundColor: Colors.grey,
                            );
                          },
                        ),
                        CircleAvatar(
                          radius: 35.0,
                          backgroundColor: Colors.greenAccent[700],
                          child: Icon(
                            _isRecording ? Icons.stop : Icons.videocam,
                            color: Colors.white,
                            size: 35.0,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}