import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';
import 'package:mime/mime.dart';
import 'dart:convert'; 

class ApiService {
  static String _baseUrl = 'http://10.253.130.148:8000'; // Replace with your API base URL

  static Future<Map<String, dynamic>> uploadFile(
      String endpoint, File file, String userMedicalAilments) async {
    String fileName = file.path.split('/').last;
    String? mimeType = lookupMimeType(file.path);

    var request = http.MultipartRequest('POST', Uri.parse('$_baseUrl/$endpoint'));

    request.files.add(
      http.MultipartFile(
        'file',
        file.readAsBytes().asStream(),
        file.lengthSync(),
        filename: fileName,
        contentType: mimeType != null ? MediaType.parse(mimeType) : null,
      ),
    );

    // Add the userMedicalAilments field to the request
    request.fields['userMedicalAilments'] = userMedicalAilments; 

    try {
      var response = await request.send();
      if (response.statusCode == 200) {
        var responseBody = await response.stream.bytesToString();
        print('File uploaded successfully. Response: $responseBody');

        // Parse the response body here
        Map<String, dynamic> responseData = jsonDecode(responseBody);
        return responseData; 

      } else {
        print('File upload failed with status: ${response.statusCode}');
        throw Exception('File upload failed');
      }
    } catch (e) {
      print('Error uploading file: $e');
      throw Exception('Error uploading file');
    }
  }
}